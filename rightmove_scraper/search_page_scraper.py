import requests
from bs4 import BeautifulSoup
from typing import List
import pandas as pd

from .constants import HEADERS
from .helpers import find_and_strip, get_and_parse, get_url


def sarch_page_parse_flat_html(apartment_no: BeautifulSoup) -> dict:
    """
    Proces a flat card and extract data
    """
    apartment_info = apartment_no.find("a", class_="propertyCard-link")
    return dict(
        apartment_info=apartment_info,
        link="https://www.rightmove.co.uk" + apartment_info.attrs["href"],
        address= find_and_strip(apartment_info, "address", class_="propertyCard-address"),
        description = find_and_strip(apartment_info, "h2", class_="propertyCard-title"),
        price = find_and_strip(apartment_no, "div", class_="propertyCard-priceValue"),
        branch_name=find_and_strip(apartment_no, 'span', class_="propertyCard-branchSummary-branchName"),
        url=get_url(apartment_no),
        image = apartment_no.find('img')['src'],
        add_date = find_and_strip(apartment_info, 'span', class_="propertyCard-contactsAddedOrReduced"),
    )


def sarch_page_get_flat_html(borough: str, radius: str) -> List[BeautifulSoup]:
    """
    Extract all the flat cards in the search page into a list
    """
    flats_list = []
    index = 0
    while True:
        # request our webpage
        # res = requests.get(BASE_URL, headers=headers, params=params)
        if index == 0:
            rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&maxDaysSinceAdded=14&keywords=&radius={radius}"
        elif index != 0:
            rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&index={index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&maxDaysSinceAdded=14&furnishTypes=&keywords=&radius={radius}"

        # request our webpage
        try:
            soup = get_and_parse(rightmove, headers=HEADERS)
        except requests.HTTPError:
            break
        apartments = soup.find_all("div", class_="l-searchResult is-list")
        number_of_listings = soup.find(
            "span", {"class": "searchHeader-resultCount"}
        )
        number_of_listings = number_of_listings.get_text()
        number_of_listings = int(number_of_listings.replace(",", ""))
        for flats_no in apartments:
            flats_list.append(flats_no)
            index += 1

        if index >= number_of_listings:
            break
        print(f'processed {index}/{number_of_listings} items')
    return flats_list


def get_flats_html_and_parse(borough: str, radius: str):
    flats_list = sarch_page_get_flat_html(borough, radius)
    return pd.DataFrame([sarch_page_parse_flat_html(el) for el in flats_list])