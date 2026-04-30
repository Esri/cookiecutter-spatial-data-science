# SQL Queries with DuckDB

Cookiecutter-Spatial-Data-Science encourages a particular pattern for SQL-heavy work,
particularly with [DuckDB](https://duckdb.org/): keep query text in discrete `.sql` files
inside a dedicated `sql/` sub-package, and load them at runtime with a small helper.

This page describes the rationale, the recommended layout, and the patterns for using
DuckDB's spatial extension — including in restricted-network and air-gapped environments.

!!! note "DuckDB ships with ArcGIS Pro"
    ArcGIS Pro's bundled Python environment includes the `duckdb` package out of the
    box, so projects can use DuckDB **in-place** alongside `arcpy` — no extra
    installation, no separate environment. Just `import duckdb` and go. The
    [spatial extension](#spatial-extension), however, is fetched on first use (see
    below).

## Why externalise SQL?

- **IDE support.** VS Code (and most editors) provide rich SQL syntax highlighting,
  formatting, and linting (e.g. *SQLTools*, *SQLFluff*) for `.sql` files. None of that
  works on SQL embedded inside a Python triple-quoted string.
- **Readable diffs.** Long, multi-CTE queries diff cleanly when they live on their own.
- **No escaping pain.** No quote-escaping, backslash gymnastics, or f-string `{}`
  collisions with SQL or Jinja syntax.
- **Encourages parameterisation.** Externalising naturally pushes you toward bind
  parameters (`$name`, `?`) rather than string interpolation — which sidesteps SQL
  injection entirely.
- **Reusable.** The same `.sql` file can be consumed by Python, a notebook, dbt, or a
  CLI without copy-paste.

## File layout

Add a `sql/` package under your project's source tree:

```text
src/myproject/
└── sql/
    ├── __init__.py        # exposes load_sql()
    ├── nearest_poi.sql
    └── h3_aggregate.sql
```

**Naming**: `snake_case.sql`, named after the *operation*
(`spatial_join_blocks.sql`, `build_h3_index.sql`), not the table.

## When to externalise vs. inline

| Inline (in Python) | Externalise (`.sql` file) |
|---|---|
| Short ad-hoc queries (≤ ~10 lines) | Multi-statement or multi-CTE queries |
| No user-supplied input | Anything parameterised |
| Used in exactly one place | Reused in more than one place |
| Trivial (`SELECT COUNT(*) FROM t`) | Anything you'd want to lint or format |

## A small `load_sql()` helper

A minimal helper that reads a `.sql` file from the `sql/` resource directory and caches
the result for the lifetime of the process:

```python
# src/myproject/sql/__init__.py
from __future__ import annotations

from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=None)
def load_sql(name: str) -> str:
    """Load a `.sql` file shipped inside this `sql/` resource directory.

    Pass the file *stem* (no `.sql` extension). Always pass user-supplied or
    runtime values via DuckDB bind parameters rather than interpolating them
    into the returned string.
    """
    resource = files(__name__).joinpath(f"{name}.sql")
    if not resource.is_file():
        raise FileNotFoundError(f"SQL resource '{name}.sql' not found.")
    return resource.read_text(encoding="utf-8")
```

Using it:

```python
import duckdb
from myproject.sql import load_sql

con = duckdb.connect()

df = con.execute(
    load_sql("nearest_poi"),
    {"max_distance_m": 1500, "category": "grocery"},
).fetch_df()
```

!!! note
    `importlib.resources.files()` works correctly whether the package is installed
    editable (`pip install -e .`), installed normally, or executed from inside a wheel.

## Always parameterise

Use DuckDB's named-parameter syntax (`$name`) and pass a `dict` to `execute()`. The
DuckDB driver handles type conversion and quoting safely.

```sql
-- src/myproject/sql/nearest_poi.sql
SELECT
    poi_id,
    ST_Distance(origin_geom, poi_geom) AS distance_m
FROM
    pois
WHERE
    category = $category
    AND ST_Distance(origin_geom, poi_geom) <= $max_distance_m
ORDER BY
    distance_m
LIMIT
    $limit;
```

```python
df = con.execute(
    load_sql("nearest_poi"),
    {"category": "grocery", "max_distance_m": 1500, "limit": 10},
).fetch_df()
```

!!! danger "Never f-string your SQL"
    Do not build SQL with f-strings or `%`-formatting, even for "trusted" internal
    inputs. Today's internal value is tomorrow's user input.

    ```python
    # BAD — vulnerable to SQL injection
    con.execute(f"SELECT * FROM pois WHERE category = '{category}'")

    # GOOD — bind parameter, type-safe and injection-safe
    con.execute(
        "SELECT * FROM pois WHERE category = $category",
        {"category": category},
    )
    ```

## When you can't bind a value

DuckDB (like all SQL engines) only allows binding *values*, not identifiers (table
names, column names) or file paths inside table-valued functions like
`read_parquet(...)`. For those cases:

1. Validate the value against an **allow-list** of known-safe strings, then
2. Substitute it via Python `str.format`, an f-string on the *template* (not the
   value), or a templating engine such as Jinja.

```python
ALLOWED_TABLES = {"pois", "blocks", "trips"}


def query_table(con, table: str, limit: int):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Unknown table: {table!r}")
    sql = load_sql("select_from_table").format(table=table)  # safe: validated
    return con.execute(sql, {"limit": limit}).fetch_df()
```

## Configuration over hardcoding

Paths to Parquet datasets, working CRS WKIDs, H3 resolutions, and similar values belong
in your project's configuration (e.g. `config/config.yml`) and should be passed in as
bind parameters — not baked into the `.sql` file.

```python
from myproject.config import config
from myproject.sql import load_sql

df = con.execute(
    load_sql("load_partitioned"),
    {
        "parquet_path": config.data.points_parquet,
        "h3_resolution": config.spatial.h3_resolution,
    },
).fetch_df()
```

## Spatial Extension

DuckDB's spatial capabilities (`ST_*` functions, GeoParquet I/O, reprojection) are
provided by the official
[`spatial` extension](https://duckdb.org/docs/extensions/spatial.html). It is not
bundled with the core engine — each connection that needs it must `INSTALL` (once per
machine) and `LOAD` (once per connection) the extension.

### One-time install, per-connection load

```python
import duckdb

con = duckdb.connect()
con.install_extension("spatial")   # downloads & caches; safe to call repeatedly
con.load_extension("spatial")      # makes ST_* functions available in this connection
```

In a project, prefer wrapping this in a small helper so every entry point gets a
consistently configured connection:

```python
# src/myproject/db.py
from __future__ import annotations

import duckdb


def get_spatial_connection(database: str = ":memory:") -> duckdb.DuckDBPyConnection:
    """Return a DuckDB connection with the spatial extension loaded."""
    con = duckdb.connect(database)
    con.install_extension("spatial")
    con.load_extension("spatial")
    return con
```

### Common spatial operations

```sql
-- src/myproject/sql/buffer_and_count.sql
--
-- Count points within a buffer of each origin, in a projected CRS.
WITH origins_proj AS (
    SELECT
        id,
        ST_Transform(geom, 'EPSG:4326', $working_crs) AS geom
    FROM
        ST_Read($origins_path)
),
points_proj AS (
    SELECT
        ST_Transform(geom, 'EPSG:4326', $working_crs) AS geom
    FROM
        ST_Read($points_path)
)
SELECT
    o.id,
    COUNT(p.geom) AS n_within
FROM
    origins_proj AS o
LEFT JOIN
    points_proj AS p
    ON ST_Intersects(ST_Buffer(o.geom, $buffer_m), p.geom)
GROUP BY
    o.id;
```

```python
from myproject.config import config
from myproject.sql import load_sql
from myproject.db import get_spatial_connection

con = get_spatial_connection()

df = con.execute(
    load_sql("buffer_and_count"),
    {
        "origins_path": str(config.data.origins_geoparquet),
        "points_path": str(config.data.points_geoparquet),
        "working_crs": config.spatial.crs_working,   # e.g. "EPSG:3857"
        "buffer_m": 1500,
    },
).fetch_df()
```

### Reading and writing spatial formats

The spatial extension exposes `ST_Read()` (powered by GDAL) and
`COPY ... TO ... (FORMAT GDAL, ...)`, giving you read access to most vector
formats — Shapefile, GeoPackage, GeoJSON, FlatGeobuf, file geodatabase, and
**GeoParquet**.

```sql
-- Read GeoParquet directly (preferred for large datasets)
SELECT * FROM read_parquet($parquet_path);

-- Read any GDAL-supported vector format
SELECT * FROM ST_Read($shapefile_path);

-- Write GeoParquet
COPY (SELECT * FROM origins) TO 'out.parquet' (FORMAT PARQUET);

-- Write any GDAL-supported format
COPY (SELECT * FROM origins) TO 'out.gpkg' (FORMAT GDAL, DRIVER 'GPKG');
```

!!! tip "Prefer GeoParquet for intermediate spatial data"
    GeoParquet preserves geometry as binary WKB plus a CRS in the file metadata, is
    columnar, splittable, and queryable in-place by DuckDB without loading the whole
    file into memory. Use it for everything between `data/raw/` and final delivery.

### CRS handling

Always work in a **projected** CRS (e.g. Web Mercator, a UTM zone, or a local
equidistant projection) when computing distances, areas, or buffers. `ST_Transform`
accepts authority codes (`'EPSG:4326'`) or full WKT/PROJ strings. Read the working CRS
from configuration — never hardcode it inside a `.sql` file.

### Restricted-network and air-gapped environments

`install_extension("spatial")` downloads the extension binary **once per (DuckDB
version, platform)** and caches it on disk. After that, every
`load_extension("spatial")` call — across all connections, all databases, and all
processes — reads from that cache. The download is **not** repeated per database or per
connection.

The cache lives at:

| Platform | Path |
|---|---|
| Windows | `%USERPROFILE%\.duckdb\extensions\<version>\<platform>\` |
| macOS / Linux | `~/.duckdb/extensions/<version>/<platform>/` |

Because `<version>` is part of the path, upgrading DuckDB (e.g. when ArcGIS Pro ships a
new bundled `duckdb`) triggers a one-time re-download on first use.

On networks where `https://extensions.duckdb.org/` is blocked, choose one of the
following patterns:

#### 1. Pre-seed the cache during onboarding

Run `con.install_extension("spatial")` once on a machine with internet access, then
copy the resulting `~/.duckdb/extensions/` directory to user profiles on locked-down
machines (via group policy, MDM, or a login script). The cache is just files — no
DuckDB process needs to be running on the target machine.

#### 2. Host extensions on an internal mirror

DuckDB supports a custom extension repository:

```sql
SET custom_extension_repository = 'https://extensions.internal.example.com';
INSTALL spatial;
```

IT mirrors the contents of `https://extensions.duckdb.org/` (or just the extensions
you need) onto an internal HTTPS host once. Document the internal URL in your project
config and apply it in `get_spatial_connection()`:

```python
# src/myproject/db.py
from myproject.config import config
import duckdb


def get_spatial_connection(database: str = ":memory:") -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(database)
    repo = getattr(config.duckdb, "extension_repository", None)
    if repo:
        con.execute(f"SET custom_extension_repository = '{repo}';")
    con.install_extension("spatial")
    con.load_extension("spatial")
    return con
```

#### 3. Bundle the extension with the project (most reliable for air-gap)

Commit the `.duckdb_extension` binary into the repository (or distribute it with your
release artifact) and `LOAD` it by absolute path — bypassing `INSTALL` entirely:

```text
vendor/
└── duckdb-extensions/
    └── v1.1.3/
        └── windows_amd64/
            └── spatial.duckdb_extension
```

```python
from pathlib import Path
import duckdb
from myproject.config import config


def get_spatial_connection(database: str = ":memory:") -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(database)
    ext_path = Path(config.duckdb.spatial_extension_path)  # absolute path on disk
    con.execute(f"LOAD '{ext_path.as_posix()}';")
    return con
```

!!! tip
    To allow loading extensions from arbitrary paths, you may need
    `SET allow_unsigned_extensions = true;` *before* the `LOAD` — the bundled binary is
    signed by DuckDB Labs, so this is usually unnecessary, but worth knowing if you
    build the extension yourself.

#### Verifying the cache state

```powershell
# Windows
Test-Path "$env:USERPROFILE\.duckdb\extensions"
Get-ChildItem "$env:USERPROFILE\.duckdb\extensions" -Recurse -Filter "spatial*"
```

```bash
# macOS / Linux
ls -R ~/.duckdb/extensions/ 2>/dev/null | grep spatial
```

If the file is present, `load_extension("spatial")` will succeed offline.

## Package-data setup

`.sql` files are shipped with the wheel via `pyproject.toml`:

```toml
[tool.setuptools.package-data]
"myproject.sql" = ["*.sql"]
```

If you add a sub-directory under `sql/` (e.g. `sql/spatial/`), add a matching entry:

```toml
[tool.setuptools.package-data]
"myproject.sql"         = ["*.sql"]
"myproject.sql.spatial" = ["*.sql"]
```

…and create an `__init__.py` inside the new directory so it is a proper sub-package.
