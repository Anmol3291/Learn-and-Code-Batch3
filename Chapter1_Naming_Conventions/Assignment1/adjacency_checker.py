import json


def load_adjacent_country_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON in the file '{file_path}'.")
        return {}


def get_adjacent_countries(country_code, country_data):
    country_code = country_code.upper()
    country_info = country_data.get(country_code)

    if not country_info:
        return f"Error: Country code '{country_code}' is not recognized."

    country_name = country_info["name"]
    adjacent_countries = country_info["adjacent"]

    if not adjacent_countries:
        return f"{country_name} has no adjacent countries."

    adjacent_list = ""
    for country in adjacent_countries:
        adjacent_list += country + ", "
    return f"{country_name} is adjacent to: {adjacent_list}."


def main():
    country_data = load_adjacent_country_data("adjacent_country_data.json")
    if not country_data:
        return

    while True:
        country_code = input("Enter a country code (or 'exit' to quit): ").strip()

        if country_code.lower() == "exit":
            break

        result = get_adjacent_countries(country_code, country_data)
        print(result)


if __name__ == "__main__":
    main()
