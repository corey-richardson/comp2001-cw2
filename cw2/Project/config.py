import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

# Database credentials
server = "DIST-6-505.uopnet.plymouth.ac.uk"
database = 'COMP2001_CRichardson'
username = "CRichardson"
password = "BssN103*"

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialise SQLAlchemy and Marshmallow in the context of the app
db = SQLAlchemy(app)
ma = Marshmallow(app)
