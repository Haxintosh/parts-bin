from typing_extensions import List
from fastapi import status, HTTPException
from typing import Optional
from uuid import uuid4

from app import database as db
from app.api.component.schemas import Component, ComponentUpdate, ComponentList, HTTPResponse
from app.config import COMPONENT_COLLECTION_NAME, APP_DB_NAME

db_client = db.DBClient.get_client()
component_collection = db_client[APP_DB_NAME][COMPONENT_COLLECTION_NAME]

# Create
async def db_create_component(component: Component) -> Component:
    if await isInDB(component.mpn):
        raise HTTPException(409, detail="Component already exists")
    component.id = str(uuid4())
    component_collection.insert_one(component)
    return component

async def db_create_bulk_component(array:ComponentList) -> ComponentList:
    return_components = ComponentList(components=[])
    for i in array.components:
        if await isInDB(i.mpn):
            c = component_collection.find_one({"mpn":i.mpn})
            qty = c.__dict__["qty"]
            component_collection.find_one_and_update({"mpn":i.mpn}, {"$set": {"qty": qty}})
            print(qty)
        else:
            ComponentList.components.append(await db_create_component(i))
    return return_components

# Read
async def db_get_component_by_id(uuid: str) -> Component:
    component = component_collection.find_one({"id":uuid})
    if component:
        return component
    raise HTTPException(404, detail="Component not found")

async def db_get_component_by_mpn(mpn: str) -> Component:
    component = component_collection.find_one({"mpn":mpn})
    if component:
        return component
    raise HTTPException(404, detail="Component not found")


async def db_get_all_components() -> ComponentList:
    components = component_collection.find({})
    return ComponentList(components=list(components))

# Update
async def db_update_component(update:ComponentUpdate) -> Component:
    sanitized_update = {}
    for k, v in update:
        print(k, v)
        if v == None or k == "id":
            pass
        else:
            sanitized_update[k] = v
    if await isInDB_id(update.id):
        component=component_collection.find_one_and_update(filter={"id":update.id}, update={"$set":sanitized_update})
        return component
    else:
        raise HTTPException(404, detail="Component not found")

# Delete
async def db_delete_single_component(uuid:str) -> HTTPResponse:
    if await isInDB_id(uuid):
        component_collection.delete_one({"id":uuid})
        return HTTPResponse(message="Deleted")
    raise HTTPException(404, detail="Component not found")

async def db_delete_bulk_component(array: List[str]) -> HTTPResponse:
    for i in array:
       await db_delete_single_component(i)
    return HTTPResponse(message = f"Deleted {len(array)} components")

# Utils
async def isInDB(mpn):
    if component_collection.find_one({"mpn":mpn}):
        return True
    return False

async def isInDB_id(id):
    if component_collection.find_one({"id":id}):
        return True
    return False
