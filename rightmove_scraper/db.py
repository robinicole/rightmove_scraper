from pymongo import MongoClient
from rightmove_scraper.flat_desc_scraper import link_to_id, extract_additional_info
from rightmove_scraper.helpers import get_and_parse


class FlatStore:
    """
    An interface in front of MongoDB
    """
    def __init__(self, client=None, db='main', collection='rightmove'):
        self.client = client or MongoClient()
        db_ = self.client[db]
        self.coll = db_[collection]
    
    def force_update(self, link) -> dict:
        page = extract_additional_info(get_and_parse(link))
        page['id'] = link_to_id(link)
        self.coll.delete_one({"id": page['id']})
        self.coll.insert_one(page)
        return page
    
    def get(self, link):
        _id = link_to_id(link)
        output = self.coll.find_one({'id': _id})
        if output:
            return output
        return self.force_update(link)