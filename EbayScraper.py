from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json


class EbayScraper:
    def __init__(self, url):
        self.url = url

    def fetch_page(self):
        response = Request(self.url)
        webpage = urlopen(response).read()
        return webpage

    def parse_data(self, html):
        soup = BeautifulSoup(html, "html.parser")
        result = {}

        title_element = soup.find("h1", {"class": "x-item-title__mainTitle"})
        result["title"] = title_element.text.strip() if title_element else "N/A"

        price_element = soup.find("div", {"class": "x-price-primary"})
        result["price"] = price_element.text.strip() if price_element else "N/A"

        result["product_url"] = self.url

        seller_element = soup.find(
            "div", {"class": "x-sellercard-atf__info__about-seller"}
        ).find("a")["href"]
        result["seller"] = seller_element if seller_element else "N/A"

        shipping_price_element = soup.find(
            "div", {"class": "ux-labels-values__values-content"}
        ).find("span", {"class": "ux-textspans ux-textspans--BOLD"})
        result["shipping_price"] = (
            shipping_price_element.text.strip() if shipping_price_element else "N/A"
        )

        return result

    @staticmethod
    def save_to_file(result_dict, filename="ebay_product_data.json"):
        with open(filename, "w") as file:
            json.dump(result_dict, file, indent=4)

    def display_data(self):
        html = self.fetch_page()
        result = self.parse_data(html)
        print(json.dumps(result, indent=4))


if __name__ == "__main__":
    url = "https://www.ebay.com/itm/226231943139?itmmeta=01J2BWXHWBSYJHGMDATE9RGWPT&hash=item34ac797fe3:g:H~0AAOSwFr5mit1C"
    scraper = EbayScraper(url)
    page = scraper.fetch_page()
    data = scraper.parse_data(page)
    scraper.save_to_file(data)
