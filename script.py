from rightmove_scraper import generate_df, ISLINGTON_BOROUGH, BERM_BOROUGH, CAMDEN_BOROUGH
from pymongo import MongoClient
import os
MONGO_URL = os.environ.get('MONGO_URL')
mongo_client = MongoClient(MONGO_URL)
generate_df(ISLINGTON_BOROUGH, radius='1', mongo_client=mongo_client)
generate_df(BERM_BOROUGH, radius='1', mongo_client=mongo_client)
generate_df(CAMDEN_BOROUGH, radius='1', mongo_client=mongo_client)