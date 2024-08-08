from fastapi import APIRouter

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
    responses={404: {"description": "Not found"}},
)
