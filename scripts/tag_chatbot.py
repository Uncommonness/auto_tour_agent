import argparse
import csv
import os
import sqlite3
from typing import List, Dict

import google.generativeai as genai

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS places (
    xid TEXT PRIMARY KEY,
    name TEXT,
    lat REAL,
    lon REAL,
    kinds TEXT
)
"""


def init_db(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    conn.execute(DB_SCHEMA)
    conn.commit()
    conn.close()


def import_csv(csv_path: str, db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT OR REPLACE INTO places (xid, name, lat, lon, kinds) VALUES (?,?,?,?,?)",
                (row.get("xid"), row.get("name"), row.get("lat"), row.get("lon"), row.get("kinds")),
            )
    conn.commit()
    conn.close()


def search_by_tag(db_path: str, tag: str) -> List[Dict[str, str]]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name, kinds FROM places WHERE kinds LIKE ?", (f"%{tag}%",))
    rows = cur.fetchall()
    conn.close()
    return [{"name": r[0], "kinds": r[1]} for r in rows]


def build_prompt(places: List[Dict[str, str]], question: str) -> str:
    lines = [f"- {p['name']} ({p['kinds']})" for p in places]
    joined = "\n".join(lines) if lines else "No places found."
    return (
        "You are a travel assistant. Answer the user's question using only the "
        f"following places.\nQuestion: {question}\nPlaces:\n{joined}"
    )


def ask_gemini(prompt: str, api_key: str) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="TAG-based travel chatbot")
    sub = parser.add_subparsers(dest="command", required=True)

    p_import = sub.add_parser("import", help="Import CSV data into SQLite")
    p_import.add_argument("--csv", required=True, help="CSV file path")
    p_import.add_argument("--db", default="places.db", help="Database path")

    p_query = sub.add_parser("query", help="Query places by tag and ask Gemini")
    p_query.add_argument("--tag", required=True, help="Place tag to search")
    p_query.add_argument("--question", required=True, help="User question")
    p_query.add_argument("--db", default="places.db", help="Database path")
    p_query.add_argument("--apikey", default=os.getenv("GEMINI_API_KEY"), help="Gemini API key")

    args = parser.parse_args()

    if args.command == "import":
        init_db(args.db)
        import_csv(args.csv, args.db)
    elif args.command == "query":
        if not args.apikey:
            raise SystemExit("GEMINI_API_KEY not set and --apikey not provided")
        places = search_by_tag(args.db, args.tag)
        prompt = build_prompt(places, args.question)
        answer = ask_gemini(prompt, args.apikey)
        print(answer)


if __name__ == "__main__":
    main()
