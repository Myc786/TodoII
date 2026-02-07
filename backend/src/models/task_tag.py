from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class TaskTag(SQLModel, table=True):
    """
    Association model for the many-to-many relationship between Task and Tag.

    Attributes:
        task_id: Foreign key referencing the task
        tag_id: Foreign key referencing the tag
    """
    task_id: uuid.UUID = Field(foreign_key="task.id", primary_key=True)
    tag_id: uuid.UUID = Field(foreign_key="tag.id", primary_key=True)