from fastapi import APIRouter, Response, status, HTTPException
from app.api.component.schemas import Component, ComponentList, HTTPResponse
from app.api.component.crud import db_create_component, db_get_all_components, db_get_component_by_id, isInDB

router = APIRouter(
    prefix="/components",
    tags=["components"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def say_hello():
    return {"message": "Hello, World!"}

@router.post("/create")
async def create_component(component: Component) -> HTTPResponse:
    try:
        return db_create_component(component)
    except HTTPException as e:
        raise e

@router.get("/get/id/{uuid}")
async def get_component_by_id(uuid:str) -> Component:
    try:
        return db_get_component_by_id(uuid)
    except HTTPException as e:
        raise e

@router.get("/get/mpn/{mpn}")
async def get_component_by_mpn(mpn:str) -> Component:
    try:
        return db_get_component_by_mpn(mpn)
    except HTTPException as e:
        raise e

@router.get("/get/all")
async def get_all_components() -> ComponentList:
    return db_get_all_components()
