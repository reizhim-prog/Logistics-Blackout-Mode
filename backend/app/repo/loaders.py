import os
import pandas as pd

REQUIRED = [
    "admin_units.csv",
    "pop_admin.csv",
    "health_facilities.csv",
]

OPTIONAL = [
    "air_nodes.csv",
    "road_nodes.csv",
    "road_edges.csv",
    "events_quake_catalog.csv",
]

def _read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_all(data_dir: str) -> dict[str, pd.DataFrame]:
    """
    Returns dict: { "<filename>.csv": DataFrame }
    """
    data_dir = os.path.abspath(data_dir)
    dfs: dict[str, pd.DataFrame] = {}

    # required
    for fn in REQUIRED:
        fpath = os.path.join(data_dir, fn)
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"Required file not found: {fpath}")
        dfs[fn] = _read_csv(fpath)

    # optional (load if exists)
    for fn in OPTIONAL:
        fpath = os.path.join(data_dir, fn)
        if os.path.exists(fpath):
            dfs[fn] = _read_csv(fpath)

    return dfs
