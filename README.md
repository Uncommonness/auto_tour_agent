# Auto Tour Agent

This repository contains basic utilities for collecting points of interest (POI) data using the [OpenTripMap](https://opentripmap.io/product) API. A small sample dataset is included so you can try the chatbot without providing an OpenTripMap key. In addition, a Gemini powered chatbot demonstrates how to generate itineraries from the dataset.

## Requirements

Install the dependencies via pip:

```bash
pip install -r requirements.txt
```

## Collecting POI Data

Use `scripts/collect_opentripmap.py` to fetch places around a location. This step is optional because a small Seoul dataset (`data/seoul_sample.csv`) is already provided. If you do run the script, you must supply your own OpenTripMap API key.

Example usage (collect attractions, hotels and restaurants around Seoul City Hall):

```bash
python scripts/collect_opentripmap.py \
    --apikey YOUR_API_KEY \
    --lat 37.5665 \
    --lon 126.9780 \
    --radius 1000 \
    --limit 50 \
    --kinds interesting_places,accomodations,restaurants \
    --output data/seoul_poi.csv
```

This command downloads up to 50 places within a 1 km radius of the coordinates provided (here: Seoul, South Korea) and saves them to `data/seoul_poi.csv`.

## Simple Itinerary Generation

Once you have collected data (or use the provided `data/seoul_sample.csv`), you can
generate a very basic itinerary using `scripts/simple_rag_chatbot.py`:

```bash
python scripts/simple_rag_chatbot.py --data data/seoul_sample.csv --days 2
```

The script selects a point of interest, a restaurant and a hotel for each day from
the dataset and prints them to the console. It is a lightweight demonstration of a
retrieval‐augmented workflow without relying on external services.

## Gemini Chatbot

If you have a Gemini API key, you can generate a short itinerary using the
language model. Set your API key in the ``GEMINI_API_KEY`` environment variable
and run:

```bash
python scripts/gemini_chatbot.py --data data/seoul_sample.csv --days 2
```

The script sends the place names to Gemini and prints the resulting itinerary.

## Simple Web Interface

You can also try a minimal Flask web application that requires login before using
the chatbot. Run it with:

```bash
python webapp.py
```

Then visit `http://localhost:5000` in your browser and log in with `admin` / `password`.
If `GEMINI_API_KEY` is set, the web interface will use Gemini to suggest an itinerary.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
