#polymedic_test_task 

# ABOUT 
This is testing task realizing simple SQL-DB relations by SQL-script written manually.
Then DB handles SQL-queries defined by task terms.
And finally project realize CRUD-functions of simple API-service using FastAPI framework.

# BUILT-IN
- Python 3.11;
- Docker, Docker-Compose for starting Postgre-DB and app server;
- All libraries included in FastAPI framework such as Pydantic and SQLAlchemy;
- psycopg2 package for manually connecting to server.

# USAGE
- First of all, you can see SQL-script creating Database relations in app folder 'sql_app/static/sql', in file 'script.sql', with some comments of actions;
- At the same folder you can find graphic map of Database relations in file 'diagram.png';
- Then you can check SQL-queries realized in file 'queries.sql' at the same folder;
- 