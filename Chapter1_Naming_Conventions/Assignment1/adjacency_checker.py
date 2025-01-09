import json


def load_adjacency_countries_list():
    with open("adjacent_countries_data.json") as f:
        adjacency_countries = json.load(f)
    return adjacency_countries


def main():
    user_entered_country_code = input("Enter the country code: ")
    adjacent_countries_data = load_adjacency_countries_list()
    if user_entered_country_code in adjacent_countries_data:
        entered_country_name = adjacent_countries_data[user_entered_country_code][
            "name"
        ]
        adjacent_countries_list = adjacent_countries_data[user_entered_country_code][
            "adjacent"
        ]

        print(f"\nThe adjacent countries of {entered_country_name} are:\n\t")
        for country in adjacent_countries_list:
            print(country)
    else:
        print(
            "The country code is not found in the database or you have entered an invalid country code.please try again."
        )


main()
