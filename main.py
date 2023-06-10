from dotenv import load_dotenv

load_dotenv()


from src import logger_init, start_app
from sql_app import init_database, init_models


def main():
	logger_init()
	init_database()
	init_models()
	start_app()


if __name__ == '__main__':
	main()

