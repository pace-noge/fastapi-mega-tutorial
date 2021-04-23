from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    acces_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None