import argparse
from data_formatter import give_current_weather
from api_and_storage import load_recent


def get_args():
    parser = argparse.ArgumentParser(description="Welcome to my Weather App")

    parser.add_argument("--city", metavar="city")
    parser.add_argument("--zipcode", nargs=2, metavar="zipcode and countrycode")
    parser.add_argument("--latlon", nargs=2, metavar="latitude and longitude")

    parser.add_argument("--mode", choices=["weather", "forecast"])
    parser.add_argument("--unit", choices=["c", "f"])
    parser.add_argument("--recent", action="store_true")
    parser.add_argument("--gethelp", action="store_true")

    if parser.parse_args().gethelp:
        print(
            """
            You can use my script either by executing it,
            or using the following CLI arguments:

            --city(followed by city name)
            --zipcode(followed by zip-code and country-code)
            --latlon(followed by geographical coordinated(latitide and longitude))

            EXAMPLE:

            py main.py --city Lahore
            py main.py --zipcode 50400 pk
            py main.py --latlon 45.133 7.367

            UNITS:

            by default, the units used are metric
            but you can specify it by using --unit argument
            (C(metric) or F(imperial))

            EXAMPLE:

            py main.py --name Lahore --unit F
            """
        )

    if parser.parse_args().recent:
        data_list = load_recent()

        print("\nfollowing is the history of 5 recent forecasts:\n")
        for data in data_list:
            print(give_current_weather(data, "metric"))

    return parser.parse_args()


def user_input():
    print("1. City Name    2. ZIP Code    3. Geographical Coordinates")
    main_option = input("Enter the method by which you want your data: ")

    if main_option == "1":
        method = "city"
        city_name_input = input("Enter name of your preferred city: ")
        unit_input = input_validation("unit", ["c", "f"])
        mode_input = input_validation("mode of weather", ["weather", "forecast"])
        unit = "imperial" if unit_input == "f" else "metric"
        return method, (mode_input, city_name_input, unit)

    elif main_option == "2":

        method = "zipcode"
        zipcode_input = int(input("Enter zip code of your preferred city: "))
        country_code_input = input("Enter valid country code: ")
        unit_input = input_validation("unit", ["c", "f"])
        mode_input = input_validation("mode of weather", ["weather", "forecast"])
        unit = "imperial" if unit_input == "f" else "metric"
        return method, (mode_input, zipcode_input, country_code_input, unit)

    elif main_option == "3":

        method = "latlon"
        lat_input = float(input("Enter preferred latitude value: "))
        lon_input = float(input("Enter preferred latitude value: "))
        unit_input = input_validation("unit", ["c", "f"])
        mode_input = input_validation("mode of weather", ["weather", "forecast"])
        unit = "imperial" if unit_input == "f" else "metric"
        return method, (mode_input, lat_input, lon_input, unit)

    else:
        print("Invalid Inputs...Try again later.")
        return ""


def input_validation(choice, choices):
    choice_input = ""
    choice_input = input(
            f"Enter your preferred {choice} ({choices[0]} or {choices[-1]}): "
        ).lower()

    while choice_input not in choices:
        choice_input = input(
            f"Invalid Input! Enter a valid option({choices[0]} or {choices[-1]}): "
        ).lower()
    return choice_input


if __name__ == "__main__":
    my_args = get_args()

    if not any([my_args.city, my_args.zipcode, my_args.latlon]):
        print(user_input())
    else:
        print(f"{my_args}")
        print(vars(my_args).values()[1])
