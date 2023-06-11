from .database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, ForeignKey
from loguru import logger


# изначально попробовал сделать модели автоматически, но при таком варианте они доступны только для чтения :(

# Student = Base.classes.student
# Department = Base.classes.department
# Faculty = Base.classes.faculty
# StudentGroup = Base.classes.student_group


class Department(Base):
	__tablename__ = "department"

	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=True)


class Faculty(Base):
	__tablename__ = "faculty"

	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=True)
	department_id = Column(Integer, ForeignKey("department.id", onupdate="CASCADE", ondelete="CASCADE"))


class StudentGroup(Base):
	__tablename__ = "student_group"

	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=True)
	faculty_id = Column(Integer, ForeignKey("faculty.id", onupdate="CASCADE", ondelete="CASCADE"))

	@staticmethod
	def default_student_group_id():
		try:
			return SessionLocal().query(StudentGroup).first().id
		except AttributeError:
			logger.error(
				"There are default model StudentGroup objects wasn't defined"
			)


class Student(Base):
	__tablename__ = "student"

	id = Column(Integer, primary_key=True)
	fullname = Column(String, nullable=True)
	student_group_id = Column(Integer, ForeignKey("student_group.id", onupdate="CASCADE", ondelete="CASCADE"))


