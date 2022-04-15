from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
import pprint
 
app = Flask(__name__)  
 


app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/home')  
def home():  
    return "hello, welcome to our website";  

# @app.route('/')
# def home_page():
#     online_users = mongo.db.users.find({'online': True})
#     return render_template('index.html', online_users=online_users)



client = MongoClient('mongodb://localhost:27017')

print(client.list_database_names())

database = client['velvioo_aws5']
print(database.list_collection_names())

rides = database.rides


pprint.pprint(rides.find_one())

if __name__ =="__main__":  
    app.run(debug = True)  

