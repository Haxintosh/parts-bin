from pydantic import BaseModel
from typing import List, Optional, Dict

class Component(BaseModel):
    mpn: str
    manufacturer: str
    distributor_id: str
    description: str
    package: str
    datasheet: Optional[str] = None
    category: str
    sub_category: str
    qty: int
    data: Optional[Dict[str, str]] = None
    parse_type: Optional[str] = None
    value: Optional[str] = None
    id : Optional[str] = None # UUID of the component

"""
{
    "mpn": "1234", # Manufacturer Part Number
    "manufacturer": "Texas Instruments" # Manufacturer
    "distributor_id": "1234", # Distributor ID
    "description": "A cool component", # Description
    "package": "SMD", # Package
    "datasheet": "http://example.com", # Datasheet
    "category": "IC", # Category
    "sub_category": "OpAmp", # Sub Category
    "qty": 100, # Quantity
    "data": { # Data (parsed from description)
        "voltage": "5V",
        "current": "10mA"
    }
    "id" : "UUIDv4"
}
"""
# This is the schema for the component update request
class ComponentUpdate(BaseModel):
    mpn: Optional[str] = None
    manufacturer: Optional[str] = None
    distributor_id: Optional[str] = None
    description: Optional[str] = None
    package: Optional[str] = None
    datasheet: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    qty: Optional[int] = None
    data: Optional[Dict[str, str]] = None
    id : str # UUID of the component

class ComponentList(BaseModel):
    components: List[Component]

class HTTPResponse(BaseModel):
    message: str
