from pydantic import BaseModel

class ParseRequest(BaseModel):
    type: str
    bypass: bool
    data: str # CSV
