from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class GetCoursesRequest(BaseModel):
    student_id: UUID
    offset: Optional[int] = 0  # Default to the first page
    page_size: Optional[int] = 10  # Default number of courses per page