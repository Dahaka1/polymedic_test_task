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
	:param db: default SA db-session obj defined by fastapi Depends
	:return: created student instance dict
	"""
	if student_group_id is None:
		student_group_id = models.StudentGroup.default_student_group_id()
	else:
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
	"""
	:param student_id: searched student id
	:param db: default SA db-session obj defined by fastapi Depends
	:return: searched student instance dict
	"""
	db_student = crud.get_student(db=db, student_id=student_id)
	if db_student is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
	return db_student


@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(
	student_id: Annotated[int, Path(ge=1)],
	student: Annotated[schemas.StudentCreate, Body(embed=True)],
	db: Session = Depends(get_db)
):
	"""
	:param student_id: student id that you need to update
	:param student: updated student data dict (excepting id)
	:param db: default SA db-session obj defined by fastapi Depends
	:return: updated student instance dict
	"""
	db_student = crud.get_student(db=db, student_id=student_id)
	if db_student is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

	if student.student_group_id is None:
		if not db_student.student_group_id is None:
			student.student_group_id = db_student.student_group_id
		else:
			student.student_group_id = models.StudentGroup.default_student_group_id()
	else:
		student_group = db.query(
			models.StudentGroup
		).filter_by(id=student.student_group_id).first()
		if student_group is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student group not found")

	return crud.update_student(db=db, student=db_student, updated_student=student)


@app.delete("/students/{student_id}")
def delete_student(
	student_id: Annotated[int, Path(ge=1)],
	db: Session = Depends(get_db)
):
	"""
	:param student_id: student id that you have to delete
	:param db: default SA db-session obj defined by fastapi Depends
	:return: deleted student id
	"""
	db_student = crud.get_student(db=db, student_id=student_id)
	if db_student is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
	return crud.delete_student(db=db, student_id=student_id)


@app.get("/teachers/", response_model=list[schemas.Teacher])
def get_teachers(
	db: Session = Depends(get_db)
):
	"""
	:param db: default SA db-session obj defined by fastapi Depends
	:return: list of the Teacher instances if they're exists
	"""
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
	"""
	:param course: Course instance with params you need
	:param course_program_id: optionally choosing param; if not chosen, course program will be automatically defined by
	 default course program instance
	:param db: default SA db-session obj defined by fastapi Depends
	:return: created course instanced dict with it additional params such as included exams and self works
	"""
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
	"""
	:param course_id: course id that you need to get
	:param db: default SA db-session obj defined by fastapi Depends
	:return: created course instanced dict with it additional params such as included exams and self works
	"""
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
	"""
	:param course_id: id of student course which instances you need to get
	:param db: default SA db-session obj defined by fastapi Depends
	:return: course instance dict and list of Student instances
	"""
	course = crud.get_course(course_id=course_id, db=db)
	if course is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
	return {"course": course,
			"students": course.get_students()}


@app.post("/grades/")
def create_student_exam_grade(
	student_course_grade: Annotated[schemas.StudentGradeCreate, Body()],
	exam_id: Annotated[int | None, Body()] = None,
	db: Session = Depends(get_db)
):
	"""
	:param exam_id: specific exam id for creating grade by course if needed. if not chosen,
	function will use default exam instance. NOTICE: this parameter is because studying course may include
	many exams, not only one
	:param student_course_grade: new student grade instance
	:param db: default SA db-session obj defined by fastapi Depends
	:return: created student grade instance dict
	"""
	student = crud.get_student(db=db, student_id=student_course_grade.student_id)
	if student is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
	course = db.query(models.Course).filter_by(id=student_course_grade.course_id).first()
	if course is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
	if student_course_grade.exam_id is None:
		try:
			student_course_grade.exam_id = course.get_course_program().exams()[0].exam_id  # set exam id as default
		except IndexError:
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chosen course doesn't have defined exams"
																				"in database")
	else:
		exam = db.query(models.Exam).filter_by(id=exam_id).first()
		if exam is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
	if any(
		db.query(models.StudentGrade).filter_by(
			student_id=student.id, course_id=course.id, exam_id=student_course_grade.exam_id
		).all()
	):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Current grade already exists")

	student_grade = crud.create_student_course_grade(db=db, student_score=student_course_grade)
	return student_grade


@app.put("/grades/{grade_id}")
def update_student_exam_grade(
	grade: Annotated[int, Body(embed=True,
							   ge=1, le=5)],
	grade_id: Annotated[int, Path(ge=1)],
	db: Session = Depends(get_db)
):
	"""
	:param grade: student grade score that you need to set
	:param grade_id: id of existing student exam grade
	:param db: default SA db-session obj defined by fastapi Depends
	:return: updated student grade instance
	"""
	student_grade = db.query(
		models.StudentGrade
	).filter_by(id=grade_id).first()
	if student_grade is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found")
	return crud.update_student_exam_grade(
		db, student_grade, grade
	)
