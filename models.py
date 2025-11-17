from typing import List, Dict, Optional, Annotated
from pydantic import BaseModel, Field, computed_field, field_validator, model_validator


class Employee(BaseModel):
    id: Annotated[int, Field(
        ...,
        gt=0,
        description='ID of the employee',
        examples=['1', '2']
    )]
    name: Annotated[str, Field(
        ...,
        min_length=3,
        max_length=50,
        description='Name of the employee',
        examples=['John Doe', 'Jane Doe']
    )]
    age: Annotated[int, Field(
        ...,
        ge=18,
        le=58,
        description='Age of the employee',
        examples=[18, 19, 20, 58]
    )]
    department: Annotated[str, Field(
        ...,
        description='Department of the employee',
        examples=['dept1', 'dept2']
    )]
