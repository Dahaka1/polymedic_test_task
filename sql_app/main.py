from fastapi import FastAPI, Depends, Body, Path, HTTPException, status
from . import crud, schemas, models
from typing import Annotated, Any
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


@app.get("/teachers/", response_model=list[schemas.Teacher])
def get_teachers(
	db: Session = Depends(get_db)
):
	teachers = crud.get_teachers(db=db)
	if not any(teachers):
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teachers not found")
	return teachers


@app.post("/courses/")
def create_course(
	course: Annotated[schemas.CourseCreate, Body()],
	course_program_id: Annotated[int | None, Body()] = None,
	db: Session = Depends(get_db)
):
	course = crud.create_course(
		db=db, course=course
	)
	if course_program_id is None:
		default_course_program, db_session = models.CourseProgram.create_default(course.id)  # creating default course program
		models.StudyingPlan.create_default(default_course_program.id, db_session)
	return {"course": course,
			**course.get_info()}


@app.get("/courses/{course_id}")
def get_course(
	course_id: Annotated[int, Path(ge=1)],
	db: Session = Depends(get_db)
):
	course = crud.get_course(course_id=course_id, db=db)
	if course is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
	return {"course": course,
			**course.get_info()}


@app.get("/courses/{course_id}/students")
def get_course_students(
	course_id: Annotated[int, Path(ge=1)],
	db: Session = Depends(get_db)
):
	course = crud.get_course(course_id=course_id, db=db)
	if course is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
	return {"course": course,
			"students": course.get_students()}


@app.post("/grades/")
def create_student_exam_grade(
	student_exam_grade: Annotated[schemas.StudentGradeCreate, Body()],
	db: Session = Depends(get_db)
):
	student = crud.get_student(db=db, student_id=student_exam_grade.student_id)
	if student is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
	exam = db.query(models.Exam).filter_by(id=student_exam_grade.exam_id).first()
	if exam is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
	if any(
		db.query(models.StudentGrade).filter_by(
			student_id=student.id, exam_id=exam.id
		).all()
	):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Current grade already exists")
	student_grade = crud.create_student_exam_grade(db=db, student_score=student_exam_grade)
	return student_grade


@app.put("/grades/{grade_id}")
def update_student_exam_grade(
	student_exam_grade: Annotated[schemas.StudentGradeCreate, Body()],
	grade_id: Annotated[int, Path(ge=1)],
	db: Session = Depends(get_db)
):
	student_grade = db.query(
		models.StudentGrade
	).filter_by(id=grade_id).first()
	if student_grade is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
	return crud.update_student_exam_grade(
		db, student_grade, student_exam_grade
	)
