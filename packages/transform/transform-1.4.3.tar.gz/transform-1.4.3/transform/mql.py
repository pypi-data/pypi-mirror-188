import pandas as pd
import requests

from typing import Dict, List, Optional, Tuple
from metricflow.model.validations.validator_helpers import ModelValidationResults

from .auth import TransformAuth
from .models import (
    INF,
    NEGATIVE_ONE,
    CacheMode,
    Dimension,
    HealthReportStatus,
    Materialization,
    Metric,
    MqlMaterializeResp,
    MqlQueryStatusResp,
    MQLServer,
    MQLServerImage,
    ModelKey,
    PercentChange,
    Query,
    ServerHealthReport,
    TimeGranularity,
    UserState,
)
from .interfaces import AsyncDWValidationType, DWValidationType, MQLInterface
from .exceptions import QueryRuntimeException


class MQLClient:
    """Wrapper that exposes MQLInterface and BackendInterface"""

    def __init__(  # noqa: D
        self,
        api_key: Optional[str] = None,
        mql_server_url: Optional[str] = None,
        override_config: bool = True,
        use_async: bool = False,
        target_org_id: Optional[int] = None,  # no-op for non-admin use
    ) -> None:
        self.context = TransformAuth(api_key, mql_server_url, override_config, use_async, target_org_id)

    def create_query(  # noqa: D
        self,
        metrics: List[str],
        dimensions: List[str] = [],
        model_key_id: Optional[int] = None,
        where: Optional[str] = None,
        time_constraint: Optional[str] = None,
        time_granularity: Optional[str] = None,
        time_comparison: Optional[str] = None,
        order: Optional[List[str]] = None,
        limit: Optional[str] = None,
        cache_mode: Optional[str] = None,
        as_table: Optional[str] = None,
        allow_dynamic_cache: bool = True,
        result_format: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        trim: Optional[bool] = None,
    ) -> MqlQueryStatusResp:
        """Builds a query in MQL and returns a MqlQueryStatusResp detailing the results."""
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        query_id = self.context.mql_client.create_query(
            metrics,
            dimensions,
            model_key,
            where,
            time_constraint,
            TimeGranularity(time_granularity) if time_granularity else None,
            PercentChange(time_comparison) if time_comparison else None,
            order,
            None if limit in [INF, NEGATIVE_ONE, int(NEGATIVE_ONE)] else limit,
            CacheMode(cache_mode) if cache_mode else None,
            as_table,
            allow_dynamic_cache,
            result_format,
            start_time,
            end_time,
            trim,
        )
        return self.context.mql_client.get_query_status(query_id)

    def create_data_warehouse_validations_job(
        self, dw_validation_type: AsyncDWValidationType, model_key_id: Optional[int] = None
    ) -> str:
        """Submits a data warehouse validations job and return the associated query job id"""
        return self.context.mql_client.create_data_warehouse_validations_job(
            dw_validation_type=dw_validation_type, model_id=model_key_id
        )

    def query_latest_metric_change(self, metric_name: str) -> MqlQueryStatusResp:
        """Create a query for the latest change in the specified metric"""
        query_id = self.context.mql_client.query_latest_metric_change(metric_name)
        return self.context.mql_client.get_query_status(query_id)

    def query(  # noqa: D
        self,
        metrics: List[str],
        dimensions: List[str] = [],
        model_key_id: Optional[int] = None,
        where: Optional[str] = None,
        time_constraint: Optional[str] = None,
        time_granularity: Optional[str] = None,
        time_comparison: Optional[str] = None,
        order: Optional[List[str]] = None,
        limit: Optional[str] = None,
        cache_mode: Optional[str] = None,
        as_table: Optional[str] = None,
        allow_dynamic_cache: bool = True,
        timeout: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> pd.DataFrame:
        """Builds a query in MQL and returns pandas dataframe of queried result.

        TODO: Now that MQL optionally returns synchronous results on query creation,
        the python interface should support opportunistically returning these rather
        than having to always poll for results
        """
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        query_id = self.context.mql_client.create_query(
            metrics=metrics,
            dimensions=dimensions,
            model_key=model_key,
            where_constraint_str=where,
            time_constraint=time_constraint,
            time_granularity=TimeGranularity(time_granularity) if time_granularity else None,
            time_comparison=PercentChange(time_comparison) if time_comparison else None,
            order=order,
            limit=None if limit in [INF, NEGATIVE_ONE, int(NEGATIVE_ONE)] else limit,
            cache_mode=CacheMode(cache_mode) if cache_mode else None,
            as_table=as_table,
            allow_dynamic_cache=allow_dynamic_cache,
            start_time=start_time,
            end_time=end_time,
        )
        return self.get_query_dataframe(query_id, timeout)

    def query_safe(  # noqa: D
        self,
        metrics: List[str],
        dimensions: List[str] = [],
        model_key_id: Optional[int] = None,
        where: Optional[str] = None,
        time_constraint: Optional[str] = None,
        time_granularity: Optional[str] = None,
        time_comparison: Optional[str] = None,
        order: Optional[List[str]] = None,
        limit: Optional[str] = None,
        cache_mode: Optional[str] = None,
        as_table: Optional[str] = None,
        allow_dynamic_cache: bool = True,
        timeout: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> MqlQueryStatusResp:
        """Builds a query in MQL and returns a MqlQueryStatusResp.

        Instead of throwing if unable to get query, it returns a response class to show the details of the query.
        """
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        query_id = self.context.mql_client.create_query(
            metrics,
            dimensions,
            model_key,
            where,
            time_constraint,
            TimeGranularity(time_granularity) if time_granularity else None,
            PercentChange(time_comparison) if time_comparison else None,
            order,
            None if limit in [INF, NEGATIVE_ONE, int(NEGATIVE_ONE)] else limit,
            CacheMode(cache_mode) if cache_mode else None,
            as_table,
            allow_dynamic_cache,
            start_time,
            end_time,
        )
        try:
            result = self.get_query_dataframe(query_id, timeout)
        except QueryRuntimeException:
            result = None
        resp = self.context.mql_client.get_query_status(query_id)
        return MqlQueryStatusResp(
            query_id=resp.query_id,
            status=resp.status,
            error=resp.error,
            sql=resp.sql,
            result=result,
            chart_value_max=resp.chart_value_max,
            chart_value_min=resp.chart_value_min,
            result_source=resp.result_source,
            result_primary_time_granularity=resp.result_primary_time_granularity,
            warnings=resp.warnings,
        )

    def list_queries(self, active_only: bool, limit: Optional[int] = None) -> List[Query]:
        """Retrieve a list of queries from MQL server."""
        return self.context.mql_client.get_queries(active_only=active_only, limit=limit)

    def list_metrics(self, model_key_id: Optional[int] = None) -> Dict[str, Metric]:
        """Returns a dictionary {metric_name: Metric}."""
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        metrics = {m.name: m for m in self.context.mql_client.get_metrics(model_key)}
        metrics_metadata = self.context.backend_client.get_metrics_metadata(model_key_id=model_key_id)
        for data in metrics_metadata:
            metrics[data["name"]].input_metadata(data)
        return metrics

    def get_metric(self, metric_name: str, model_key_id: Optional[int] = None) -> Metric:
        """Retrieve a Metric Object by name."""
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        metric = self.context.mql_client.get_metric_by_name(metric_name, model_key=model_key)
        metric.input_metadata(
            self.context.backend_client.get_metric_metadata_by_name(metric_name, model_key_id=model_key_id)
        )
        return metric

    def create_materialization(  # noqa: D
        self,
        materialization_name: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        model_key_id: Optional[int] = None,
        output_table: Optional[str] = None,
        force: bool = False,
    ) -> MqlQueryStatusResp:
        """Implements Materialize (new) mutation in MQL/GQL and returns MqlQueryStatusResp object. Can be very expensive if a large time range is provided.

        Note: This is an asynchronous function (for synchronous function, see materialize)
        """
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        query_id = self.context.mql_client.create_materialization(
            materialization_name, start_time, end_time, model_key, output_table, force
        )
        return self.context.mql_client.get_query_status(query_id)

    def materialize(  # noqa: D
        self,
        materialization_name: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        model_key_id: Optional[int] = None,
        output_table: Optional[str] = None,
        force: bool = False,
        timeout: Optional[int] = None,
    ) -> MqlMaterializeResp:
        """Builds materilization and returns MqlMaterializeResp object. Can be very expensive if a large time range is provided.

        Note: This is a synchronous function (for asynchronous function, see create_materialization)
        """
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        query_id = self.context.mql_client.create_materialization(
            materialization_name, start_time, end_time, model_key, output_table, force
        )
        schema, table = self.get_materialization_result(query_id, timeout)
        return MqlMaterializeResp(table=table, schema=schema, query_id=query_id)

    def drop_materialization(  # noqa: D
        self,
        materialization_name: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        model_key_id: Optional[int] = None,
    ) -> MqlQueryStatusResp:
        """Implements drop materialization mutation in MQL/GQL. Can be very expensive if a large time range is provided.

        Note: This is an asynchronous function, the query may not be completed after the function returns.
        """
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        query_id = self.context.mql_client.drop_materialization(materialization_name, start_time, end_time, model_key)
        return self.context.mql_client.get_query_status(query_id)

    def list_materializations(self, model_key_id: Optional[int] = None) -> List[Materialization]:
        """List the materializations for the Organization with their available metrics and dimensions."""
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        return sorted(self.context.mql_client.get_materializations(model_key), key=lambda m: m.name)

    def commit_configs(
        self,
        config_dir: str,
        is_validation: bool = False,
        is_dbt_model: bool = False,
        dbt_profile: Optional[str] = None,
        dbt_target: Optional[str] = None,
    ) -> Tuple[ModelKey, ModelValidationResults]:
        """Validates and commits yaml transform configs in the provided directory. Returns a ModelKey object."""
        return self.context.backend_client.commit_configs(
            config_dir=config_dir,
            is_validation=is_validation,
            is_dbt_model=is_dbt_model,
            dbt_profile=dbt_profile,
            dbt_target=dbt_target,
        )

    def validate_configs(
        self,
        config_dir: str,
        is_dbt_model: bool = False,
        dbt_profile: Optional[str] = None,
        dbt_target: Optional[str] = None,
    ) -> Tuple[ModelKey, ModelValidationResults]:
        """Finds and validates yaml transform configs in the provided directory. Returns a tuple (repo, branch, commit)"""
        return self.context.backend_client.validate_configs(
            config_dir=config_dir, is_dbt_model=is_dbt_model, dbt_profile=dbt_profile, dbt_target=dbt_target
        )

    def promote_model(self, model_key: ModelKey) -> None:
        """Promotes a given model key to be the current/primary model for the organization"""
        return self.context.backend_client.promote_model_with_key(model_key=model_key)

    def health_report(self) -> List[ServerHealthReport]:
        """Performs a health check on all mql servers within the organization and returns List[ServerHealthReport]."""
        servers = self.context.backend_client.get_org_mql_servers()
        # in the case where the user has a local override, we still want to run a health report
        if self.context.mql_client.rest_api_url not in [s.url for s in servers]:
            servers.append(
                MQLServer(id=0, name="Local Override", url=self.context.mql_client.rest_api_url, is_org_default=False)
            )
        result = []
        for s in servers:
            test_server = MQLInterface(self.context.auth_header, s.url)
            try:
                version, health = test_server.get_health_report()
                result.append(
                    ServerHealthReport(
                        name=s.name, status=HealthReportStatus.SUCCESS.value, url=s.url, version=version, servers=health
                    )
                )
            except Exception as e:  # noqa: D
                result.append(
                    ServerHealthReport(
                        name=s.name,
                        status=HealthReportStatus.FAIL.value,
                        url=s.url,
                        error_message="Unable to connect to MQL server",
                    )
                )
        return result

    def drop_cache(self) -> bool:
        """Drops the entire MQL cache. Only do this is the cache is somehow corrupt. Returns boolean about operation result."""
        return self.context.mql_client.drop_cache()

    def identify(self) -> UserState:
        """Returns a UserState object describing current user."""
        return self.context.user_state

    def ping(self) -> requests.Response:
        """Returns ping response from currently selected MQL server."""
        return self.context.mql_client.ping()

    def list_servers(self) -> List[MQLServer]:
        """Returns a list of MQL servers within the organization."""
        return self.context.backend_client.get_org_mql_servers()

    def poll_for_query_completion(self, query_id: str, timeout: Optional[int] = None) -> MqlQueryStatusResp:
        """Poll for query completion, displaying some progress indication."""
        return self.context.mql_client.poll_for_query_completion(query_id, timeout)

    def get_materialization_result(self, query_id: str, timeout: Optional[int] = None) -> Tuple[str, str]:
        """Retrieves materialized table resulting from successful materialization query."""
        return self.context.mql_client.get_materialization_result(query_id, timeout)

    def get_query_dataframe(self, query_id: str, timeout: Optional[int] = None) -> pd.DataFrame:
        """Retrieves query results in Pandas DataFrame format.

        Includes logic for:
        1. Polling for completion
        2. Paging through results
        3. Converting JSON to a Pandas DataFrame
        """
        return self.context.mql_client.get_query_dataframe(query_id, timeout)

    def get_data_warehouse_validations_job_result(
        self, query_id: str, timeout: Optional[int] = None
    ) -> ModelValidationResults:
        """Retrieves query results in Pandas DataFrame format.

        Includes logic for:
        1. Polling for completion
        2. Converting JSON to a ModelValidationResults
        """
        return self.context.mql_client.get_data_warehouse_validation_query(query_id, timeout)

    def get_model_key(self, model_key_id: int) -> ModelKey:
        """Retrieves ModelKey object given the id."""
        return self.context.backend_client.get_model_key(model_key_id)

    def get_current_model_key(self) -> ModelKey:
        """Retrieves the current ModelKey object for the user's organization"""
        return self.context.backend_client.get_current_model_key()

    def latest_mql_image(self) -> MQLServerImage:
        """Retrieves the latest MQL server image."""
        return self.context.backend_client.get_latest_mql_server_image()

    def get_dimension_values(
        self,
        metric_name: str,
        dimension_name: str,
        model_key_id: Optional[int] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[str]:
        """Retrieves a list of dimension values given a [metric_name, dimension_name]."""
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        return self.context.mql_client.get_dimension_values(
            metric_name, dimension_name, model_key=model_key, page_number=page_number, page_size=page_size
        )

    def list_dimensions(
        self,
        metric_names: Optional[List[str]] = None,
        model_key_id: Optional[int] = None,
    ) -> Dict[str, Dimension]:
        """Retrieves a list of all Dimension objects."""
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        dimensions = self.context.mql_client.get_dimensions(metric_names, model_key)
        return {dim.name: dim for dim in dimensions}

    def get_data_warehouse_issues(
        self, type: DWValidationType, model_key_id: Optional[int] = None
    ) -> ModelValidationResults:
        """DEPRECATED: Use create_data_warehouse_validations_job + get_data_warehouse_validations_job_result instead

        Retrieves a list of warehosue validation issues with for the type on the model.
        """
        model_key = self.get_model_key(model_key_id) if model_key_id else None
        return self.context.mql_client.get_data_warehouse_validation_issues(type, model_key)

    def get_query_status(self, query_id: str) -> MqlQueryStatusResp:
        """Returns a query response object."""
        return self.context.mql_client.get_query_status(query_id)

    def invalidate_all_caches(self) -> bool:
        """Invalidates all caches."""
        return self.context.mql_client.invalidate_all_caches()

    def invalidate_cache_for_metric(self, metric_name: str) -> bool:
        """Invalidates caches related to the given metric."""
        return self.context.mql_client.invalidate_cache_for_metric(metric_name)
