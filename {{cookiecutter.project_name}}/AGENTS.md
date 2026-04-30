# AGENTS.md

## AI Code Assistant Guidelines for This Project

This project was created using the 
[Cookiecutter-Spatial-Data-Science](https://github.com/esri/cookiecutter-spatial-data-science) template, 
which is designed to streamline and promote best practices for projects combining Geography and Data Science. 
It provides a logical, reasonably standardized, and flexible project structure.

You are an AI code assistant designed to help generate and edit code for this project. Your role is to 
assist in writing clean, efficient, and well-documented code that adheres to the project's standards and 
conventions.

---

## Table of Contents

- [TL;DR — Quick Reference for Agents](#tldr--quick-reference-for-agents)
- [Project Context](#project-context)
- [Coding Standards and Conventions](#coding-standards-and-conventions)
    - [1. Coding Standards](#1-coding-standards)
    - [2. Docstring Example](#2-docstring-example)
    - [3. Markdown Conventions](#3-markdown-conventions)
    - [4. Project Structure](#4-project-structure)
    - [5. Configuration](#5-configuration)
    - [6. Dependency Management](#6-dependency-management)
    - [7. Spatial Data Science Best Practices](#7-spatial-data-science-best-practices)
    - [8. Testing Conventions](#8-testing-conventions)
    - [9. Makefile Commands and Quick Cheat Sheet](#9-makefile-commands-and-quick-cheat-sheet)
    - [10. AI Assistant Usage Guidelines](#10-ai-assistant-usage-guidelines)
    - [11. Documentation Best Practices](#11-documentation-best-practices)
    - [12. Logging Best Practices](#12-logging-best-practices)
    - [13. Notebook Hygiene](#13-notebook-hygiene)

---

## TL;DR — Quick Reference for Agents

The rules most often violated. The full rationale is below.

- **Style**: PEP 8, 4-space indent, type hints on every function/method, Google-style docstrings.
- **Paths**: Use `pathlib.Path`, never `os.path` or string concatenation.
- **Logging**: Use a module-level `logger` from `get_logger(__name__, ...)`. No `print()` outside script entry points.
- **Config**: Read settings via `config.*` and `secrets.*` singletons. Never hardcode paths, WKIDs, or credentials.
- **Secrets**: Never commit `config/secrets.yml`. Add new keys to `secrets_template.yml` too.
- **Data**: `data/raw/` is read-only. Write outputs to `data/interim/` or `data/processed/`.
- **ArcPy**: Call as `arcpy.toolbox.Toolname(...)` with named parameters. Use `with_temp_fgdb` for large intermediates.
- **SQL/DuckDB**: Externalise non-trivial queries to `src/{{cookiecutter.support_library}}/sql/*.sql`. Always use bind parameters — never f-string interpolation.
- **Tests**: Mirror `src/` layout in `testing/`. One behavior per test. Use fixtures from `conftest.py`.
- **Scope**: Don't refactor unrelated code. Don't rename or change signatures of public symbols without approval.
- **Dependencies**: Don't add packages to `pyproject.toml` or `environment.yml` without flagging the addition.

---

## Project Context

When working in this project:

- The primary Python package is `{{cookiecutter.support_library}}`, located in `src/{{cookiecutter.support_library}}/`
- ArcGIS Pro toolboxes are in `arcgis/` and reference `{{cookiecutter.support_library}}` for shared logic
- Tests live in `testing/` and follow the naming convention `test_*.py`
- Configuration is loaded from `config/config.yml`; secrets belong in `config/secrets.yml` (gitignored)

---

## Coding Standards and Conventions

Please follow these standards and conventions when generating or editing code:

<!-- copilot:instruction name="python-style" applyTo="**/*.py,**/*.pyt" -->

### 1. Coding Standards

- **PEP 8**: All Python code must comply with [PEP 8](https://peps.python.org/pep-0008/).
- **Formatting**: Code is formatted with `black` (line length 100). Run `black src testing scripts`
  before committing.
- **Type Hints**: All functions and class methods must include explicit type hints for arguments
  and return values. Style decisions for this project:
    - Add `from __future__ import annotations` at the top of every module so annotations are
      evaluated lazily as strings.
    - Use PEP 604 union syntax: `int | None`, not `Optional[int]` or `Union[int, None]`.
    - Use built-in generics: `list[str]`, `dict[str, int]`, not `List[str]` / `Dict[str, int]`.
    - For ArcPy paths, annotate as `str | os.PathLike[str]` when both are accepted, else `str`.
- **Docstrings**: Use [Google-style](https://google.github.io/styleguide/pyguide.html) docstrings
  with `Args:`, and `Returns:` / `Raises:` sections when applicable. See §2 for an example and
  §3 for admonition syntax used inside docstrings.
- **Code samples in docstrings**: Do not use the `Example:` section header. Use a fenced code
  block with the `python` language tag instead.

### 2. Docstring Example

```python
variable: str = "This is a variable with a docstring example."
"""This variable is an example of how to include a docstring for a variable."""

def example_function(param1: int, param2: str) -> bool:
    """
    Brief description of what the function does.

    !!! note
        Additional notes about the function.

    ??? note "Collapsible Note with Title"
        This is a collapsible note section using a custom title.

    !!! warning
        Warnings about the function usage.

    ```python
    result = example_function(10, "test")
    print(result)
    ```
    
    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        bool: Description of the return value.
    """
    ...
```

<!-- /copilot:instruction -->

<!-- copilot:instruction name="markdown" applyTo="**/*.md" -->

### 3. Markdown Conventions

- **Headings**: Use ATX-style headers (`#`, `##`, `###`, etc.)
- **Lists**:
    - Use hyphens (`-`) for unordered lists
    - Use numbers for ordered lists
    - Ensure there is a line preceding lists so they are formatted correctly for MkDocs
- **Emphasis**: Use `*italic*` for emphasis and `**bold**` for strong emphasis
- **Indentation**: Use four spaces for indentation/tabs (not tab characters)
- **Code**:
    - Use single backticks for inline code: `` `variable_name` ``
    - Use triple backticks with language identifiers for code blocks
    - When including code in docstrings, use triple backticks with the language identifier 
      (e.g., `` ```python ``)
- **Links**: Use descriptive link text: `[link text](URL)`
- **Admonitions**: Use MkDocs-style admonitions in documentation and docstrings:
    - `!!! note` for general information
    - `!!! warning` for important warnings
    - `!!! tip` for helpful tips
    - `!!! danger` for critical warnings
    - `!!! example` for examples
    - **Collapsible Admonitions**: Use `???` instead of `!!!` to make admonitions collapsible by default
    - Use `???+` to make collapsible admonitions expanded by default
- **Tables**: Use pipe-delimited tables with header separators (`|---|---|`)
- **Line Length**: Keep markdown lines under 120 characters when possible for readability
- Follow style guidance and conventions from the
  [MkDocs Material documentation](https://squidfunk.github.io/mkdocs-material/) as the primary
  reference. For anything not covered there, fall back to the
  [MkDocs documentation](https://www.mkdocs.org/user-guide/writing-your-docs/).

<!-- /copilot:instruction -->

### 4. Project Structure

This project follows the Cookiecutter-Spatial-Data-Science structure:



- **`src/{{cookiecutter.support_library}}/`** - Main source code for the project package
    - **`src/{{cookiecutter.support_library}}/sql/`** - Externalised SQL queries (`*.sql`) used
      by the package, typically with DuckDB. See §7.6.
- **`config/`** - Configuration files; `config.yml` for settings, `secrets.yml` for credentials
    - Any credentials or sensitive information should be stored in `config/secrets.yml`
      (not committed to version control — copy from `secrets_template.yml`)
- **`scripts/`** - Standalone automation scripts for data processing, toolbox creation, etc.
- **`data/`** - Data files (raw, processed, external, interim)
- **`notebooks/`** - Jupyter notebooks for exploratory analysis
- **`arcgis/`** - ArcGIS Pro project files, Python toolboxes (*.pyt), and layer files
- **`testing/`** - PyTest test files
- **`docsrc/`** - MkDocs documentation source files
- **`reports/`** - Generated reports, figures, and logs
- **`models/`** - Trained models and model metadata (*.emd files)

### 5. Configuration

Project configuration is split across two YAML files and loaded via
`src/{{cookiecutter.support_library}}/config.py`, which exposes a singleton `ConfigNode` supporting
both dot-notation and dict-style access.

#### 5.1 Files

| File | Purpose | Committed? |
|---|---|---|
| `config/config.yml` | Non-sensitive project settings (paths, log levels, env overrides) | Yes |
| `config/secrets_template.yml` | Template showing the shape of secrets — no real values | Yes |
| `config/secrets.yml` | Your actual credentials — copy from `secrets_template.yml` and fill in | **No** (gitignored) |

#### 5.2 Accessing configuration in code

Import the pre-built singletons from `{{cookiecutter.support_library}}.config`:

```python
from {{cookiecutter.support_library}}.config import config, secrets, ENVIRONMENT

# Dot-notation access
log_level = config.logging.level

# Dict-style access
input_path = config["data"]["input"]

# Secrets
gis_url = secrets.esri.gis_url
gis_profile = secrets.esri.gis_profile

# Check active environment (dev / test / prod)
print(f"Running in {ENVIRONMENT} mode")
```

The active environment is controlled by the `PROJECT_ENV` environment variable (defaults to
`"dev"`). Settings under `environments.<env>` in `config.yml` are merged on top of
`environments.default` (if present), which is itself merged on top of any top-level keys.
The full merge order is: **top-level keys → `default` → active environment**.

#### 5.3 Switching environments

```bash
# Windows PowerShell
$env:PROJECT_ENV = "prod"

# macOS / Linux
export PROJECT_ENV=prod
```

Alternatively, change the `ENVIRONMENT` default directly in
`src/{{cookiecutter.support_library}}/config.py` for a persistent local override.

#### 5.4 Adding new configuration values

1. **Shared across all environments** — add the key/value under `environments.default` in
   `config/config.yml`. Every environment that does not explicitly override the key will inherit
   this value automatically.
2. **Environment-specific** — add the key/value only under the relevant environment block(s)
   (e.g. `environments.prod`). Any environment that omits the key falls back to the `default`
   value (or is absent if there is no default).
3. Access it in code via dot- or dict-notation — no Python changes to `config.py` are needed.
4. Never put credentials or API keys in `config.yml`; use `config/secrets.yml` instead.

#### 5.5 `secrets.yml` pattern

Copy `secrets_template.yml` to `secrets.yml` and fill in real values:

```yaml
esri:
  gis_url: "https://your-org.maps.arcgis.com"
  gis_profile: "your_profile_name"
```

In code use `secrets.esri.gis_url` etc. — the `secrets` object is a `ConfigNode` loaded from
this file. Add new top-level keys to both `secrets_template.yml` (with placeholder values) and
your local `secrets.yml` (with real values).

### 6. Dependency Management

This project uses two complementary files to manage dependencies. Keep them in sync when adding
or removing packages.

#### 6.1 `pyproject.toml` — Runtime dependencies

`pyproject.toml` declares the packages that **`{{cookiecutter.support_library}}` itself requires to
run**. Add a dependency here when:

- A module inside `src/{{cookiecutter.support_library}}/` contains a top-level `import` of that package
- The package must be present for the installed library to function correctly

```toml
[project]
dependencies = [
    "some-package>=1.0",
]
```

> **Note:** Do **not** add `arcpy` here. ArcPy is provided implicitly by the ArcGIS Pro
> conda environment and cannot be installed via pip or conda in the normal way.

#### 6.2 `environment.yml` — Development environment

`environment.yml` defines the full **conda environment** used for development, testing, and
documentation. Add a package here when it is needed for any of the following, but is *not* a
runtime dependency of `{{cookiecutter.support_library}}`:

- **Development tooling**: `black`, `pytest`, `jupyterlab`, `jupyterlab_code_formatter`
- **Documentation**: `mkdocs`, `mkdocs-material`, `mkdocstrings[python]`, `mkdocs-jupyter`, etc.
- **Data science / analysis**: `scipy`, `scikit-learn`, `h3-py`, `tqdm`, etc.
- **Build / release tooling**: `bump-my-version` (the maintained successor to `bump2version`)

Prefer `conda-forge` or `esri` channels for conda packages. Use the `pip:` block inside
`environment.yml` for packages that are only available on PyPI (e.g., the MkDocs plugins).

> **Note:** ArcPy is also **not** listed in `environment.yml`; it is pre-installed in the
> ArcGIS Pro conda base environment and inherited automatically.

#### 6.3 Decision guide

| Scenario | Add to |
|---|---|
| `import foo` inside `src/{{cookiecutter.support_library}}/` | `pyproject.toml` `[project] dependencies` |
| MkDocs plugin or theme | `environment.yml` pip block |
| Test-only package (`pytest-*`, `pytest-mock`) | `environment.yml` conda/pip block |
| JupyterLab extension or kernel | `environment.yml` conda block |
| Conda-distributed data science library | `environment.yml` conda block |
| ArcPy or any `arcpy.*` import | Neither — provided by ArcGIS Pro |

### 7. Spatial Data Science Best Practices

#### 7.1 General Code Quality

- Prefer clear, descriptive variable and function names over abbreviations or single letters
- Avoid global variables; pass dependencies explicitly as parameters
- Keep functions small and focused on a single responsibility; prefer composing small functions
  over large multi-step ones
- Use comments to explain *why* code does something, not *what* it does; favour self-documenting
  names and structure first
- Avoid hardcoding values; use `config` or environment variables (see §4)
- Use `pathlib.Path` instead of `os.path` or manual string manipulation for all file paths
- Use logging rather than `print()`; follow the patterns in §12
- Handle exceptions using the build-message → log → raise pattern described in §12.5
- Write tests for new functionality following the conventions in §8

#### 7.2 ArcPy Performance

<!-- copilot:instruction name="arcpy" applyTo="**/*.pyt,arcgis/**/*.py,src/**/*.py,scripts/**/*.py" -->

- Prefer `arcpy.da.UpdateCursor` over older cursor methods for better performance
- Use generator expressions to feed values into cursors when possible
- Always clean up cursors using `with` statements, `del` statements, or as context managers
- When calling arcpy tools, use the convention `arcpy.toolbox.Toolname` instead of 
  `arcpy.Toolname_toolbox`, and use named parameters for clarity and forward compatibility

#### 7.3 Intermediate Data Management

**For small datasets (< tens of thousands of features)**:

- Use the `memory` workspace for intermediate outputs: `memory/datasetname`
- Provides fastest performance for small to moderate datasets
- No cleanup required as data is automatically released

**For large datasets (≥ tens of thousands of features)**:

- Use the `@with_temp_fgdb` decorator from `{{cookiecutter.support_library}}.utils` —
  implemented in `src/{{cookiecutter.support_library}}/utils/_data.py` and included by default
  in generated projects
- Automatically sets `arcpy.env.workspace` to a temporary file geodatabase for the duration of
  the function, then deletes all intermediate data and the workspace on exit (even on error)
- Prevents memory issues with large intermediate datasets

```python
from {{cookiecutter.support_library}}.utils import with_temp_fgdb
from pathlib import Path

@with_temp_fgdb
def process_large_dataset(
    input_fc: str,
    clip_boundary: str,
    output_fc: str,
    temp_fgdb: str = None,
) -> str:
    """
    Process a large dataset using a temporary file geodatabase.

    Args:
        input_fc: Path to input feature class.
        clip_boundary: Path to feature class used to clip the buffered output.
        output_fc: Path to output feature class.
        temp_fgdb: Temporary file geodatabase path (injected by decorator).

    Returns:
        str: Path to the output feature class.
    """
    # Use temp_fgdb for intermediate outputs
    intermediate_fc = str(Path(temp_fgdb) / "intermediate")
    arcpy.analysis.Buffer(
        in_features=input_fc,
        out_feature_class=intermediate_fc,
        buffer_distance_or_field="100 METERS"
    )
    arcpy.analysis.Clip(
        in_features=intermediate_fc,
        clip_features=clip_boundary,
        out_feature_class=output_fc
    )
    return output_fc
```

<!-- /copilot:instruction -->

#### 7.4 Data Processing Best Practices

- Prefer `pandas`, `numpy`, and `scikit-learn` for tabular data manipulation; use the
  [Spatially Enabled DataFrame](https://developers.arcgis.com/python/latest/guide/introduction-to-the-spatially-enabled-dataframe/)
  (`arcgis.GeoAccessor` / `arcgis.GeoSeriesAccessor`) for spatial DataFrame operations —
  access it via `df.spatial` after importing `arcgis.features`. If spatial operation is
  not available, or does not work, in the current environment, which can be the case in 
  non-ArcGIS Pro environments or when the ArcGIS API for Python is not installed, use
  [GeoPandas](https://geopandas.org/) as a fallback for spatial operations. If using 
  GeoPandas, ensure that your data is in a GeoDataFrame and that the coordinate reference 
  system (CRS) is correctly set.
- Use vectorized operations in pandas and NumPy rather than row-wise iteration (`apply`,
  `iterrows`); reach for NumPy ufuncs or pandas built-ins first
- Avoid mutating DataFrame slices — pandas 2.x Copy-on-Write (CoW) makes in-place slice
  mutation a no-op; always assign back to the original or use `.loc`/`.iloc`
- Use appropriate dtypes to reduce memory consumption: `int32`/`float32` where precision
  allows, and `pd.Categorical` for low-cardinality string columns
- Prefer columnar file formats (GeoParquet and Parquet) over CSV for intermediate tabular data:
  faster I/O, smaller files, and dtypes are preserved across read/write cycles. If the data
  is spatial, use GeoParquet to preserve geometry and CRS information without needing separate 
  sidecar files.
- Use [DuckDB](https://duckdb.org/docs/stable/) with the [Spatial Extension](https://duckdb.org/docs/extensions/spatial) 
  for large-dataset filtering, aggregation, and multi-table joins where pandas performance
  is insufficient; DuckDB can query Parquet files directly without loading them into memory
- For data being loaded and repeatedly queried in-memory, use DuckDB's Python API to create 
  an in-memory database and load the data into DuckDB tables for efficient querying and 
  transformation
- For files too large to load in full, use DuckDB's lazy query evaluation
- Use list/generator expressions for simple single-condition transformations; if an
  expression requires nested logic or more than one condition, extract a named function

#### 7.5 Coordinate Reference Systems (CRS)

<!-- copilot:instruction name="crs" applyTo="**/*.py,**/*.pyt" -->

Spatial bugs caused by mismatched or assumed CRS are among the most common — and most expensive
— errors in spatial workflows. Treat CRS as a first-class concern.

- **Never hardcode WKIDs / EPSG codes** in code. Define them in `config.yml` (e.g.
  `spatial.crs_working`, `spatial.crs_storage`, `spatial.crs_display`) and read via
  `config.spatial.crs_working`.
- **Validate CRS on every input** at the start of any function that consumes spatial data.
  If the input lacks a CRS, raise rather than guessing.
- **Reproject explicitly**, never implicitly. Document the target CRS in the function
  docstring and log the source → target transformation.
- **Project before measuring**. Area, length, and distance calculations must be performed
  in a projected CRS appropriate for the area of interest, not in geographic coordinates
  (e.g. WGS 84 / EPSG:4326).
- **GeoPandas**: use `gdf.to_crs(epsg=...)` and check `gdf.crs is not None` before any
  geometric operation. Do not use `gdf.set_crs(...)` to "fix" data with an unknown CRS.
- **ArcPy**: use `arcpy.management.Project` (not `Define Projection`) to actually transform
  coordinates. `Define Projection` only updates metadata and silently corrupts data when
  misused.
- **DuckDB**: use `ST_Transform(geometry, target_srid)` to reproject geometries to the CRS 
  defined in the configuration in SQL queries.

<!-- /copilot:instruction -->

#### 7.6 SQL and DuckDB Query Organization

<!-- copilot:instruction name="sql" applyTo="src/**/*.py,scripts/**/*.py,src/**/sql/*.sql" -->

Externalise non-trivial SQL into discrete `.sql` files under
`src/{{cookiecutter.support_library}}/sql/`. This is a widely adopted best practice because it:

- Enables full SQL syntax highlighting, formatting, and linting in VS Code (e.g. the
  *SQLTools* and *SQLFluff* extensions) — features that do not work on SQL embedded in Python
  string literals.
- Produces clean, reviewable diffs for long queries.
- Eliminates Python-string escaping issues (quotes, backslashes, f-string `{}` collisions).
- Encourages parameterized queries (`$name`, `?`) over string interpolation, sidestepping
  SQL injection.
- Allows the same query to be reused by Python, notebooks, dbt, or a CLI.

**When to inline vs. externalise:**

- **Inline**: short ad-hoc queries (≤ ~10 lines) with no user-supplied input.
- **Externalise**: anything multi-statement, multi-CTE, longer than ~10 lines, parameterized,
  or reused in more than one place.

**File layout:**

```
src/{{cookiecutter.support_library}}/
    sql/
        __init__.py              # exposes load_sql() helper
        h3_aggregate.sql
        nearest_poi.sql
        load_parquet_partitioned.sql
```

**Naming:** `snake_case.sql`, named after the operation (`build_index.sql`,
`spatial_join_blocks.sql`), not the table.

**Loading and executing** (canonical pattern — `load_sql()` is shipped with the package):

```python
import duckdb
from {{cookiecutter.support_library}}.sql import load_sql

con = duckdb.connect()
result = con.execute(
    load_sql("nearest_poi"),
    {"max_distance_m": 1500, "category": "grocery"},
).fetch_df()
```

**Always parameterise**. Use DuckDB's named-parameter form (`$max_distance_m`) and pass a
dict to `execute()`. Never `f"... WHERE category = '{category}'"`-style interpolation, even
for "internal" inputs.

**For values that cannot be bound** (table or column names, file paths in `read_parquet(...)`),
validate them against an allow-list before substituting via Python `str.format` or Jinja.

**Configuration over hardcoding**: paths to Parquet datasets, working CRS WKIDs, and
H3 resolutions belong in `config.yml` (see §5) and should be passed in as bind parameters,
not baked into the `.sql` file.

<!-- /copilot:instruction -->

### 8. Testing Conventions

<!-- copilot:instruction name="testing" applyTo="testing/**/*.py" -->

The project uses **PyTest** as the testing framework. Follow PyTest conventions when writing and
organizing tests. Run the full test suite at any time with `make test`.

#### 8.1 File and Module Organization

- Mirror the `src/{{cookiecutter.support_library}}/` package structure in `testing/`:
    - One test file per module: `testing/test_<module_name>.py`
    - Example: `src/{{cookiecutter.support_library}}/analysis.py` → `testing/test_analysis.py`
- Use `testing/test_{{cookiecutter.support_library}}.py` for package-level smoke tests
- Do not place test files inside `src/`

#### 8.2 Naming Conventions

- **Test files**: `test_*.py`
- **Test functions**: `test_<what_is_being_tested>()` — names should read like a sentence
    - Good: `test_buffer_returns_expected_area()`
    - Avoid: `test1()`, `test_thing()`
- **Test classes** (when grouping related tests): `Test<ClassName>` with no `__init__`
- **Fixtures**: descriptive lowercase names (e.g., `temp_gdb`, `sample_feature_class`)

#### 8.3 Fixtures

- Place **reusable fixtures** in `testing/conftest.py` — PyTest discovers them automatically for
  all test files without explicit imports
- The following fixtures are pre-defined in `conftest.py`:
    - `temp_dir` — provides a temporary `Path` directory; deleted after each test
    - `temp_gdb` — provides a temporary ArcGIS file geodatabase `Path`; deleted after each test
    - `setup_environment` — session-scoped; sets `TEST_ENV=true` for the full test session
- Use the **narrowest scope possible**: prefer `scope="function"` (default) unless the setup cost
  justifies `scope="module"` or `scope="session"`
- Parametrize repetitive test cases with `@pytest.mark.parametrize` rather than writing duplicate
  test functions

#### 8.4 Test Writing Guidelines

- Each test must be **independent and isolated** — tests must not depend on execution order or
  shared mutable state
- Use plain `assert` statements; PyTest rewrites them to provide detailed failure output
- Test **one behavior per function**; keep tests small and focused
- Avoid testing third-party libraries (arcpy, pandas, etc.) — only test project code
- For ArcPy-dependent tests, use the `temp_gdb` fixture for all intermediate and output data
- Mock external calls and expensive operations using `unittest.mock` or `pytest-mock`
- Prefer `monkeypatch` over module-level patching to keep side-effects scoped to the test
- Do not use `print()` in tests; use `pytest`'s captured output or logging assertions instead

#### 8.5 Running Tests

- Run all tests: `make test`
- Run a single file: `pytest testing/test_<module>.py`
- Run a single test by name: `pytest testing/test_<module>.py::test_function_name`
- Run with verbose output: `pytest -v`
- Run with coverage (if `pytest-cov` is installed):
  `pytest --cov={{cookiecutter.support_library}} --cov-report=term-missing`

<!-- /copilot:instruction -->

---

### 9. Makefile Commands and Quick Cheat Sheet

Frequently used one-liners (run from the project root, conda env activated):

```bash
# Tests
pytest                                              # full suite
pytest testing/test_<module>.py::test_func -xvs     # one test, verbose, stop on first fail

# Format / style
black src testing scripts

# Docs (live preview at http://localhost:8000)
mkdocs serve -f docsrc/mkdocs.yml

# Run the project's data pipeline
python scripts/make_data.py
```


This project includes a `Makefile` (and `make.cmd` for Windows) with common commands:

- `make env` - Set up the Conda environment with all dependencies
- `make data` - Run the data pipeline (`./scripts/make_data.py`)
- `make pytzip` - Create a distributable zipped archive of the Python toolbox
- `make docserve` - Run live MkDocs documentation server (http://localhost:8000)
- `make docs` - Build the documentation
- `make test` - Run all tests using PyTest
- `make jupyter` - Run Jupyter notebook with options enabling remote connections

!!! note
    These commands are defined in `./make.cmd` (Windows) and `./Makefile` (*nix) if you want to 
    examine, modify or extend this capability.

### 10. AI Assistant Usage Guidelines

#### 10.1 Code Changes — Conservative by Default

- **Before creating**: Always check for existing functions/classes before creating new ones; prefer
  modifying an existing function over creating a new one
- **When editing**: Preserve existing logic unless explicitly instructed to refactor; do not
  "clean up" surrounding code opportunistically
- **Public API**: Do not rename public symbols (functions, classes, module-level constants) without
  explicit instruction — callers outside this repo may depend on them
- **Signatures**: Do not change a function's signature (add/remove/reorder parameters) unless
  asked; if a signature change is necessary, flag it and confirm before proceeding
- **Removing code**: Do not delete code unless the request requires it. If you find code that
  appears unused, flag it in your response — do not remove it silently and do not leave it
  commented out in the file. Never commit commented-out code; if a block must be temporarily
  disabled, leave a `# TODO(<reason>):` comment with an issue link.

#### 10.2 Data Safety

- **Data files are read-only**: Never delete, overwrite, or truncate files under `data/` unless
  the task is explicitly a data pipeline step
- **Output directories**: Never write output to `data/raw/`; processed results go to
  `data/interim/` or `data/processed/`
- **Output paths**: Always derive output file paths from `config` values rather than hardcoding
  them in code

#### 10.3 Scope Discipline

- **Stay on task**: Limit changes to the files and functions directly relevant to the request
- **Dependencies**: Do not add packages to `pyproject.toml` or `environment.yml` without flagging
  the addition — new dependencies need review
- **Pinned versions**: Do not upgrade pinned dependency versions as a side effect of other changes

#### 10.4 Uncertainty and Ambiguity

- **Understand before changing**: If the intent of existing code is unclear, read related tests and
  docstrings before making assumptions
- **State your interpretation**: If a request is ambiguous or could break existing behavior,
  describe your interpretation and the trade-offs before writing code
- **Breaking changes**: If a task requires altering the public API or removing functionality,
  pause and confirm rather than proceeding silently

#### 10.5 ArcGIS / Spatial Specifics

- **Source data**: Do not call `arcpy` functions that modify a source geodatabase without
  confirming the target is a copy or a test fixture
- **Spatial references**: Avoid hardcoding spatial reference WKIDs; read them from `config` or
  accept them as parameters

#### 10.6 General

- **When adding files**: Update relevant documentation and tests
- **Version control**: Never commit sensitive information (credentials, API keys) to version control
- **Testing**: Write tests for new functionality in the `testing/` directory
- **Documentation**: Update MkDocs documentation in `docsrc/` when adding significant features

#### 10.7 Version Control Conventions

- **Commit messages**: Use [Conventional Commits](https://www.conventionalcommits.org/) — e.g.
  `feat(analysis): add buffer-and-clip helper`, `fix(config): handle missing secrets.yml`,
  `docs(readme): clarify env setup`. Subject line under 72 characters, imperative mood.
- **One logical change per commit**. Do not bundle unrelated edits.
- **Branches**: `feature/<short-description>`, `fix/<short-description>`, `docs/<short-description>`.
- **Do not push or force-push** without explicit instruction. Do not amend commits already pushed.
- **Never commit** `config/secrets.yml`, `data/` contents, large binaries, or notebook outputs
  containing sensitive data.

### 11. Documentation Best Practices

- Use **MkDocs** with the Material theme for all documentation
- Place documentation files in `./docsrc/mkdocs/`
- Update `./docsrc/mkdocs.yml` to include new pages in the table of contents
- Use **MkDocStrings** to auto-generate API documentation from Python docstrings
- Move Jupyter Notebooks you want in documentation to `./docsrc/mkdocs/notebooks/`
- Use admonitions (`!!! note`, `!!! warning`, etc.) to highlight important information
- Keep documentation up-to-date with code changes

### 12. Logging Best Practices

<!-- copilot:instruction name="logging" applyTo="src/**/*.py,scripts/**/*.py,**/*.pyt" -->

#### 12.1 `get_logger`

`get_logger` is a project-defined utility implemented in
`src/{{cookiecutter.support_library}}/utils/_logging.py` and included by default in generated
projects. It returns a configured `logging.Logger` that routes messages to the console, a logfile,
and/or ArcPy messaging (`arcpy.AddMessage` / `AddWarning` / `AddError`) depending on the options
provided.

#### 12.2 Module-level loggers

Every module in `src/{{cookiecutter.support_library}}/` should configure a logger at the top of
the file. Use `__name__` as the logger name so log output identifies the originating module:

```python
from {{cookiecutter.support_library}}.utils import get_logger

logger = get_logger(__name__, level='DEBUG', add_stream_handler=False)
```

- Set `level='DEBUG'` in modules so all messages are captured; the effective output level is
  controlled by the root logger configured in scripts
- Set `add_stream_handler=False` in modules to avoid duplicate console output

#### 12.3 Script-level (root) logger

Scripts in `scripts/` configure the root logger once at the entry point, which applies to all
module-level loggers via propagation:

```python
import datetime
from pathlib import Path
from {{cookiecutter.support_library}}.utils import get_logger

script_pth = Path(__file__)
dir_logs = script_pth.parent.parent / 'reports' / 'logs'
dir_logs.mkdir(parents=True, exist_ok=True)

logfile_path = dir_logs / f'{script_pth.stem}_{datetime.datetime.now().strftime("%Y%m%dT%H%M%S")}.log'

logger = get_logger(level='INFO', add_stream_handler=True, logfile_path=logfile_path)
```

#### 12.4 Log level guidance

Use log levels consistently and frequently throughout the codebase:

| Level | When to use |
|---|---|
| `DEBUG` | Detailed diagnostic info useful when troubleshooting: variable values, loop counts, intermediate results |
| `INFO` | Normal progress milestones: function entry/exit, key steps completed, record counts |
| `WARNING` | Unexpected but recoverable conditions: missing optional data, fallback behaviour triggered |
| `ERROR` | A specific operation failed and could not complete, but execution can continue |
| `CRITICAL` | A severe failure that will prevent the program from continuing |

Prefer **too many** log messages over too few. A well-logged spatial workflow should let a
developer diagnose a failure from the logfile alone, without needing to reproduce it interactively.

#### 12.5 Logging in `try`/`except` blocks

When catching exceptions, always:

1. Build the error message as a variable
2. Log it at the appropriate level before raising
3. Raise the exception with the message so the caller and any outer handlers see the same text

```python
# ERROR — a specific operation failed; execution may continue in the caller
try:
    result = arcpy.analysis.Buffer(input_fc, output_fc, "100 METERS")
    logger.debug(f"Buffer completed: {output_fc}")
except Exception as e:
    msg = f"Buffer failed for '{input_fc}': {e}"
    logger.error(msg)
    raise RuntimeError(msg) from e
```

```python
# WARNING — unexpected but handled; execution continues normally
try:
    gis = GIS(profile=secrets.esri.gis_profile)
    logger.info(f"Connected to GIS: {gis.url}")
except Exception as e:
    msg = f"Could not connect to GIS profile '{secrets.esri.gis_profile}', continuing offline: {e}"
    logger.warning(msg)
    gis = None
```

```python
# CRITICAL — unrecoverable; program cannot continue
try:
    config_path = PROJECT_ROOT / "config" / "config.yml"
    with open(config_path) as f:
        raw = yaml.safe_load(f)
except FileNotFoundError as e:
    msg = f"Configuration file not found at '{config_path}': {e}"
    logger.critical(msg)
    raise FileNotFoundError(msg) from e
```

#### 12.6 ArcPy toolbox logging

When writing Python toolbox tools (`.pyt`), pass `add_arcpy_handler=True` so messages appear
in the ArcGIS Pro geoprocessing pane and results window:

```python
logger = get_logger(__name__, level='INFO', add_arcpy_handler=True)
```

<!-- /copilot:instruction -->

---

### 13. Notebook Hygiene

<!-- copilot:instruction name="notebooks" applyTo="**/*.ipynb,notebooks/**" -->

Notebooks under `notebooks/` are for exploratory work. Apply these rules to keep them
reviewable and free of stale artifacts:

- **Strip outputs before committing.** Install [`nbstripout`](https://github.com/kynan/nbstripout)
  as a Git filter (`nbstripout --install`) so committed `.ipynb` files contain no cell outputs,
  execution counts, or metadata churn. Outputs bloat diffs and may leak data or credentials.
- **Restart-and-run-all** before committing. A notebook that does not run top-to-bottom in a
  fresh kernel is broken; do not commit it.
- **No secrets in notebooks.** Use `secrets.*` from `{{cookiecutter.support_library}}.config`
  rather than pasting tokens, profile names, or URLs into cells.
- **Promote reusable code out of notebooks.** Once a function works, move it into
  `src/{{cookiecutter.support_library}}/` and import it back into the notebook. Notebooks
  should orchestrate, not own logic.
- **Notebooks intended for documentation** belong under `docsrc/mkdocs/notebooks/` and are
  rendered by `mkdocs-jupyter`; keep their outputs (since they are the documentation) but
  still restart-and-run-all before committing.
- **Prefer JupyterLab via `make jupyter`** so the kernel matches the project conda env.

<!-- /copilot:instruction -->

---

For questions or clarifications, refer to the:

- Project [README.md](README.md)
- Project maintainers or team leads

---

## Editing this file

`AGENTS.md` is the **canonical source** of AI assistant guidance for this project. Other agent
configuration files are derived from it by the cookiecutter post-generation hook
(`hooks/post_gen_project.py`):

- `.github/copilot-instructions.md` — full copy for GitHub Copilot
- `.github/instructions/<name>.instructions.md` — per-context Copilot files generated from
  `<!-- copilot:instruction name="..." applyTo="..." -->` ... `<!-- /copilot:instruction -->`
  marker blocks in this file
- `CLAUDE.md` — full copy for Claude Code
- `.cursor/rules/instructions.mdc` — full copy for Cursor

Edit AGENTS.md, not the generated files. To add a new per-context Copilot instruction, wrap the
relevant section(s) in marker comments — the hook will pick them up the next time the template is
generated. The markers are HTML comments, so they are invisible in MkDocs and GitHub rendering.

_Last reviewed: 2026-04_

---

<details>
<summary>Template &amp; Cookiecutter Resources</summary>

#### This Project's Template

- **Cookiecutter-Spatial-Data-Science Repository**:
  [https://github.com/esri/cookiecutter-spatial-data-science](https://github.com/esri/cookiecutter-spatial-data-science)
- **Template Issues**:
  [https://github.com/esri/cookiecutter-spatial-data-science/issues](https://github.com/esri/cookiecutter-spatial-data-science/issues)
- **Contributing Guidelines**:
  [https://github.com/esri/contributing](https://github.com/esri/contributing)

#### Cookiecutter Core Documentation

- **Cookiecutter Documentation**:
  [https://cookiecutter.readthedocs.io/](https://cookiecutter.readthedocs.io/)
- **Cookiecutter GitHub**:
  [https://github.com/cookiecutter/cookiecutter](https://github.com/cookiecutter/cookiecutter)
- **Advanced Features**:
  [https://cookiecutter.readthedocs.io/en/stable/advanced/index.html](https://cookiecutter.readthedocs.io/en/stable/advanced/index.html)

</details>
