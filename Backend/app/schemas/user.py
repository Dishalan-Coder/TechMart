from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    phone: str | None = None
    address: str | None = None


class UpdateProfileRequest(BaseModel):
    name: str | None = None
    phone: str | None = None
    address: str | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str