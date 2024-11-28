from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserRole(str, Enum):
    Admin = "admin"
    Student = "student"
    Parent = "parent"
    Teacher = "teacher"


class User(BaseModel):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[UserRole]


class CompleteUser(BaseModel):
    id: str
    email: str
    password: str
    salt: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: Optional[UserRole]

    def to_user(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            role=self.role,
        )
