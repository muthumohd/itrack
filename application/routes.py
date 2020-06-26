from typing import Any, Union

from application import app
from flask import render_template
from flask import Flask
import pymongo, json
from decimal import Decimal
from datetime import datetime
# from flask_pymongo import PyMongo
# from pymongo import MongoClient

# Configure the Flask application to connect with the MongoDB server
# app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/SomeDatabase"
# app.config['MONGO_DBNAME'] = 'SomeCollection'
# app.config['SECRET_KEY'] = 'secret_key'

# Connect to MongoDB using Flask's PyMongo wrapper
# mongo = PyMongo(app)
# db = mongo.db
# col = mongo.db["Some Collection"]
# print ("MongoDB Database:", mongo.db)

mongo = pymongo.MongoClient('mongodb+srv://iotuld:iotuld@cluster0-fe0zr.mongodb.net/test', maxPoolSize=50, connect=False)
# mongodb+srv://iotuld:iotuld@cluster0-fe0zr.mongodb.net/test
db = pymongo.database.Database(mongo, 'uldtracker')



@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/warehouse")
def warehouse():
    return render_template("warehouse.html")

@app.route("/warehouse/<whname>")
def whdetails(whname):
    col = pymongo.collection.Collection(db, 'warehouse')
    x = col.find_one(sort=[("created_date", pymongo.DESCENDING)])
    templateData={
        'title' : "Warehouse",
        'Warehouse':x['wh_name'],
        'Temperature':x['temperature'],
        'LightStatus':x['light_status'],
        'Date':x['created_date'].strftime("%d/%m/%Y, %H:%M:%S")
    }
    print(templateData)
    return render_template("warehouse.html", **templateData)

@app.route("/uld")
def uld():
    return render_template("uldinfo.html", title="ULD")

@app.route("/uld/<uldid>")
def ulddetail(uldid):
    col = pymongo.collection.Collection(db, 'ulddata')
    x = col.find_one(sort=[("created_date", pymongo.DESCENDING)])
    print("The type of createddate = ", type(x['created_date']))
    lcol=pymongo.collection.Collection(db, 'uldlocationdata')
    lx = lcol.find_one(sort=[("time", pymongo.DESCENDING)])
    base_url="https://www.google.com/maps/embed/v1/place?key=AIzaSyDWgQ9WQQZXfc5p9AovX-L0AG4A6X6gWtI&q="
    templateData = {
        'title':uldid,
        'UldId': x['ULDId'],
        'Temperature': x['temperature'],
        'Humidity':x['humidity'],
        'Loaded': x['isloaded'],
        'UldTime': x['created_date'].strftime("%d/%m/%Y, %H:%M:%S"),
        # 'City': x['city'],
        #         # 'Country': x['country'],
        #         # 'Date':x['createddate'],


        'MapApi':base_url+lx['latitude']+"," +lx['longitude']
    }
    print ("Template ===", templateData)
    return render_template("uldinfo.html", **templateData)

@app.route("/uld/trace/<uldid>/<startdate>/<enddate>")
def history(uldid, startdate, enddate):
    col = pymongo.collection.Collection(db, 'uldlocationdata')
    startDateObj=datetime.strptime(startdate, "%d-%m-%Y")
    endDateObj=datetime.strptime(enddate, "%d-%m-%Y")
    print("The uld id = ", uldid)
    print("The startdate = ", startdate)
    print("The enddate = ", enddate)
    print("Start Date Obj = ", startDateObj)
    print("End Date Obj = ", endDateObj)
    print("End Date Obj Type = ", type(endDateObj))
    # x = col.find({'$and' : [{"uldId":uldid},{ "time":{'$gte': startDateObj, '$lte': endDateObj}}]}, {"latitude":1, "longitude":1}, sort=[("time", pymongo.ASCENDING)])
    # x = col.find({'$and': [{"uldId": uldid}, ]},
    #     #               {"latitude": 1, "longitude": 1}, sort=[("time", pymongo.ASCENDING)])
    x = col.find({"uldId":uldid, "$and": [{"time": {"$gte": startDateObj}}, {"time": {"$lte":endDateObj}}]},
                 {"latitude": 1, "longitude": 1}, sort=[("time", pymongo.DESCENDING)]).limit(20)
    # x=col.find({"uldId":uldid}, sort=[("time", pymongo.DESCENDING)]).limit(20)
    count=x.count()
    print("Result Set ===", x.count())
    originLat=Decimal(x[count-1]['latitude'])
    originLon=Decimal(x[count-1]['longitude'])
    destLat=Decimal(x[0]['latitude'])
    destLon=Decimal(x[0]['longitude'])
    waypointArray=[]

    for item in x:
        dictA = {}
        lat=str(Decimal(item['latitude']))
        lon=str(Decimal(item['longitude']))
        dictA={"lat":lat, "lng":lon}
        waypointArray.append(dictA)

    templateData={
        'Origin':{'lat':originLat, 'lng':originLon},
        'Destination':{'lat':destLat, 'lng':destLon},
        'WayPoints': waypointArray
        # 'WayPoints':"[{lat:25.228322, lng:55.332773}, {lat:25.230934, lng:55.289468}]"
    }
    print("The template data = ", templateData)
    return  render_template("uldtrack.html", **templateData)