import json
import os

def load_cache():
    if os.path.exists("cache.json"):
        with open("cache.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(data):
    with open("cache.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
