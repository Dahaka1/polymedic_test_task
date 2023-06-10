from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
	title: str


class DepartmentCreate(DepartmentBase):
	pass


class Department(DepartmentBase):
	id: int

	class Config:
		orm_mode = True


class FacultyBase(BaseModel):
	title: str | None = None
	department: Department


class FacultyCreate(FacultyBase):
	pass


class Faculty(FacultyBase):
	id: int

	class Config:
		orm_mode = True


class StudentGroupBase(BaseModel):
	title: str | None = None
	faculty: Faculty


class StudentGroupCreate(StudentGroupBase):
	pass


class StudentGroup(StudentGroupBase):
	id: int

	class Config:
		orm_mode = True


class StudentBase(BaseModel):
	fullname: str
	student_group: StudentGroup


class StudentCreate(StudentBase):
	pass


class Student(StudentBase):
	id: int

	class Config:
		orm_mode = True


