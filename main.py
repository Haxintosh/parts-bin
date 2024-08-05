import os

from pymongo import MongoClient
from dotenv import load_dotenv

import bom_parsers

load_dotenv()

MAIN_DB_URI= os.getenv("MONGODB_CONN_URI")

def get_component_db():
    client = MongoClient(MAIN_DB_URI)
    return client['components']

if __name__ == '__main__':
    rows = bom_parsers.parse_csv("tests/LCSC.csv")
    bom_parsers.lcsc_parser(rows)
    # db = get_component_db()
    # capacitor_collection = db['capacitors']
    #
    # component_1 = {
    #     "MFN": "CL05A105KP5NNNC",
    #     "Manufacturer": "Samsung Electro-Mechanics",
    #     "Distributor_ID": ["C14445"],
    #     "Type": "Capacitor, MLCC",
    #     "Package": "0402",
    #     "Value": "1uF"
    # }
    #
    # capacitor_collection.insert_one(component_1)
