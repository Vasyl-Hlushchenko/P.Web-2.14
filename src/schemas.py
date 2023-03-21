from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    first_name: str = Field(min_length=3, strict=True, max_length=30)
    second_name: str = Field(min_length=3, strict=True, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=10, strict=True, max_length=13)
    birthaday: date
    description: str = Field(min_length=3, strict=True, max_length=250)
    authuser_id: int


class UserResponse(UserModel):
    id: int = 1
    first_name: str = "User"
    second_name: str = "Example"
    email: EmailStr = "example@gmail.com"
    phone: str= "0987654321"
    birthaday: date = date(year=1988, month=3, day=25)
    description: str = "Created first contact for test"
    authuser_id: int = 1

    class Config:
        orm_mode = True


class AuthUserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class AuthUserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class AuthUserResponse(BaseModel):
    user: AuthUserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
