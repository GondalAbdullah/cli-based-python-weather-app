import os
from dotenv import load_dotenv
from inputs import get_args, user_input
from api_and_storage import fetch_data, log_error, save_recent
from data_formatter import give_current_weather, give_forecast
from cache import generate_cache_key, get_cached_data, save_to_cache

load_dotenv()
API_KEY = os.getenv("MY_API_KEY")
CITY_BASE_URL = os.getenv("CITY_BASE_URL")
ZIPCODE_BASE_URL = os.getenv("ZIPCODE_BASE_URL")
LATLON_BASE_URL = os.getenv("COORDINATES_BASE_URL")


def main():
    my_args = get_args()
    url = ""
    unit = ""
    mode = ""
    key = ""

    if any([my_args.recent, my_args.gethelp]):
        return

    if not any(
        [my_args.city, my_args.zipcode, my_args.latlon]
    ):
        try:

            method, input_tuple = user_input()

            if method == "city":
                first, second, last = input_tuple
                mode = first
                unit = last
                url = CITY_BASE_URL.format(
                    mode=mode,
                    city_name=second,
                    api_key=API_KEY,
                    unit=last,
                )
                key = generate_cache_key(mode=mode, unit=unit, city=second)

            elif method == "zipcode":
                first, second, third, last = input_tuple
                mode = first
                unit = last
                url = ZIPCODE_BASE_URL.format(
                    mode=mode,
                    zip_code=second,
                    country_code=third,
                    api_key=API_KEY,
                    unit=last
                )
                key = generate_cache_key(
                    mode=mode, unit=unit, zipcode=second, countrycode=third
                )

            elif method == "latlon":
                first, second, third, last = input_tuple
                mode = first
                unit = last
                url = LATLON_BASE_URL.format(
                    mode=mode,
                    lat=second,
                    lon=third,
                    api_key=API_KEY,
                    unit=last
                )
                key = generate_cache_key(mode=mode, unit=unit, lat=second, lon=third)

            # mode = "forecast" if mode == "forecast" else "weather"

        except Exception as e:
            print(f"ERROR OCCURED with interactive input: {e}")
            log_error(f"ERROR OCCURED with interactive input: {e}")

    if my_args:
        try:

            unit = "imperial" if my_args.unit == "f" else "metric"
            mode = "forecast" if my_args.mode == "forecast" else "weather"

            if my_args.city:
                url = CITY_BASE_URL.format(
                    mode=mode,
                    city_name=my_args.city,
                    api_key=API_KEY,
                    unit=unit
                )
                key = generate_cache_key(mode=mode, unit=unit, city=my_args.city)

            elif my_args.zipcode:
                zip_code, country_code = my_args.zipcode
                url = ZIPCODE_BASE_URL.format(
                    mode=mode,
                    zip_code=zip_code,
                    country_code=country_code,
                    api_key=API_KEY,
                    unit=unit
                )
                key = generate_cache_key(
                    mode=mode, unit=unit, zipcode=zip_code, countrycode=country_code
                )

            elif my_args.latlon:
                lat, lon = my_args.latlon
                url = LATLON_BASE_URL.format(
                    mode=mode,
                    lat=lat,
                    lon=lon,
                    api_key=API_KEY,
                    unit=unit
                )
                key = generate_cache_key(mode=mode, unit=unit, lat=lat, lon=lon)

        except Exception as e:
            print(f"ERROR OCCURED in CMD arguments: {e}")
            log_error(f"ERROR OCCURED in CMD arguments: {e}")

    cached = get_cached_data(key)

    if cached:

        try:
            print("\nUsing cached data...\n")
            if mode == "forecast":
                print(give_forecast(cached, unit))
            else:
                print(give_current_weather(cached, unit))
        except Exception as e:
            print(f"Error occured while retrieving cached data: {e}")
            log_error(f"Error occured while retrieving cached data: {e}")

    else:

        try:
            print("Getting New data...\n")
            data = fetch_data(url)
            if not data:
                raise ValueError("\nNo data found from API\n")

            save_to_cache(key, data)
            cached = get_cached_data(key)
            if mode == "forecast":
                print(give_forecast(cached, unit))
            else:
                print(give_current_weather(cached, unit))
                save_recent(data)

        except Exception as e:
            print(f"Error occured while retrieving new data: {e}")
            log_error(f"Error occured while retrieving new data: {e}")


if __name__ == "__main__":
    main()
