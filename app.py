from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import uvicorn
import os

app = FastAPI()

# Initialize Nominatim geocoder
geolocator = Nominatim(user_agent="distance_web_app_v1")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class Location(BaseModel):
    lat: float
    lon: float

class DistanceRequest(BaseModel):
    start: Location
    end: Location

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/api/geocode")
async def geocode(query: str = Query(..., min_length=1)):
    try:
        location = geolocator.geocode(query, language='ko')
        if location:
            return {
                "address": location.address,
                "lat": location.latitude,
                "lon": location.longitude,
                "found": True
            }
        else:
            return {"found": False, "message": "Location not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/calculate")
async def calculate_distance(request: DistanceRequest):
    try:
        start_coords = (request.start.lat, request.start.lon)
        end_coords = (request.end.lat, request.end.lon)
        dist = geodesic(start_coords, end_coords).kilometers
        return {"distance_km": round(dist, 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
