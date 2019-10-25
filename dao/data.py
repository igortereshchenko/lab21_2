username = 'postgres'
password = 'StepWolf13'
host = 'localhost'
port = '5432'
database = 'postgres'
DATABASE_URI = 'postgres+psycopg2://postgres:{}@{}:{}/{}'.format(password, host, port, database)
