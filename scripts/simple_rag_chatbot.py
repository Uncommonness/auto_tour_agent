import argparse
import csv
from collections import defaultdict
from typing import List, Dict


def load_places(csv_path: str) -> List[Dict[str, str]]:
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def categorize_places(places: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    grouped = defaultdict(list)
    for p in places:
        kinds = (p.get('kinds') or '').split(',')
        for k in kinds:
            grouped[k.strip()].append(p)
    return grouped


def plan_itinerary(places: List[Dict[str, str]], days: int = 1) -> List[List[Dict[str, str]]]:
    groups = categorize_places(places)
    attractions = groups.get('interesting_places', [])
    restaurants = groups.get('restaurants', [])
    hotels = groups.get('accomodations', [])

    itinerary = []
    for day in range(days):
        day_plan = []
        if day < len(attractions):
            day_plan.append(attractions[day])
        if day < len(restaurants):
            day_plan.append(restaurants[day])
        if day < len(hotels):
            day_plan.append(hotels[day])
        itinerary.append(day_plan)
    return itinerary


def print_plan(itinerary: List[List[Dict[str, str]]]):
    for i, day in enumerate(itinerary, 1):
        print(f"Day {i}:")
        for p in day:
            print(f"  - {p['name']} ({p['kinds']})")
        if not day:
            print("  No recommendations.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple itinerary generator")
    parser.add_argument('--data', default='data/seoul_sample.csv', help='CSV dataset of places')
    parser.add_argument('--days', type=int, default=1, help='Number of days to plan')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    places = load_places(args.data)
    itinerary = plan_itinerary(places, args.days)
    print_plan(itinerary)


if __name__ == '__main__':
    main()
