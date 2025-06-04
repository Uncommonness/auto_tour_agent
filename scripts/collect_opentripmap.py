import argparse
import csv
import requests
from typing import List, Dict


API_BASE = "https://api.opentripmap.com/0.1"


def fetch_places(api_key: str, lat: float, lon: float, radius: int, limit: int, lang: str = "en", kinds: str | None = None) -> List[Dict]:
    """Fetch basic place information within a radius.

    Optionally filter results by comma-separated ``kinds`` categories.
    """
    url = f"{API_BASE}/{lang}/places/radius"
    params = {
        "apikey": api_key,
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "limit": limit,
        "format": "json",
    }
    if kinds:
        params["kinds"] = kinds
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def collect_data(api_key: str, lat: float, lon: float, radius: int, limit: int, out_csv: str, lang: str = "en", kinds: str | None = None) -> None:
    """Collect places around a point and save them to a CSV file."""
    places = fetch_places(api_key, lat, lon, radius, limit, lang, kinds=kinds)

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
    parser.add_argument("--apikey", required=True, help="OpenTripMap API key")
    parser.add_argument("--lat", type=float, required=True, help="Latitude of the center")
    parser.add_argument("--lon", type=float, required=True, help="Longitude of the center")
    parser.add_argument("--radius", type=int, default=1000, help="Search radius in meters")
    parser.add_argument("--limit", type=int, default=50, help="Maximum number of places to fetch")
    parser.add_argument("--kinds", help="Comma-separated place categories to filter")
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
        kinds=args.kinds,
    )


if __name__ == "__main__":
    main()
