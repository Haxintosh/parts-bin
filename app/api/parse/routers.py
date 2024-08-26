from fastapi import APIRouter

import hashlib

from app.api.component.routers import create_bulk_component
from app.api.component.schemas import Component, ComponentList, ComponentUpdate, HTTPResponse
from app.api.parse.schemas import ParseRequest
from app.api.parse.crud import insert_hash, check_hash
from app.parser.LCSC.bom_parser import lcsc_parser
from app.api.component.crud import db_create_bulk_component

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
    responses={404: {"description": "Not found"}},
)

# Create (ish)
@router.post("/parse/bom")
async def parse_bom(req: ParseRequest) -> ComponentList:
    hash = hashlib.md5(req.data.encode()).hexdigest()
    if not req.bypass:
        if check_hash(hash):
            return ComponentList(components=[])
        await insert_hash(hash)

    match req.type:
        case "lcsc":
            return lcsc_parser(req.data)
        case _:
            return ComponentList(components=[])

@router.post("/parse/save/bom")
async def parse_bom_and_save(req: ParseRequest) -> ComponentList:
    hash = hashlib.md5(req.data.encode()).hexdigest()
    if not req.bypass:
        if check_hash(hash):
            return ComponentList(components=[])
        await insert_hash(hash)

    match req.type:
        case "lcsc":
            data = lcsc_parser(req.data)
            await create_bulk_component(data)
            return data
        case _:
            return ComponentList(components=[])
