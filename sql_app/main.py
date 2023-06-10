from fastapi import FastAPI, Depends, Body
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
def create_student(fullname: Annotated[str, Body(embed=True)], db: Session = Depends(get_db)):
	# default_group = models.default_student_group()
	return crud.create_db_instance(db=db, cls_name="student", fullname=fullname, student_group=default_group)

