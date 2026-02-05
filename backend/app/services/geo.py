import numpy as np
import pandas as pd

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1 = np.radians(float(lat1))
    lon1 = np.radians(float(lon1))
    lat2 = np.radians(lat2.astype(float))
    lon2 = np.radians(lon2.astype(float))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2.0)**2
    return 2.0 * R * np.arcsin(np.sqrt(a))

def nearest_points_for_admins(admin_df: pd.DataFrame, points_df: pd.DataFrame, name_col: str):
    """
    For each admin centroid, find nearest point in points_df.
    Returns: nearest_km (np array), nearest_name (np array), nearest_type (np array optional)
    """
    p_lat = points_df["lat"].to_numpy(dtype=float)
    p_lon = points_df["lon"].to_numpy(dtype=float)
    p_name = points_df[name_col].astype(str).to_numpy(dtype=object)
    p_type = points_df["type"].astype(str).to_numpy(dtype=object) if "type" in points_df.columns else None

    nearest_km = np.zeros(len(admin_df), dtype=float)
    nearest_name = np.empty(len(admin_df), dtype=object)
    nearest_type = np.empty(len(admin_df), dtype=object) if p_type is not None else None

    for i, row in enumerate(admin_df.itertuples(index=False)):
        d = haversine_km(row.lat, row.lon, p_lat, p_lon)
        j = int(np.argmin(d))
        nearest_km[i] = float(d[j])
        nearest_name[i] = p_name[j]
        if p_type is not None:
            nearest_type[i] = p_type[j]

    return nearest_km, nearest_name, nearest_type
