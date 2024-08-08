from fastapi import status, HTTPException
from typing import Optional
from uuid import uuid4

from app import database as db
from app.api.component.schemas import Component, ComponentUpdate, ComponentList, HTTPResponse
from app.config import COMPONENT_COLLECTION_NAME, APP_DB_NAME

db_client = db.DBClient.get_client()
component_collection = db_client[APP_DB_NAME][COMPONENT_COLLECTION_NAME]

# Create
def db_create_component(component: Component) -> HTTPResponse:
    if isInDB(component.mpn):
        raise HTTPException(409, detail="Component already exists")
    insert_e = component.dict()
    insert_e["_id"] = str(uuid4())
    component_collection.insert_one(insert_e)
    return HTTPResponse(message="Component created")

# Read
def db_get_component_by_id(uuid: str) -> Component:
    component = component_collection.find_one({"_id":uuid})
    if component:
        return component
    raise HTTPException(404, detail="Component not found")

def db_get_component_by_mpn(mpn: str) -> Component:
    component = component_collection.find_one({"mpn":mpn})
    if component:
        return component
    raise HTTPException(404, detail="Component not found")


def db_get_all_components() -> ComponentList:
    components = component_collection.find({})
    return ComponentList(components=list(components))

# Utils
def isInDB(mpn):
    if component_collection.find_one({"mpn":mpn}):
        return True
    return False
