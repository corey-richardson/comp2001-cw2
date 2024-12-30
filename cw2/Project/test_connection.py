from sqlalchemy import create_engine

server = "DIST-6-505.uopnet.plymouth.ac.uk"
database = 'COMP2001_CRichardson'
username = "CRichardson"
password = "BssN103*"

connection_string = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
)

engine = create_engine(connection_string)
connection = engine.connect()

print("Connection successful!")
connection.close()
