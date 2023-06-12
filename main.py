from dotenv import load_dotenv

load_dotenv()

import time
time.sleep(5)  # waiting before imports for db-initializing while starting docker container

from src import logger_init, start_app
from sql_app import init_database, init_models


def main():
	logger_init()
	init_database()
	init_models()
	start_app()


if __name__ == '__main__':
	main()

