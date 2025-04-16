from pydantic import BaseModel, EmailStr
from typing import Optional,List

# ✅ Base schema for user
class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = True
    role: str="vendor"  # Example: "super_admin", "admin", or "vendor"

# ✅ Schema for user creation (includes password)
class UserCreate(UserBase):
    password: str  # Only required during user creation

# ✅ Schema for showing user (fixing class definition)
# ✅ Individual user schema
class UserListResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True  # Use this if you're on Pydantic v2
        

# ✅ Wrapper schema for the full response
class ShowUser(BaseModel):
    data: List[UserListResponse]
    status: bool
    message: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username: str
    role: str | None=None


class User_update(BaseModel):
    email:Optional[EmailStr]
    role:Optional[str]="vendor"


class UserActionSchema(BaseModel):
    create_data: Optional[UserCreate] = None
    update_data: Optional[User_update] = None

class MessageResponse(BaseModel):
    message: str