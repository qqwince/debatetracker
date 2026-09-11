
from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)
    
class UserResponse(UserRequest):
    model_config = {"from_attributes": True}
    id: int