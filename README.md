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
- Then you can check SQL-queries realized in file 'queries.sql' at the same folder.

# Server launching and using API directions:
- Just clone project by git-clone command and run next commands using docker/docker-compose: 'docker-compose build' -> 'docker-compose up';
- After applying start-commands app will automatically initialize their database default content. You'll see notifications about it;
- By default, for clear API testing all database relations are deleting every app launch. To change it, you can set the corresponding parameter at the settings file ('src/setting.py');
- So, now you can send requests to the application API by default address: 'localhost:8000' (+ needed url);
- All of available requests types are showing at '/docs' url - in the standard Swagger generated API docs.