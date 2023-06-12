from sqlalchemy.orm import Session
from typing import Any
from . import schemas, models
from .database import SessionLocal


def create_instance(instance: Any) -> Any:
	"""
	creating instances by general case (without pydantic validation)
	"""
	db = SessionLocal()
	db.add(instance)
	db.commit()
	db.refresh(instance)
	db.close()
	return instance


def create_student(db: Session, student: schemas.StudentCreate, student_group_id: int):
	student = models.Student(
		fullname=student.fullname,
		student_group_id=student_group_id
	)
	db.add(student)
	db.commit()
	db.refresh(student)
	return student


def get_student(db: Session, student_id: int):
	return db.query(models.Student).filter_by(id=student_id).first()


def update_student(db: Session, student: schemas.Student, updated_student: schemas.Student):
	student.id = updated_student.id
	student.fullname = updated_student.fullname
	student.student_group_id = updated_student.student_group_id
	db.commit()
	db.refresh(student)
	return student


def delete_student(db: Session, student_id: int):
	db.query(models.Student).filter_by(id=student_id).delete()
	db.commit()
	return student_id


def get_teachers(db: Session):
	teachers = db.query(models.Teacher).all()
	return teachers


def create_course(db: Session, course: schemas.CourseCreate):
	course = models.Course(
		title=course.title
	)
	db.add(course)
	db.commit()
	db.refresh(course)
	return course


def get_course(db: Session, course_id: int):
	course = db.query(models.Course).filter_by(id=course_id).first()
	return course


def create_student_exam_grade(db: Session, student_score: schemas.StudentGradeCreate):
	student_exam_score = models.StudentGrade(
		student_id=student_score.student_id,
		exam_id=student_score.exam_id,
		grade=student_score.grade
	)
	db.add(student_exam_score)
	db.commit()
	db.refresh(student_exam_score)
	return student_exam_score


def update_student_exam_grade(db: Session, student_grade: models.StudentGrade, updated_student_grade: schemas.StudentGradeCreate):
	student_grade.grade = updated_student_grade.grade
	db.commit()
	db.refresh(student_grade)
	return student_grade
