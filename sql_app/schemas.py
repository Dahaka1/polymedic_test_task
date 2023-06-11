from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
	title: str | None = Field(
		default=None, max_length=50
	)


class DepartmentCreate(DepartmentBase):
	pass


class Department(DepartmentBase):
	id: int

	class Config:
		orm_mode = True


class FacultyBase(BaseModel):
	title: str | None = Field(
		default=None,
		max_length=50
	)
	department_id: int


class FacultyCreate(FacultyBase):
	pass


class Faculty(FacultyBase):
	id: int

	class Config:
		orm_mode = True


class StudentGroupBase(BaseModel):
	title: str | None = Field(
		default=None,
		max_length=50
	)
	faculty_id: int


class StudentGroupCreate(StudentGroupBase):
	pass


class StudentGroup(StudentGroupBase):
	id: int

	class Config:
		orm_mode = True


class StudentBase(BaseModel):
	fullname: str = Field(
		max_length=50
	)
	student_group_id: int | None = None


class StudentCreate(StudentBase):
	pass


class Student(StudentBase):
	id: int

	class Config:
		orm_mode = True


