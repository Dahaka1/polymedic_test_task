from fastapi import FastAPI, Depends, Body, Path, HTTPException, status

from . import crud, schemas, models
from typing import Annotated
from sqlalchemy.orm import Session
from .database import SessionLocal

app = FastAPI()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.post("/students/", response_model=schemas.Student)
def create_student(
	student: Annotated[schemas.StudentCreate, Body()],
	student_group_id: Annotated[int | None, Body()] = None,
	db: Session = Depends(get_db)
):
	"""
	:param student_group_id: student group id is optional param; if it wouldn't choose, it will define as default object id
	:param student: pydantic validation model
	:param db: default SA db-session obj
	"""
	if student_group_id is None:
		student_group_id = models.StudentGroup.default_student_group_id()
	if db.query(models.StudentGroup).filter_by(id=student_group_id).first() is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student group not found")
	return crud.create_student(
		student=student,
		db=db,
		student_group_id=student_group_id
	)


@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(
	student_id: Annotated[int, Path(ge=1)],
	db: Session = Depends(get_db)
):
	db_student = crud.get_student(db=db, student_id=student_id)
	if db_student is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
	return db_student


@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(
	student_id: Annotated[int, Path(ge=1)],
	student: Annotated[schemas.Student, Body(embed=True)],
	db: Session = Depends(get_db)
):
	db_student = crud.get_student(db=db, student_id=student_id)
	if db_student is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

	if student.student_group_id is None:
		student.student_group_id = models.StudentGroup.default_student_group_id()

	updated_student = db.query(models.Student).filter_by(id=student.id).first()
	if not updated_student is None and updated_student.id != db_student.id:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Student with ID = {student.id} already exists")

	return crud.update_student(db=db, student=db_student, updated_student=student)


@app.delete("/students/{student_id}")
def delete_student(
	student_id: Annotated[int, Path(ge=1)],
	db: Session = Depends(get_db)
):
	db_student = crud.get_student(db=db, student_id=student_id)
	if db_student is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
	return crud.delete_student(db=db, student_id=student_id)