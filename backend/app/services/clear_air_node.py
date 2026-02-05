import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]   
p = BASE.parent / "data" / "processed" / "air_nodes.csv"  

air = pd.read_csv(p)
air["lat"] = pd.to_numeric(air["lat"], errors="coerce")
air["lon"] = pd.to_numeric(air["lon"], errors="coerce")

air_clean = air.dropna(subset=["name", "lat", "lon"]).copy()
air_clean.to_csv(p, index=False)

print("sebelum", len(air), "sesudah", len(air_clean))
print("NaN lat", air_clean["lat"].isna().sum(), "NaN lon", air_clean["lon"].isna().sum(), "NaN name", air_clean["name"].isna().sum())
