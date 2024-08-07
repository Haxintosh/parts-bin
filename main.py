import os

from pymongo import MongoClient
from dotenv import load_dotenv

from openai import OpenAI

import bom_parsers
import utils

from typing import Union
from fastapi import FastAPI

load_dotenv()

MAIN_DB_URI= os.getenv("MONGODB_CONN_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

fastapi_app = FastAPI()

client = MongoClient(MAIN_DB_URI)
db = client['components']

def get_openai_client():
    client = OpenAI(api_key=OPENAI_API_KEY)
    return client

@fastapi_app.get('/api/components/get_all')
def get_all():
    return utils.get_all_components(db)

@fastapi_app.get('/api/components/{type}')
def get_by_type(type:str):
    return utils.get_components_by_type(db, type)

@fastapi_app.get('/api/components/mpn/{mpn}')
def get_by_mpn(mpn:str):
    return utils.get_components_by_mpn(db, mpn)

# @fastapi_app.post('/api/components/add')
# def add_component(component: Union[bom_parsers.Component, dict]):
#     if isinstance(component, dict):
#         component = bom_parsers.Component(**component)
#     return utils.add_component(db, component.type, component.dict())

@fastapi_app.post('/api/components/add')
def add_component(component: dict):
    return utils.add_component(db, component['type'], component)

@fastapi_app.post('/api/components/change_qty')
def change_qty(type:str, mpn:str, qty:int):
    return utils.change_component_qty(db, type, mpn, qty)

@fastapi_app.post('/api/components/add_from_parsed_bom')
def add_from_parsed_bom(parsed_bom: dict):
    return utils.add_components_from_parsed_bom(db, parsed_bom)

@fastapi_app.get('/api/components/find/{str}')
def find(str:str):
    return utils.db_find_from_str(db, str)

if __name__ == '__main__':
    client = get_openai_client()