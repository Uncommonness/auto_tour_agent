import argparse
import csv
import os
import google.generativeai as genai
from typing import List, Dict


def load_places(csv_path: str) -> List[Dict[str, str]]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_prompt(places: List[Dict[str, str]], days: int) -> str:
    lines = [f"- {p['name']} ({p['kinds']})" for p in places]
    joined = "\n".join(lines)
    return (
        f"You are a travel assistant. Using the following places, plan a {days}-day itinerary in Seoul.\n"
        f"Places:\n{joined}"
    )


def generate_itinerary(csv_path: str, days: int, api_key: str) -> str:
    places = load_places(csv_path)
    prompt = build_prompt(places, days)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate itinerary with Gemini")
    parser.add_argument("--apikey", default=os.getenv("GEMINI_API_KEY"), help="Gemini API key")
    parser.add_argument("--data", default="data/seoul_sample.csv", help="CSV dataset of places")
    parser.add_argument("--days", type=int, default=1, help="Number of days to plan")
    return parser.parse_args()



def main() -> None:
    args = parse_args()
    if not args.apikey:
        raise SystemExit("GEMINI_API_KEY not set and --apikey not provided")
    result = generate_itinerary(args.data, args.days, args.apikey)
    print(result)


if __name__ == "__main__":
    main()
