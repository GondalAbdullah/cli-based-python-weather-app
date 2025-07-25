import os
import json
import requests
from datetime import datetime


def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
    except Exception as e:
        print(f"Error occured while fetching data.Try again with proper input: {e}")
        log_error(f"Error occured while fetching data.Try again with proper input: {e}")


def load_recent():
    if not os.path.exists("recent.json"):
        print("NO RECENT SEARCHES...")
        return []
    try:
        with open("recent.json", "r") as recent_file:
            return json.load(recent_file)
    except Exception as e:
        print(f"Error occured while loading forecast history: {e}")
        log_error(f"Error occured while loading forecast history: {e}")
        return []


def save_recent(data):
    recent_list = []
    recent_list = load_recent()

    recent_list.insert(0, data)
    recent_list = recent_list[:5]

    with open("recent.json", "w") as recent_file:
        json.dump(recent_list, recent_file, indent=2)


def log_error(message):
    with open("error.log", "a") as error_file:

        error_file.write(f"{datetime.now()} - {message}\n")
