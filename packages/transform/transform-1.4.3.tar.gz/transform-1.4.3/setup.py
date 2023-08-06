import re
from setuptools import find_packages, setup

# Read the version and package name from cli/__init__.py
# From https://gehrcke.de/2014/02/distributing-a-python-command-line-application/
# Your setup.py should not import your package for reading the version number.
# Instead, always read it directly. In this case, I used regular expressions for extracting it.
version = re.search('^__version__\\s*=\\s*"(.*)"', open("transform/__init__.py").read(), re.M)
PACKAGE_NAME = re.search('^PACKAGE_NAME\\s*=\\s*"(.*)"', open("transform/__init__.py").read(), re.M)
if not version or not PACKAGE_NAME:
    raise Exception("Failed to parse transform/__init__.py for version and package name.")

setup(
    name=PACKAGE_NAME.group(1),
    version=version.group(1),
    python_requires=">=3.8",
    author="Transform Data",
    author_email="marco@transformdata.io",
    description=("Transform MQL Client Library"),
    long_description="",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["mql = transform.cli.mql_cli:cli"]},
    py_modules=["mql_cli"],
    # Package details
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    # Dependencies
    setup_requires=["setupmeta"],
    install_requires=[
        "aiohttp",
        "gitpython>=3.1.27",
        "requests>=2.23.0",
        "pytest",
        "click>=8.1.3",
        "pyyaml",
        "update_checker",
        "tabulate",
        "pandas>=0.24.2,<1.5.0",
        "dataclasses",
        "halo>=0.0.31",
        "validators",
        "transform_tools>=1.1.0",
        "arrow",
        "log_symbols>=0.0.14",
        "requests-toolbelt",
        "gql",
        "rich>=9.10.0",
        "shellingham",
        "metricflow-lite>=0.130.1",
    ],
    extras_require={
        "dbt-snowflake": ["dbt-snowflake"],
        "dbt-redshift": ["dbt-redshift"],
        "dbt-postgres": ["dbt-postgres"],
        "dbt-bigquery": ["dbt-bigquery"],
    },
)
