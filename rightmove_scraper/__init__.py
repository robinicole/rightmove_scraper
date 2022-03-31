import pandas as pd
from tqdm.auto import tqdm

from rightmove_scraper.db import FlatStore
from rightmove_scraper.search_page_scraper import get_flats_html_and_parse
from .constants import ISLINGTON_BOROUGH, CAMDEN_BOROUGH, BERM_BOROUGH


def generate_df(borough: str, radius: str, flat_store=None, mongo_client=None) -> pd.DataFrame:
    flat_store = flat_store or FlatStore(mongo_client)
    search_page_flats_df = get_flats_html_and_parse(borough, radius)
    links_in_search_page = search_page_flats_df.link
    return pd.concat((pd.DataFrame([flat_store.get(l) for l in tqdm(links_in_search_page)]), search_page_flats_df),
                     axis=1)
