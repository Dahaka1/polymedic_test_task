from .database import Base, SessionLocal
from sqlalchemy import Enum, Column, Integer, String, ForeignKey, Date, Time, Text, PrimaryKeyConstraint
from loguru import logger
from datetime import date
import enum


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


class Teacher(Base):
	__tablename__ = "teacher"

	id = Column(Integer, primary_key=True)
	fullname = Column(String, nullable=True)
	department_id = Column(Integer, ForeignKey("department.id", ondelete="CASCADE", onupdate="CASCADE"))


class Exam(Base):
	__tablename__ = "exam"

	id = Column(Integer, primary_key=True)
	exam_date = Column(Date)
	exam_time = Column(Time)
	content = Column(Text, nullable=True)


class SelfWork(Base):
	__tablename__ = "self_work"
	id = Column(Integer, primary_key=True)
	created_at = Column(Date, default=date.today())
	content = Column(String, nullable=True)


class Course(Base):
	__tablename__ = "course"

	id = Column(Integer, primary_key=True)
	title = Column(String)

	def get_course_program(self):
		course_program = SessionLocal().query(
			CourseProgram
		).filter_by(course_id=self.id).first()
		return course_program

	def get_info(self):
		course_program = self.get_course_program()
		return {
			"course_program": course_program,
			"exams": course_program.exams(),
			"self_works": course_program.self_works()
		}

	def get_students(self):
		db = SessionLocal()
		studying_plan = self.get_course_program().studying_plan()
		student_groups = db.query(
			StudentGroup
		).filter_by(faculty_id=studying_plan.faculty_id).all()
		students = []
		for group in student_groups:
			group_students = db.query(
				Student
			).filter_by(student_group_id=group.id).all()
			students.extend(group_students)
		return students


class CourseProgram(Base):
	__tablename__ = "course_program"

	id = Column(Integer, primary_key=True)
	course_id = Column(Integer, ForeignKey("course.id", ondelete="CASCADE", onupdate="CASCADE"))

	def exams(self):
		return SessionLocal().query(
			CourseProgramExam
		).filter_by(course_program_id=self.id).all()

	def self_works(self):
		return SessionLocal().query(
			CourseProgramSelfWork
		).filter_by(course_program_id=self.id).all()

	def studying_plan(self, semester_id: int | None = None):
		if semester_id is None:
			return SessionLocal().query(
				StudyingPlan
			).filter_by(course_program_id=self.id).first()
		else:
			...  # may be extended later

	@staticmethod
	def create_default(course_id: int):
		default_course_program = CourseProgram(
			course_id=course_id
		)
		db = SessionLocal()
		db.add(default_course_program)
		db.commit()
		db.refresh(default_course_program)

		db.add(CourseProgramExam(
			course_program_id=default_course_program.id,
			exam_id=db.query(Exam).first().id
		))
		db.add(CourseProgramSelfWork(
			course_program_id=default_course_program.id,
			self_work_id=db.query(SelfWork).first().id
		))
		db.commit()
		return default_course_program, db  # returns db session instance for using in next method (Studying plan)


class CourseProgramExam(Base):
	__tablename__ = "course_program_exam"
	__table_args__ = (
		PrimaryKeyConstraint("course_program_id", "exam_id"),
	)

	course_program_id = Column(Integer, ForeignKey("course_program.id", ondelete="CASCADE", onupdate="CASCADE"))
	exam_id = Column(Integer, ForeignKey("exam.id", ondelete="CASCADE", onupdate="CASCADE"))


class CourseProgramSelfWork(Base):
	__tablename__ = "course_program_self_work"
	__table_args__ = (
		PrimaryKeyConstraint("course_program_id", "self_work_id"),
	)

	course_program_id = Column(Integer, ForeignKey("course_program.id", ondelete="CASCADE", onupdate="CASCADE"))
	self_work_id = Column(Integer, ForeignKey("self_work.id", ondelete="CASCADE", onupdate="CASCADE"))


class StudyingPlan(Base):
	__tablename__ = "studying_plan"
	__table_args__ = (
		PrimaryKeyConstraint("course_program_id", "faculty_id", "semester_id"),
	)

	faculty_id = Column(Integer, ForeignKey("faculty.id", ondelete="CASCADE", onupdate="CASCADE"))
	semester_id = Column(Integer, ForeignKey("semester.id", ondelete="CASCADE", onupdate="CASCADE"))
	course_program_id = Column(Integer, ForeignKey("course_program.id", ondelete="CASCADE", onupdate="CASCADE"))

	@staticmethod
	def create_default(course_program_id, db):
		default_studying_plan = StudyingPlan(
			faculty_id=db.query(Faculty).first().id,
			semester_id=db.query(Semester).first().id,
			course_program_id=course_program_id
		)
		db.add(default_studying_plan)
		db.commit()


class Semester(Base):
	__tablename__ = "semester"

	id = Column(Integer, primary_key=True)
	number = Column(Integer)
	semester_year = Column(Integer)


class StudentGrade(Base):
	__tablename__ = "student_grade"

	id = Column(Integer, primary_key=True)
	student_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE", onupdate="CASCADE"))
	exam_id = Column(Integer, ForeignKey("exam.id", ondelete="CASCADE", onupdate="CASCADE"))
	grade = Column(Integer)


# class CourseProgram(Base):
# 	__tablename__ = "course_program"
#
# 	id = Column(Integer, primary_key=True)
# 	course_id = Column(Integer, ForeignKey("course.id", onupdate="CASCADE", ondelete="CASCADE"))
#
