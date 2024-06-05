from pydantic import BaseModel

class User(BaseModel):
    cccd: str
    password: str
    name: str
    birthdate: str
    address: str
    gender: str
    hadgdc: bool

class GDC(BaseModel):
    cccd: str
    CP_username: str
    isVerified: bool
    gdc_Id: str

class ChingsPhu(BaseModel):
    CP_username: str
    password: str
    name: str