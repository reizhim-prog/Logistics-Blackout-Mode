def recommend_package(mag: float):
    
    if mag is None:
        return ["medis_dasar", "selimut"]

    if mag >= 7.5:
        return ["air_bersih", "tenda", "medis_dasar", "selimut"]
    elif mag >= 6.8:
        return ["air_bersih", "medis_dasar", "selimut"]
    else:
        return ["medis_dasar", "selimut"]
