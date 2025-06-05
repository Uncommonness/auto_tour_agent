import argparse
import csv
import os
import shutil
import requests
from typing import List, Dict, Optional


API_BASE = "https://api.opentripmap.com/0.1"
SAMPLE_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "example_places.csv")


def fetch_places(api_key: str, lat: float, lon: float, radius: int, limit: int, lang: str = "en") -> List[Dict]:
    """Fetch basic place information within a radius."""

    url = f"{API_BASE}/{lang}/places/radius"
    params = {
        "apikey": api_key,
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "limit": limit,
        "format": "json",
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def collect_data(api_key: Optional[str], lat: float, lon: float, radius: int, limit: int, out_csv: str, lang: str = "en") -> None:
    """Collect places around a point and save them to a CSV file.

    If ``api_key`` is ``None`` the bundled sample data is copied to ``out_csv``.
    """
    if api_key is None:
        shutil.copyfile(SAMPLE_CSV, out_csv)
        print(f"No API key provided, copied sample data to {out_csv}")
        return

    places = fetch_places(api_key, lat, lon, radius, limit, lang)


    fieldnames = ["xid", "name", "lat", "lon", "kinds"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in places:
            writer.writerow({
                "xid": item.get("xid"),
                "name": item.get("name"),
                "lat": item.get("point", {}).get("lat"),
                "lon": item.get("point", {}).get("lon"),
                "kinds": item.get("kinds"),
            })


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect POI data from OpenTripMap API")
    parser.add_argument("--apikey", help="OpenTripMap API key")
    parser.add_argument("--lat", type=float, default=0.0, help="Latitude of the center (ignored without API key)")
    parser.add_argument("--lon", type=float, default=0.0, help="Longitude of the center (ignored without API key)")
    parser.add_argument("--radius", type=int, default=1000, help="Search radius in meters")
    parser.add_argument("--limit", type=int, default=50, help="Maximum number of places to fetch")
    parser.add_argument("--lang", default="en", help="Language code")
    parser.add_argument("--output", default="data/places.csv", help="Output CSV path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    collect_data(
        api_key=args.apikey,
        lat=args.lat,
        lon=args.lon,
        radius=args.radius,
        limit=args.limit,
        out_csv=args.output,
        lang=args.lang,
    )


if __name__ == "__main__":
    main()
