from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str

class User(BaseModel):
    name: str