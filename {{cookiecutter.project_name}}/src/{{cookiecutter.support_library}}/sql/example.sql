-- Example query template. Replace or delete when adding real queries.
--
-- Loaded via: load_sql("example")
-- Executed via: con.execute(load_sql("example"), {"limit": 10})
--
-- Always use bind parameters ($name) rather than f-string interpolation.

SELECT
    *
FROM
    read_parquet($parquet_path)
LIMIT
    $limit;
