import os

from pymongo import MongoClient
from dotenv import load_dotenv

from openai import OpenAI

import bom_parsers
import utils
load_dotenv()

MAIN_DB_URI= os.getenv("MONGODB_CONN_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_component_db():
    client = MongoClient(MAIN_DB_URI)
    return client['components']

def get_openai_client():
    client = OpenAI(api_key=OPENAI_API_KEY)
    return client

if __name__ == '__main__':
    client = get_openai_client()
    rows = bom_parsers.parse_csv("tests/LCSC.csv")
    c = bom_parsers.lcsc_parser(rows)
    bom_parsers.ai_parser(c['Other'][0], client)
    # print(c['Other'][0])
    # db = get_component_db()
    # utils.add_components_from_parsed_bom(db, c)

