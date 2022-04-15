from sqlalchemy import create_engine
from sqlalchemy import text
import urllib
import os 
import re
import sqlparse
# or from sqlalchemy.sql import text

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=localhost;"
                                 "DATABASE=formula1;"
                                 "UID=sa;"
                                 "PWD=Vahe1996")

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params), echo = True)


with open("./database/sql_server/create_tables.sql") as f_sql:
    sql_raw = f_sql.read()
    sql_queries = sqlparse.split(
        sqlparse.format(sql_raw, strip_comments=True)
    )

with engine.connect() as conn:
  for query in sql_queries:
      result = conn.execute(text(query))
      print(f"{result.rowcount} rows have been updated/selected.")