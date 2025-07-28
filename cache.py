import os
import time
import json


def create_cache():
    if not os.path.exists("cache.json"):
        with open("cache.json", "w") as cache_file:
            json.dump({}, cache_file)


def read_cache():
    with open("cache.json", "r") as cache_file:
        return json.load(cache_file)


def write_cache(cache_data):
    with open("cache.json", "w") as cache_file:
        json.dump(cache_data, cache_file, indent=2)


def generate_cache_key(mode, unit, **kwargs):
    parts = [f"mode={mode}", f"unit={unit}"] + [
        f"{k}={v}" for k, v in sorted(kwargs.items())
    ]
    return "|".join(parts)


def get_cached_data(key):
    create_cache()
    cache = read_cache()
    if key in cache:
        entry = cache[key]
        age = time.time() - entry["timestamp"]
        if age < 600:
            return entry["data"]
        else:
            print("Cached data expired.")
    return None


def save_to_cache(key, data):
    try:
        create_cache()
        cache = read_cache()
        cache[key] = {"timestamp": time.time(), "data": data}
        write_cache(cache)
        print("\nSaved to cache\n")
    except Exception as e:
        print(f"Error occured while saving to cache: {e}")
