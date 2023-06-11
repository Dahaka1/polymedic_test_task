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
