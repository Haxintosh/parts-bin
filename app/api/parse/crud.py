from typing_extensions import List
from fastapi import status, HTTPException
from typing import Optional
from uuid import uuid4
from datetime import datetime

from app import database as db
from app.api.component.schemas import Component, ComponentUpdate, ComponentList, HTTPResponse
from app.config import COMPONENT_COLLECTION_NAME, APP_DB_NAME

db_client = db.DBClient.get_client()
component_collection = db_client[APP_DB_NAME][COMPONENT_COLLECTION_NAME]

# Create
async def insert_hash(hash):
    doc = {
        "hash": hash,
        "timestamp": datetime.now()
    }
    component_collection.insert_one(doc)
    return doc

async def check_hash(hash):
    if component_collection.find_one({"hash":hash}):
        return True
    return False
