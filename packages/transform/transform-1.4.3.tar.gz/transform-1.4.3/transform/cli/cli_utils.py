import os
import ast
import logging
import click

from dateutil.parser import parse
from functools import wraps
from typing import Any, Callable, List, Optional

from ..constants import DEFAULT_QUERY_TIMEOUT
from ..models import CacheMode, PercentChange, INF, NEGATIVE_ONE, DEFAULT_LIMIT, TimeGranularity, PrintStyle


class PythonLiteralOption(click.Option):
    """Click class to decode a string literal into a Python object."""

    def type_cast_value(self, ctx, value):  # type: ignore
        """Cast to Python obj, throws exception if we are unable to cast"""

        # For non-required inputs we receive a None here, and should return it
        if value is None:
            return None
        try:
            return ast.literal_eval(value)
        except Exception:
            raise click.BadParameter(value)


def query_observability_options(function: Callable) -> Callable:
    """Options for display mql server log"""
    function = click.option(
        "--debug",
        required=False,
        is_flag=True,
        default=False,
        help="Enable showing query log in the terminal for debugging purpose",
    )(function)

    function = click.option(
        "--web",
        required=False,
        is_flag=True,
        default=False,
        help="Open the MQL server logs on the web",
    )(function)

    return function


def async_options(function: Callable) -> Callable:
    """Options for async commands"""
    function = click.option(
        "--detach",
        default=False,
        type=bool,
        help="Returns the created query ID to allow for asynchronous querying.",
    )(function)

    function = click.option(
        "-t",
        "--timeout",
        type=int,
        default=DEFAULT_QUERY_TIMEOUT,
        help="Sets the timeout to wait for query completion. Pass 0 to remove any timeout.",
    )(function)

    return function


def show_all_issues_option(function: Callable) -> Callable:
    """Used for showing all issues (warnings, future-errors, and errors) instead of just errors"""
    return click.option(
        "--show-all", is_flag=True, default=False, help="If specified, prints warnings and future-errors"
    )(function)


def verbose_issues_option(function: Callable) -> Callable:
    """Used for showing extra details issues might have that aren't shown by default"""
    return click.option(
        "--verbose-issues", is_flag=True, default=False, help="If specified, prints any extra details issues might have"
    )(function)


def dw_timeout_option(function: Callable) -> Callable:
    """Used for timing out async dw validation results polling"""
    return click.option(
        "-t",
        "--timeout",
        type=int,
        help="Sets the timeout in seconds to wait for individual data warehouse validations to finish. Defaults to None, meaning no timeout",
    )(function)


def dbt_project_option(function: Callable) -> Callable:
    """Used specifying the config dir should be interpreted as a dbt project"""
    return click.option(
        "--dbt-project", is_flag=True, default=False, help="If specified, treats config directory as dbt project"
    )(function)


def dbt_profile_option(function: Callable) -> Callable:
    """Used for specifying the the dbt profile that should be used with the dbt project"""
    return click.option(
        "--dbt-profile",
        type=str,
        required=False,
        help="The dbt profile to use when using `--dbt-project`. Defaults to the profile specified in dbt_profile.yml",
    )(function)


def dbt_target_option(function: Callable) -> Callable:
    """Used for specifying the the dbt profile target that should be used with the dbt project"""
    return click.option(
        "--dbt-target",
        type=str,
        required=False,
        help="The dbt target to use when using `--dbt-target`. Defaults to the target specified in dbt profile defintion",
    )(function)


def config_validation_options(function: Callable) -> Callable:
    """Common options when validating or committing configs"""
    function = click.option(
        "--config-dir",
        type=str,
        required=False,
        default=os.getcwd(),
        help="Path to directory containing Transform yaml models",
    )(function)

    function = click.option(
        "--skip-dw",
        is_flag=True,
        default=False,
        help="If specified, skips the data warehouse validations",
    )(function)

    function = show_all_issues_option(function)
    function = verbose_issues_option(function)
    function = dw_timeout_option(function)
    function = dbt_project_option(function)
    function = dbt_profile_option(function)
    function = dbt_target_option(function)
    return function


def query_options(function: Callable) -> Callable:
    """Common options for a query, adding support for limit, order, and cache-mode"""
    function = click.option(
        "--config-dir",
        type=str,
        required=False,
        help="Path to directory containing Transform yaml models to execute query against",
    )(function)

    function = dbt_project_option(function)
    function = dbt_profile_option(function)
    function = dbt_target_option(function)

    function = click.option(
        "--force-commit",
        required=False,
        is_flag=True,
        default=False,
        help="When using a local model (--config-dir), don't skip the commit process even if no changes are detected.",
    )(function)

    function = click.option(
        "--cache-mode",
        type=click.Choice(
            list(map(lambda x: x.value, CacheMode)),
            case_sensitive=False,
        ),
        # Cast as CacheMode type
        callback=lambda ctx, param, value: CacheMode(value) if value is not None else None,
        help="""Optional interface allowing you to control how it is reading and writing from Transform's cache.\n
        [r] read from cached tables\n
        [w] write to cached tables\n
        [rw] read + write -- DEFAULT\n
        [i] neither read nor write from cache""",
    )(function)

    function = click.option(
        "--order",
        required=False,
        multiple=True,
        help='Metrics or dimensions to order by ("-" in front of a column means descending). For example: --order -ds',
    )(function)

    function = click.option(
        "--limit",
        required=False,
        type=str,
        help="Limit the number of rows out(Default: 100) using an int or 'inf' for no limit. For example: --limit 100 or --limit inf",
    )(function)

    function = click.option(
        "--where",
        required=False,
        type=str,
        default=None,
        help="SQL-like where statement provided as a string. For example: --where \"ds = '2020-04-15'\"",
    )(function)

    function = click.option(
        "--time-constraint",
        required=False,
        type=str,
        default=None,
        help="Optional TimeConstraint on query (written as a WHERE clause, ie: `ds < '2020-01-01')",
    )(function)

    function = click.option(
        "--time-granularity",
        type=click.Choice(
            list(map(lambda x: x.value, TimeGranularity)),
            case_sensitive=False,
        ),
        # Cast as TimeGranularity type
        callback=lambda ctx, param, value: TimeGranularity(value) if value is not None else None,
    )(function)

    function = click.option(
        "--time-comparison",
        type=click.Choice(
            list(map(lambda x: x.value, PercentChange)),
            case_sensitive=False,
        ),
        # Cast as PercentChange type
        callback=lambda ctx, param, value: PercentChange(value) if value is not None else None,
    )(function)

    function = start_end_time_options(function)

    function = click.option(
        "--style",
        type=click.Choice(
            list(map(lambda x: x.value, PrintStyle)),
            case_sensitive=False,
        ),
        default="standard",
        # Cast as PrintStyle type
        callback=lambda ctx, param, value: PrintStyle(value) if value is not None else None,
        help="Choose your print style. Default: standard",
    )(function)

    function = click.option(
        "--trim",
        required=False,
        type=bool,
        help="Trim incomplete time periods at the start and end of query results to avoid misleading data.",
    )(function)

    return function


def validate_query_args(limit: Optional[str]) -> None:
    """Logic to perform query validation before sending to the MQL Server"""
    if limit and not (limit.isnumeric() or limit in [INF, NEGATIVE_ONE]):
        click.echo(
            f"❌ limit must be an int (--limit {DEFAULT_LIMIT}) or {NEGATIVE_ONE} or {INF} (--limit {INF}) to specify no limit"
        )
        exit()


def metrics_and_dimensions_options(function: Callable) -> Callable:
    """TODO: could we validate that these exist using a callback?"""

    function = click.option(
        "--metrics",
        required=True,
        multiple=True,
        help="Metrics to query for: syntax is --metrics bookings. Submit a list of metrics by providing multiple --metrics flags.",
        callback=lambda ctx, param, value: __validate_and_normalize_query_inputs("--metrics ", value),
    )(function)
    function = click.option(
        "--dimensions",
        required=False,
        multiple=True,
        default=[],
        help="Dimensions to group by: syntax is --dimensions ds. Submit a list of metrics by providing multiple --dimensions flags.",
        callback=lambda ctx, param, value: __validate_and_normalize_query_inputs("--dimensions ", value),
    )(function)
    return function


def __validate_and_normalize_query_inputs(option_name: str, value: List[str]) -> List[str]:
    """A callback executed to normalize and validate query inputs for metrics and dimensions.

    TODO: Eventually we should validate that the metrics and dimensions actually exist on the org,
        avoiding a round trip and failed query. This would be a good place for that.
    """

    for v in value:
        # We have a comma-separated list of metrics or dimensions, explode this into a list and return
        if "," in v:
            return [i.strip() for i in v.split(",")]

    return list(value)


def no_active_mql_servers(org_name: str) -> None:
    """Read out if there are no mql servers found"""
    click.echo(f"‼️  The {org_name} organization doesn't currently have an active MQL Server.")
    click.echo(
        "An admin can create a new MQL Server at:\n\n    https://app.transformdata.io/settings/org/mql",
    )


def validate_date_string(datetime_str: Optional[str]) -> Optional[str]:
    """Validates the date string, raises exception if invalid."""
    if datetime_str is None:
        return None

    try:
        parse(datetime_str)
    except Exception:
        raise click.BadParameter("must be valid iso8601 timestamp (eg., '2020-01-04')")
    return datetime_str


def enable_debug_log_file() -> None:  # noqa: D
    # Writing to the console would be ideal, but the newlines get messed up so it's hard to read.
    # e.g. log line looks like: Waiting for query2021-07-27 10:19:40,051 - http.client ...
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filemode="a",
        filename="debug.log",
    )


def get_query_logs_url_for_id(query_id: str) -> str:
    """Returns the query log URL to the web UI given the query_id"""
    return f"https://app.transformdata.io/mql/query/{query_id}?tab=server_logs"


def exception_handler(func: Callable[..., Any]) -> Callable[..., Any]:  # type: ignore[misc]
    """Decorator to handle exceptions

    TODO: handle custom exceptions
    """

    @wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore
        try:
            func(*args, **kwargs)
        except Exception as e:
            debug = os.getenv(key="DEBUG_MQL", default=False)
            click.echo(f"\nERROR: {str(e)}")
            if debug:
                raise e
            exit(1)

    return wrapper


def start_end_time_options(function: Callable) -> Callable:
    """Options for start_time and end_time."""
    function = click.option(
        "--start-time",
        type=str,
        default=None,
        help="Optional iso8601 timestamp to constraint the start time of the data (inclusive) (eg., '2020-01-04')",
        callback=lambda ctx, param, value: validate_date_string(value),
    )(function)

    function = click.option(
        "--end-time",
        type=str,
        default=None,
        help="Optional iso8601 timestamp to constraint the end time of the data (inclusive) (eg., '2020-01-04')",
        callback=lambda ctx, param, value: validate_date_string(value),
    )(function)
    return function
