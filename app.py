
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def home():

    data = mongo.db.data.find_one()
   
    return render_template("index.html", data = data)


@app.route("/scrape")
def scrape():
  
    data = mongo.db.data
    data2 = scrape_mars.scrape_all()

    data.update({}, data2, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
