import os

START_COMMAND = "uvicorn sql_app.main:app --host 0.0.0.0 --port 8000"

DATABASE_PARAMS = dict(user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD"),
					   host=os.environ.get("DB_HOST"), port=os.environ.get("DB_PORT"), dbname=os.environ.get("DB_NAME"))

SQL_MAIN_SCRIPT_PATH = "sql_app/static/sql/script.sql"

STD_TABLES_AMOUNT = 17

DROP_TABLES_EVERY_LAUNCH = True

# loguru logging settings
LOGGING_FORMAT = '{time} {level} {message}'
ERRORS_OUTPUT_FILE = 'logs.log'
LOGGING_LEVELS = [
	"ERROR",
	"INFO"
]
