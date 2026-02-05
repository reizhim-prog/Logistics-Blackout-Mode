import numpy as np
import pandas as pd
from .geo import haversine_km, nearest_points_for_admins

def _minmax(x: np.ndarray) -> np.ndarray:
    x = x.astype(float)
    mn, mx = float(np.min(x)), float(np.max(x))
    if mx - mn < 1e-9:
        return np.zeros_like(x, dtype=float)
    return (x - mn) / (mx - mn)

def score_event(
    dfs: dict[str, pd.DataFrame],
    event_lat: float,
    event_lon: float,
    mag: float,
    top_n: int = 15,
    weights=(0.50, 0.35, 0.15),
) -> pd.DataFrame:

    admin_df = dfs["admin_units.csv"].copy()
    pop_df = dfs["pop_admin.csv"].copy()
    health_df = dfs["health_facilities.csv"].copy()

    # join population
    pop_df["admin_id"] = pop_df["admin_id"].astype(str)
    admin_df["admin_id"] = admin_df["admin_id"].astype(str)

    df = admin_df.merge(pop_df[["admin_id", "population"]], on="admin_id", how="left")
    df["population"] = df["population"].fillna(0).astype(float)

    # distance to epicenter
    dist_km = haversine_km(event_lat, event_lon, df["lat"].to_numpy(), df["lon"].to_numpy())

    # hazard proxy
    hazard_raw = (float(mag) ** 2) / (dist_km + 10.0)
    score_hazard = _minmax(hazard_raw)

    # exposure
    score_exposure = _minmax(df["population"].to_numpy())

    air_df = dfs["air_nodes.csv"].copy()
    air_df = air_df.dropna(subset=["lat", "lon", "name"])

    # nearest health (name + km)
    h_km, h_name, _ = nearest_points_for_admins(
        df[["lat", "lon", "admin_id", "admin_name", "kabupaten"]],
        health_df[["lat", "lon", "name", "type"]].rename(columns={"name": "name"}),
        name_col="name"
    )
    score_medgap = _minmax(h_km)

    w_h, w_e, w_m = weights
    total = w_h*score_hazard + w_e*score_exposure + w_m*score_medgap

    out = df[["admin_id","admin_name","kabupaten","lat","lon"]].copy()
    out["score_total"] = total
    out["score_hazard"] = score_hazard
    out["score_exposure"] = score_exposure
    out["score_medgap"] = score_medgap

    out["distance_to_epicenter_km"] = dist_km.round(3)
    out["population_raw"] = df["population"].astype(float)
    out["nearest_health_km"] = np.round(h_km, 3)
    out["nearest_health_name"] = h_name.astype(str)

   
    if "air_nodes.csv" in dfs:
        air_df = dfs["air_nodes.csv"].copy()
        a_km, a_name, a_type = nearest_points_for_admins(
            df[["lat","lon","admin_id","admin_name","kabupaten"]],
            air_df[["lat","lon","name","type"]],
            name_col="name"
        )
        out["nearest_air_km"] = np.round(a_km, 3)
        out["nearest_air_name"] = a_name.astype(str)
        out["nearest_air_type"] = a_type.astype(str) if a_type is not None else ""


    reasons = []
    for i in range(len(out)):
        rs = []
        rs.append(f"Dist {out.loc[out.index[i],'distance_to_epicenter_km']:.1f} km")
        rs.append(f"Pop {int(out.loc[out.index[i],'population_raw']):,}".replace(",", "."))
        rs.append(f"RS terdekat {out.loc[out.index[i],'nearest_health_name']} ({out.loc[out.index[i],'nearest_health_km']:.1f} km)")
        reasons.append(rs)
    out["reasons"] = reasons

    out = out.sort_values("score_total", ascending=False).head(int(top_n)).reset_index(drop=True)
    out["weights_used"] = [ {"hazard":w_h,"exposure":w_e,"medgap":w_m} ] * len(out)
    return out
