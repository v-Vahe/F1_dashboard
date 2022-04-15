import pymongo as mondb

moncon = mondb.MongoClient('mongodb://<user>:<passwd>@<host>:27017/<db>')
mondb = moncon.db.collection

