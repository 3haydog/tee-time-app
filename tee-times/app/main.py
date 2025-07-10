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
def get_tee_times(
    date: Optional[str] = Query(None, description="Format: YYYY-MM-DD"),
    min_players: int = Query(1, ge=1, le=4, description="Minimum open spots"),
    holes: str = Query("any", pattern="^(9|18|any)$", description="9, 18, or any")
):
    """
    Aggregates tee times from all courses for a given date (default = today).
    Returns structured list of tee time dictionaries.
    """
    tee_times = run_all_scrapers(date, min_players=min_players, holes=holes)
    return {
        "date": date,
        "count": len(tee_times),
        "tee_times": tee_times
    }