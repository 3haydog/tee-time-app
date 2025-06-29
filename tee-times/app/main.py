from fastapi import FastAPI, Query
from typing import Optional
from run_all_scrapers import run_all_scrapers
from fastapi.middleware.cors import CORSMiddleware

print("🚀 Loaded: app.main.py")

app = FastAPI(title="Golf Tee Time API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify "http://localhost:5173" for stricter control
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tee-times")
def get_tee_times(date: Optional[str] = Query(None, description="Format: YYYY-MM-DD")):
    """
    Aggregates tee times from all courses for a given date (default = today).
    Returns structured list of tee time dictionaries.
    """
    tee_times = run_all_scrapers(date)
    return {
        "date": date,
        "count": len(tee_times),
        "tee_times": tee_times
    }