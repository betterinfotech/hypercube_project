from __future__ import annotations

import json
from pathlib import Path
import pandas as pd


def reset_sqlite(db_path: str = "etl.db") -> None:
    # Delete the SQLite file if it exists (just for demo)
    db_file = Path(db_path)
    if db_file.exists():
        db_file.unlink()
        print(f"Deleted existing DB: {db_path}")


def load_to_sqlite(df: pd.DataFrame, table_name: str, db_path: str = "etl.db") -> None:
    from pathlib import Path
    import sqlite3

    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # If no rows to write, drop the existing table so nothing stale lingers
    if df is None or df.empty:
        with sqlite3.connect(db_path) as con:
            con.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        print(f"Dropped table '{table_name}' (no rows this run)")
        return

    # Replace NaN with None so SQLite stores them as NULL
    safe = df.where(pd.notnull(df), None)

    with sqlite3.connect(db_path) as con:
        safe.to_sql(table_name, con, if_exists="replace", index=False)
        print(f"Wrote table '{table_name}' ({len(safe)} rows) to {db_path}")
