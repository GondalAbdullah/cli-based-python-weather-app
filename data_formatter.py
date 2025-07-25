from collections import defaultdict
from tabulate import tabulate

units = {
    "metric" : {
        "temp" : "°C",
        "speed" : "m/s"

    },
    "imperial" : {
        "temp" : "°F",
        "speed" : "mph"
    }
}


def give_current_weather(data, unit="metric"):
    my_data = [
        [f"Name of Country: {data["name"]}"],
        [f"Temperature: {data["main"]["temp"]} {units[unit]["temp"]}"],
        [f"Weather: {data["weather"][0]["description"]}"],
        [f"Humidity: {data["main"]["humidity"]} %"],
        [f"Wind Speed: {data["wind"]["speed"]} {units[unit]["speed"]}"],
        [f"Wind Direction: {get_wind_speed(data)}"],
        [f"Atmospheric Pressure: {data["main"]["pressure"]} hPa"],
    ]

    print("CURRENT WEATHER:")
    return tabulate(my_data, tablefmt="fancy_grid")


def get_wind_speed(data):
    directions = ["North", "North-East", "East", "South-East",
                  "South", "South-West", "West", "North-West"]
    degrees = data["wind"]["deg"]
    return directions[int((degrees/360)*8)]


def give_forecast(data, unit="metric"):

    forecast_by_day = defaultdict(list)

    for entry in data["list"]:
        dt_txt = entry["dt_txt"]
        date_str = dt_txt.split()[0]
        temp = entry["main"]["temp"]
        desc = entry["weather"][0]["description"].capitalize()
        forecast_by_day[date_str].append((dt_txt, temp, desc))

    forecast_rows = []
    for date, values in forecast_by_day.items():
        temps = [v[1] for v in values]
        descriptions = [v[2] for v in values]
        high = max(temps)
        low = min(temps)
        summary = most_common(descriptions)

        forecast_rows.append([date, f"{high}/{low} {units[unit]["temp"]}", summary])

    print("\nFORECAST OF NEXT 5 DAYS:")
    return tabulate(forecast_rows, tablefmt="fancy_grid")


def most_common(my_list):
    return max(set(my_list), key=my_list.count)
