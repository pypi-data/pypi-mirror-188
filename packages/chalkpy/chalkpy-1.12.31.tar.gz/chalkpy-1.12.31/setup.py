import re
from codecs import open
from os import path
from typing import List

import pkg_resources
from setuptools import find_packages, setup


def read(name: str) -> str:
    repo_root = path.abspath(path.dirname(__file__))
    with open(path.join(repo_root, name)) as f:
        return f.read()


def read_requirements(name: str) -> List[str]:
    return [str(r) for r in pkg_resources.parse_requirements(read(name))]


def get_version() -> str:
    version_file = "chalk/_version.py"
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", read(version_file), re.M)
    assert match is not None, f"Unable to find version string in {version_file}"
    return match.group(1)


extras_require = {
    "base": [],
    "bigquery": ["sqlalchemy-bigquery>=1.5.0,<1.6"],
    "dev": read_requirements("requirements-dev.txt"),
    "postgresql": ["psycopg2>=2.9.4,<3"],
    "polars": ["polars[timezone]==0.15.14"],
    "snowflake": [
        "snowflake-connector-python>=2.8.0,<3",
        "snowflake-sqlalchemy>=1.4.2,<1.5",
    ],
    "sqlite": [],  # Deprecated; here for backwards compatibility
    "redshift": [
        "sqlalchemy-redshift>=0.8.11,<0.9",
        "redshift_connector>=2.0.909,<2.1",
    ],
    "mysql": ["pymysql>=1.0.2,<2"],
    "sql": ["duckdb==0.6.0", "sqlglot>=10.5.2,<10.6"],
}
# Excluding dev requirements from "all" so they are not included for userland installs of chalkpy[all]
extras_require["all"] = [dep for (key, group_deps) in extras_require.items() for dep in group_deps if key != "dev"]

if __name__ == "__main__":
    setup(
        version=get_version(),
        name="chalkpy",
        author="Chalk AI, Inc.",
        description="Python SDK for Chalk",
        long_description=read("README.md"),
        long_description_content_type="text/markdown",
        python_requires=">=3.8.0",
        url="https://chalk.ai",
        packages=find_packages(exclude=("tests.*",)),
        install_requires=read_requirements("requirements.txt"),
        extras_require=extras_require,
        include_package_data=True,
        package_data={"chalk": ["py.typed"]},
        classifiers=[
            # Trove classifiers
            # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Software Development :: Code Generators",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        entry_points={"console_scripts": [f"chalkpy=chalk.cli:cli"]},
        setup_requires=[
            "setuptools_scm",
        ],
    )
