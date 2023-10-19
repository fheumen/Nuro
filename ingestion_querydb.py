from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
import pyodbc
from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"
os.environ["OPENAI_API_BASE"] = ""  # Your Azure OpenAI resource endpoint
os.environ[
    "OPENAI_API_KEY"
] = "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"  # Your Azure OpenAI resource key
os.environ["OPENAI_CHAT_MODEL"] = "gpt-35-turbo-16k"  # Use name of deployment

os.environ["SQL_SERVER"] = "genaidb"  # Your az SQL server name
os.environ["SQL_DB"] = "DB_Demo1"
os.environ["SQL_USERNAME"] = ""  # SQL server username
os.environ["SQL_PWD"] = "{<password>}"  # SQL server password


driver = "{ODBC Driver 18 for SQL Serve}"
odbc_str = (
    "mssql+pyodbc:///?odbc_connect="
    "Driver="
    + driver
    + ";Server=tcp:"
    + os.getenv("SQL_SERVER")
    + ".database.windows.net;PORT=1433"
    + ";DATABASE="
    + os.getenv("SQL_DB")
    + ";trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"
)

db_engine = create_engine(odbc_str)

db = SQLDatabase(db_engine)

engine = create_engine(
    "mssql+pymssql://genaidb.database.windows.net:1433/DB_Demo1;trusted_Connection=yes;"
)

db = SQLDatabase(engine)


##conn_str = 'sqlserver://genaidb.database.windows.net:1433;database=DBTest;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;Authentication=ActiveDirectoryIntegrated'


conn_str = "jdbc:sqlserver://genaidb.database.windows.net:1433;database=DB_Demo1;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;Authentication=ActiveDirectoryIntegrated"

conn_str = "mssql+pymssql://genaidb.database.windows.net:1433/DB_Demo1;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;Authentication=ActiveDirectoryIntegrated"

conn_str = "mssql+pymssql://genaidb.database.windows.net:1433/DB_Demo1;encrypt=true;trustauthentification=yes;"

conn_str = f"Driver={driver};Server=tcp:genaidb.database.windows.net,1433;Database=DB_Demo1;trustauthentification=yes;"

pyodbc.connect(conn_str)

pyodbc.drivers()

pyodbc.dataSources()


pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};Server=tcp:genaidb.database.windows.net,1433;Database=DB_Demo1;Uid=378885@cognizant.com;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryIntegrated"
)


db = SQLDatabase.from_uri(
    "mysql+pyodbc:Driver={ODBC Driver 18 for SQL Server};Server=tcp:genaidb.database.windows.net,1433;Database=DB_Demo1;trusted_Connection=yes;",
)

pg_uri = (
    "mssql+pymssql://genaidb.database.windows.net:1433/DB_Demo1;Trusted_Connection=yes;"
)
# db = SQLDatabase.from_uri(pg_uri)

db = pymssql.connect(pg_uri)

db = SQLDatabase.from_uri(conn_str)

db = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};Server=tcp:genaidb.database.windows.net,1433;Database=DB_Demo1;Uid={your_user_name};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryIntegrated"
)


pyodbc.dataSources()
#####################
from databricks import sql
import os

connection = sql.connect(
    server_hostname="adb-114240507699944.4.azuredatabricks.net",
    http_path="/sql/1.0/warehouses/dc0bcdc6f550d984",
    access_token="<access-token>",
)

cursor = connection.cursor()

cursor.execute("SELECT * from range(10)")
print(cursor.fetchall())

cursor.close()
connection.close()
####################


toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))

agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
