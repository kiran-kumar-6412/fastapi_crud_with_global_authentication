from pydantic import BaseModel, EmailStr
from typing import Optional

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
class ShowUser(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    role: str

    class Config:  # ✅ Fixed from `config()` to `Config`
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username: str
    role: str


class User_update(BaseModel):
    email:Optional[EmailStr]
    role:Optional[str]="vendor"
