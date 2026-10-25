from pydantic import BaseModel, Field, field_validator


class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)
    password: str = Field(..., max_length=125, min_length=6)

    @field_validator("login", "password")
    def value_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Login name cannot be empty")

        return v


class UserResponse(UserRequest):
    model_config = {"from_attributes": True}
    id: int
    
class AuthResponse(BaseModel):
    model_config = {"from_attributes": True}
    access_token: str
    refresh_token: str


class HashedPassword(BaseModel):
    password: str = Field(..., max_length=255)


class RefreshTokenResponse(BaseModel):
    refresh_token: str
