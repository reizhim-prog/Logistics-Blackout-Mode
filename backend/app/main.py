from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import math

from .settings import settings
from .schemas import QuakeEventIn
from .repo.loaders import load_all
from .services.scoring import score_event
from .services.packages import recommend_package


app = FastAPI(
    title="Quake Blackout Logistics API",
    version="0.1"
)

here = os.path.dirname(__file__)                       # backend/app
backend_dir = os.path.abspath(os.path.join(here, ".."))  # backend
root_dir = os.path.abspath(os.path.join(backend_dir, ".."))  # project root
assets_dir = os.path.join(root_dir, "frontend", "assets")

app.mount(
    "/assets",
    StaticFiles(directory=assets_dir),
    name="assets"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # demo / lokal
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# GLOBAL DATA CACHE
# =========================
DFS = {}

@app.on_event("startup")
def startup():
    global DFS
    DFS = load_all(settings.DATA_DIR)
    air = DFS["air_nodes.csv"]
    print("NaN lat:", air["lat"].isna().sum(), "NaN lon:", air["lon"].isna().sum(), "NaN name:", air["name"].isna().sum())
    print(air[air[["lat","lon","name"]].isna().any(axis=1)].head())

# =========================
# JSON SANITIZER (ANTI NaN)
# =========================
def json_sanitize(x):
    if x is None:
        return None
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return None
        return x
    if isinstance(x, dict):
        return {k: json_sanitize(v) for k, v in x.items()}
    if isinstance(x, list):
        return [json_sanitize(v) for v in x]
    return x

# =========================
# FRONTEND
# =========================
@app.get("/")
def serve_frontend():
    here = os.path.dirname(__file__)                       # backend/app
    backend_dir = os.path.abspath(os.path.join(here, ".."))  # backend
    root_dir = os.path.abspath(os.path.join(backend_dir, ".."))  # project root
    html_path = os.path.join(root_dir, "frontend", "index.html")
    return FileResponse(html_path)

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# SIMULATION ENDPOINT
# =========================
@app.post("/simulate")
def simulate(evt: QuakeEventIn):
    top_n = evt.top_n or 10

    ranked = score_event(
        dfs=DFS,
        event_lat=evt.lat,
        event_lon=evt.lon,
        mag=evt.mag,
        top_n=top_n,
    )

    payload = {
        "event": {
            "lat": evt.lat,
            "lon": evt.lon,
            "mag": evt.mag,
            "depth_km": evt.depth_km,
            "package_recommendation": recommend_package(evt.mag),
        },
        "results": ranked.to_dict(orient="records"),
    }

    return json_sanitize(payload)
