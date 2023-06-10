from loguru import logger
from . import settings
import os


def start_app() -> None:
	os.system(settings.START_COMMAND)


def logger_init() -> None:
	for level in settings.LOGGING_LEVELS:
		logger.add(
			settings.ERRORS_OUTPUT_FILE,
			level=level,
			format=settings.LOGGING_FORMAT,
			rotation="1 MB",
			compression="zip"
		)
