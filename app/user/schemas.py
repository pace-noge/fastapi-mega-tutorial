from pydantic import BaseModel

class UserBase(BaseModel):
    """
    Base models  for user
    """
    username: str
    email: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    """
    When create new user, password must be supplied.
    """
    password: str



class User(UserBase):
    """
    When display or get the user we need to include the id
    but without password
    """
    id: int


class ChangePassword(BaseModel):
    """
    Schema for reset password
    """
    current_password: str
    new_password: str
