# From cw2
# python ..\Schema\test_schema_connection.py

from sqlalchemy import create_engine, text

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

insert_query = text("""
INSERT INTO "CW2.User" (email, role)
VALUES ('testadmin@email.com', 'ADMIN')
""")

with engine.begin() as connection:
    connection.execute(insert_query)
    print("Data inserted successfully!")

connection.close()