import requests
import pandas as pd


class CountryAPI:
    def __init__(self, url="https://restcountries.com/v3.1/all"):
        self.url = url

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def display_data(self):
        data = self.fetch_data()
        countries = []
        for country in data:
            country_name = country.get("name", {}).get("common", "N/A")
            capital = country.get("capital", ["N/A"])[0]
            flag_url = country.get("flags", {}).get("png", "N/A")
            countries.append([country_name, capital, flag_url])

        df = pd.DataFrame(countries, columns=["Country Name", "Capital", "Flag URL"])
        print(df)


if __name__ == "__main__":
    country_api = CountryAPI()
    country_api.display_data()
