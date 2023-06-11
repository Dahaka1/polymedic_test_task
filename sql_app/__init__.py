from .database import SessionLocal
from .database import conn
from .static.sql import quieries
from loguru import logger
import src.settings
from . import models
from .crud import create_instance
from .main import get_db


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
	"""
	creating models objects by default
	"""
	db = SessionLocal()
	if not any(db.query(models.Department).all()):
		default_department = create_instance(
			models.Department(title="Engineering school")
		)
		default_faculty = create_instance(
			models.Faculty(title="Robotics", department_id=default_department.id)
		)
		default_student_group = create_instance(
			models.StudentGroup(title="A52", faculty_id=default_faculty.id)
		)
		logger.info(
			f"Default models instances was successfully created. "
			f"Now you can use default students group with ID = {default_student_group.id}"
			f" for creating student instances"
		)
