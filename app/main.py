from fastapi import FastAPI
from app.api.component import routers as component_routers

app = FastAPI()
app.include_router(component_routers.router)
