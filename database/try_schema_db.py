import sqlalchemy as sa
import sqlalchemy as sa
import configparser
import pandas as pd 
import pymongo
import pprint

# ________________ SQL ________________

print('I am here')
_config = configparser.ConfigParser()
_config.read('database/db.cfg')

engine = sa.create_engine('mssql+pyodbc://{3}:{4}@{1}/{2}?driver={0}'.format(*_config['SQL_DB'].values()))

query = """
    SELECT * FROM drivers
"""

df_drivers = pd.read_sql(query, engine)
df_drivers = df_drivers.head(3)
print(df_drivers.columns)
df_drivers = df_drivers.drop('dob', axis=1)
print(df_drivers.columns)
df_drivers = df_drivers.to_dict('records')
# pprint.pprint(df_drivers)
# print(df_drivers.keys())

# ______________________ MONGO _______________

client = pymongo.MongoClient('mongodb://localhost:27017')

db = client['formula1db']
db.drivers.drop()
db.drivers.insert_many(df_drivers)
db.drivers.foo.update_many()
filter = {}
doc = db.drivers.find(filter)
for document in doc:
  pprint.pprint(document)