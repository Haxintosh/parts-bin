import os

from pymongo import MongoClient
from dotenv import load_dotenv

import bom_parsers
import utils
load_dotenv()

MAIN_DB_URI= os.getenv("MONGODB_CONN_URI")

def get_component_db():
    client = MongoClient(MAIN_DB_URI)
    return client['components']

if __name__ == '__main__':
    rows = bom_parsers.parse_csv("tests/LCSC.csv")
    c = bom_parsers.lcsc_parser(rows)
    db = get_component_db()
    utils.add_components_from_parsed_bom(db, c)

