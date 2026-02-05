from pydantic import BaseModel, Field

class QuakeEventIn(BaseModel):
    lat: float = Field(...)
    lon: float = Field(...)
    mag: float = Field(..., ge=0)
    depth_km: float | None = Field(None, ge=0)
    top_n: int | None = Field(None, ge=1, le=200)
