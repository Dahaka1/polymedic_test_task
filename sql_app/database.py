from psycopg2 import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.settings
from sqlalchemy.orm import declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % tuple(src.settings.DATABASE_PARAMS.values())

engine = create_engine(
	SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

conn = connect(**src.settings.DATABASE_PARAMS)



