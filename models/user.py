import uuid as sysid
from datetime import datetime, timezone, date
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class ProjectStatus(str, Enum):
    PLANNED = "Planned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"


class Project(BaseModel):
    project_name: str = Field(..., min_length=3, max_length=50)
    project_description: str = Field(..., min_length=10)
    project_status: ProjectStatus


class User(BaseModel):
    uuid: Optional[str] = Field(default_factory=lambda: str(sysid.uuid1()))
    name: str
    first_name: str
    last_name: str
    dob: date
    age: int
    username: str = Field(min_length=7)
    email: EmailStr
    phone: List[int]
    job: str
    skills: List[str]
    salary: Optional[float] = None
    projects: Optional[List[Project]] = []
    languages_known: List[str]
    notice_period: int = Field(gt=0, lt=6)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "uuid": str(sysid.uuid1()),
                "name": "John Doe",
                "first_name": "John",
                "last_name": "Doe",
                "dob": "2003-03-25",
                "age": 30,
                "username": "johndoe99",
                "email": "john.doe@example.com",
                "phone": [1234567890],
                "job": "Software Engineer",
                "skills": ["Python", "FastAPI", "Docker"],
                "salary": 85000.00,
                "projects": [
                    {
                        "project_name": "Inventory Management",
                        "project_description": "System for tracking stock levels.",
                        "project_status": "Completed"
                    },
                    {
                        "project_name": "CRM Integration",
                        "project_description": "Integration with Salesforce.",
                        "project_status": "In Progress"
                    }
                ],
                "languages_known": ["English", "Spanish"],
                "notice_period": 2,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
