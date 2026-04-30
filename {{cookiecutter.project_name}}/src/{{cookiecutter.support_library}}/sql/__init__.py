"""
SQL query resources for the `{{cookiecutter.support_library}}` package.

Place externalised SQL queries (typically used with DuckDB) in this directory as
`.sql` files. See the `AGENTS.md` section "SQL and DuckDB Query Organization"
for guidance on when to externalise queries and how to parameterise them.

Files in this directory are shipped as package data and loaded at runtime via
the `load_sql()` helper exposed below.
"""

from __future__ import annotations

from functools import lru_cache
from importlib.resources import files


@lru_cache(maxsize=None)
def load_sql(name: str) -> str:
    """Load a `.sql` file shipped inside this `sql/` resource directory.

    The query text is read once per `name` and cached for the lifetime of the
    process. Always pass user-supplied or runtime values via DuckDB bind
    parameters (e.g. `con.execute(load_sql("foo"), {"id": 42})`) rather than
    interpolating them into the returned string.

    !!! note
        The `name` argument is the file stem (no `.sql` extension). For
        example, `load_sql("nearest_poi")` reads `nearest_poi.sql`.

    ```python
    import duckdb
    from {{cookiecutter.support_library}}.sql import load_sql

    con = duckdb.connect()
    df = con.execute(
        load_sql("nearest_poi"),
        {"max_distance_m": 1500, "category": "grocery"},
    ).fetch_df()
    ```

    Args:
        name: File stem of the SQL resource to load (without the `.sql`
            extension).

    Returns:
        str: The full text of the requested SQL file.

    Raises:
        FileNotFoundError: If `<name>.sql` does not exist in this directory.
    """
    resource = files(__name__).joinpath(f"{name}.sql")
    if not resource.is_file():
        raise FileNotFoundError(
            f"SQL resource '{name}.sql' not found in "
            f"'{{cookiecutter.support_library}}.sql'."
        )
    return resource.read_text(encoding="utf-8")


__all__ = ["load_sql"]
