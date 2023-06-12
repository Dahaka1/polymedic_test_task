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


class TeacherBase(BaseModel):
	fullname: str | None = Field(
		max_length=50,
		default=None
	)
	department_id: int


class TeacherCreate(TeacherBase):
	pass


class Teacher(TeacherBase):
	id: int

	class Config:
		orm_mode = True


class CourseBase(BaseModel):
	title: str = Field(
		max_length=50
	)


class CourseCreate(CourseBase):
	pass


class Course(CourseBase):
	id: int

	class Config:
		orm_mode = True


class StudentGradeBase(BaseModel):
	student_id: int
	exam_id: int
	grade: int = Field(
		ge=1, le=5
	)


class StudentGradeCreate(StudentGradeBase):
	pass


class StudentGrade(StudentGradeBase):
	id: int
