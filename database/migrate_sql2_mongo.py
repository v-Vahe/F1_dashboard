import sqlalchemy as sa
import pandas as pd
import configparser
import pymongo
import pprint
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

config = configparser.ConfigParser()
config.read('database/db.cfg')

engine = sa.create_engine('mssql+pyodbc://{3}:{4}@{1}/{2}?driver={0}'.format(*config['SQL_DB'].values()))

query = """
    SELECT TOP 4 * 
    FROM drivers
"""

df1 = pd.read_sql(query, engine)
df1 = df1.drop('dob',axis=1)
data_dict_1 = df1.to_dict('records')


client = pymongo.MongoClient('mongodb://localhost:27017')

db = client['formula1db']
db.records.drop()
db.records.insert_many(data_dict_1)
filter = {}
doc = db.records.find(filter)
for document in doc:
  pprint.pprint(document)
# print(document)



# db.records.update_one()
#   { "$set": { "name": 42 } }
# )


# document = {
#     'salary':23
# }

# db.create_collection()
# db['salaries'].insert_one(document)


# filter = {}
# count = db.salaries.count_documents(filter)
# doc = db.salaries.find_one(filter)
# print(client.list_database_names())
# print(count)
# print(doc)


# db.people.insertOne( {
#     user_id: "abc123",
#     age: 55,
#     status: "A"
#  } )