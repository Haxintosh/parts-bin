from fastapi import APIRouter, Response, status, HTTPException
from app.api.component.schemas import Component, ComponentList, ComponentUpdate, HTTPResponse
from app.api.component.crud import db_create_bulk_component, db_create_component, db_delete_bulk_component, db_delete_single_component, db_get_all_components, db_get_component_by_id, db_update_component, isInDB, db_get_component_by_mpn
from typing import List
router = APIRouter(
    prefix="/components",
    tags=["components"],
    responses={404: {"description": "Not found"}},
)

# Create
@router.post("/create")
async def create_component(component: Component) -> Component:
    try:
        return await db_create_component(component)
    except HTTPException as e:
        raise e

@router.post("/create/bulk")
async def create_bulk_component(array:ComponentList) -> ComponentList:
    try:
        return await db_create_bulk_component(array)
    except HTTPException as e:
        raise e

# Read
@router.get("/get/id/{uuid}")
async def get_component_by_id(uuid:str) -> Component:
    try:
        return await db_get_component_by_id(uuid)
    except HTTPException as e:
        raise e

@router.get("/get/mpn/{mpn}")
async def get_component_by_mpn(mpn:str) -> Component:
    try:
        return await db_get_component_by_mpn(mpn)
    except HTTPException as e:
        raise e

@router.get("/get/all")
async def get_all_components() -> ComponentList:
    return await db_get_all_components()

# Update
@router.put("/update")
async def update_single_component(component:ComponentUpdate) -> Component:
    try:
        return await db_update_component(component)
    except HTTPException as e:
        raise e

# Delete
@router.delete("/delete/id/{uuid}")
async def delete_single_component(uuid:str) -> HTTPResponse:
    try:
        return await db_delete_single_component(uuid)
    except HTTPException as e:
        raise e

@router.delete("/delete/bulk")
async def delete_bulk_component(array:List[str]) -> HTTPResponse:
    try:
        return await db_delete_bulk_component(array)
    except HTTPException as e:
        raise e
