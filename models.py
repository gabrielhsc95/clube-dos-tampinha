from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class UserRole(str, Enum):
    Admin = "admin"
    Student = "student"
    Parent = "parent"
    Teacher = "teacher"
    NotAssigned = "n/a"


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


class Parent(BaseModel):
    user_id: str
    children: List[str]
    payments: List[str]


class Student(BaseModel):
    user_id: str
    parents: List[str]
    activities: List[str]


class Teacher(BaseModel):
    user_id: str
    students: List[str]


class Named(BaseModel):
    first_name: str
    last_name: str


class NamedParent(Named, Parent):
    pass


class NamedStudent(Named, Student):
    pass


class NamedTeacher(Named, Teacher):
    pass
