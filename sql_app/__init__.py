from .database import SessionLocal
from .database import conn
from .static.sql import quieries
from loguru import logger
import src.settings
from .models import Department, Faculty, StudentGroup
from typing import Any
from .crud import create_db_instance
from .main import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


def get_all_tables() -> list[str]:
	with conn.cursor() as cursor:
		cursor.execute(
			quieries.GET_ALL_TABLES
		)
		return [table[0] for table in cursor.fetchall()]


def init_database() -> None:
	tables_amount = len(get_all_tables())
	if not tables_amount:  # if there are no tables existing (=0)
		file = open(src.settings.SQL_MAIN_SCRIPT_PATH, encoding='utf-8')
		script = file.read()
		with conn.cursor() as cursor:
			cursor.execute(script)
		file.close()
		logger.info(
			f"Database relations was successfully created ({tables_amount} relations)"
		)
	elif tables_amount == src.settings.STD_TABLES_AMOUNT:
		pass
	else:
		logger.error(
			f"There are non-standard amount of database tables was defined ({tables_amount})"
		)


def init_models() -> None:
	department = "Department"
	if not objects_exists(department):
		department_obj = create_db_instance(db=SessionLocal(), cls_name=department, title="Engineering school")
		faculty_obj = create_db_instance(db=SessionLocal(), cls_name="Faculty", title="Engineering school", department=department_obj)
		student_group = create_db_instance(db=SessionLocal(), cls_name="StudentGroup", title="A52", faculty=faculty_obj)
		student_group_params = student_group.__dict__
		student_group_params.pop("_sa_instance_state")
		logger.info(
			f"Database objects was successfully initiated"
		)
		logger.info(
			f"For creating student now you can use student group obj params: {student_group_params}"
		)


def objects_exists(model: str) -> bool:
	with conn.cursor() as cursor:
		cursor.execute(quieries.GET_ALL_ROWS % model.lower())
		rows_amount = len(cursor.fetchall())
	if rows_amount == 0:
		return False
	return True
