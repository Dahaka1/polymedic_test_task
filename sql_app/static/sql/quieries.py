GET_ALL_TABLES = "SELECT table_name FROM information_schema.tables " \
				 "WHERE table_schema = 'public';"

GET_ALL_ROWS = "SELECT * FROM %s;"

