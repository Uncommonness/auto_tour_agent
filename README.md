# Auto Tour Agent


This repository contains basic utilities for collecting points of interest (POI) data using the [OpenTripMap](https://opentripmap.io/product) API. The script helps you gather travel information that can be used for building tourism datasets or exploration tools.

## Requirements

Install the dependencies via pip:

```bash
pip install -r requirements.txt
```

## Collecting POI Data

Use `scripts/collect_opentripmap.py` to fetch places around a location. You must supply your own OpenTripMap API key.

Example usage:

```bash
python scripts/collect_opentripmap.py \
    --apikey YOUR_API_KEY \
    --lat 37.5665 \
    --lon 126.9780 \
    --radius 1000 \
    --limit 50 \
    --output data/seoul_poi.csv
```

This command downloads up to 50 places within a 1 km radius of the coordinates provided (here: Seoul, South Korea) and saves them to `data/seoul_poi.csv`.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
