from pydantic import BaseModel


class Week(BaseModel):
    week: int


class Semester(BaseModel):
    semester: int
    start_date: str
    year_start: int
    year_end: int
