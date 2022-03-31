import json
from bs4 import BeautifulSoup


def link_to_id(link: str) -> str:
    link = link.replace('https://www.rightmove.co.uk/properties/', '')
    return link.split('#')[0]


def extract_additional_info(page: BeautifulSoup) -> dict:
    for el in page.find_all('script'):
        if 'window.PAGE_MODEL' in el.decode():
            to_parse = el.decode().replace('<script>\n    window.PAGE_MODEL = ', '').replace('\n</script>', '')
            output = json.loads(to_parse)
            break
    propdat = output['propertyData']
    return dict(
        lat=propdat['location']['latitude'],
        lng=propdat['location']['longitude'],
        bathrooms=propdat['bathrooms'],
        bedrooms=propdat['bedrooms'],
        propdat=propdat
    )