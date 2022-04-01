import requests
from bs4 import BeautifulSoup
from rightmove_scraper.constants import BASE_URL
from typing import Optional


def get_and_parse(*args, **kwargs) -> BeautifulSoup:
    res = requests.get(*args, **kwargs)
    res.raise_for_status()
    return BeautifulSoup(res.text, "html.parser")


def find_and_strip(inp: BeautifulSoup, kind: str, class_: str) -> Optional[str]:
    try:
        return inp.find(kind, class_=class_).get_text().strip()
    except AttributeError:
        return


def get_url(appar_no: BeautifulSoup) -> str:
    return BASE_URL + appar_no.find('a', class_='propertyCard-link')['href']
