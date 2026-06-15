"""
Google Maps Places API: A Quick Start Example
See more at: https://apify.com/johnvc/google-maps-places-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/google-maps-places-api/input-schema?fpr=9n7kx3

This script shows how to call the Google Maps Places API on Apify from Python
and read its structured JSON output: one row per place, with name, address,
coordinates, rating and review count, category, phone, website, price level,
opening hours, and the Google place ID. It sets several input parameters so you
can see what is configurable, while keeping the run small so your first call
stays cheap.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# One search term with the minimum result count keeps this first run inexpensive.
# Add more terms, or raise maxResultsPerSearch, once you know your budget.
run_input = {
    "searchTerms": ["coffee shops in Austin, TX"],
    "maxResultsPerSearch": 20,   # minimum 20; pages are ~20 places each
    "language": "en",
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/google-maps-places-api").call(run_input=run_input)

# Read structured results from the run's default dataset.
# apify-client 3.x returns a typed Run object, so use the attribute (not run["defaultDatasetId"]).
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} place(s).\n")

# Each item is one place.
for place in items:
    name = place.get("title")
    rating = place.get("rating")
    count = place.get("ratingCount")
    line = f"{place.get('position')}. {name}"
    if rating is not None:
        line += f"  {rating} stars"
        if count is not None:
            line += f" ({count} reviews)"
    print(line)
    print(f"   {place.get('type')} | {place.get('address')}")
    contact = [c for c in (place.get("phoneNumber"), place.get("website")) if c]
    if contact:
        print("   " + "  ".join(contact))
    coords = (place.get("latitude"), place.get("longitude"))
    if all(c is not None for c in coords):
        print(f"   {coords[0]}, {coords[1]}  (place ID: {place.get('placeId')})")
    print()
