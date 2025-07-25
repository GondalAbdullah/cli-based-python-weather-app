import os
import time
import json


# Make sure the file exists
def init_cache():
    if not os.path.exists("cache.json"):
        with open("cache.json", "w") as f:
            json.dump({}, f)


# Generate a consistent key based on parameters
def generate_cache_key(mode, unit, **kwargs):
    parts = [f"mode={mode}", f"unit={unit}"] + [
        f"{k}={v}" for k, v in sorted(kwargs.items())
    ]
    return "|".join(parts)


# Read JSON cache
def read_cache():
    with open("cache.json", "r") as f:
        return json.load(f)


# Write JSON cache
def write_cache(cache_data):
    with open("cache.json", "w") as f:
        json.dump(cache_data, f, indent=2)


# Get cached data if fresh
def get_cached_data(key):
    init_cache()
    cache = read_cache()
    if key in cache:
        entry = cache[key]
        age = time.time() - entry["timestamp"]
        if age < 600:
            return entry["data"]
        else:
            print("Cached data expired.")
    return None


# Save API result to cache
def save_to_cache(key, data):
    try:
        init_cache()
        cache = read_cache()
        cache[key] = {"timestamp": time.time(), "data": data}
        write_cache(cache)
        print("\nSaved to cache\n")
    except Exception as e:
        print(f"Error occured while saving to cache: {e}")
