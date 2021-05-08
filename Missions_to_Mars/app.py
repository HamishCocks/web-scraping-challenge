from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_data

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def home():
    dest_data = mongo.db.mars.find_one()
    return render_template("index.html", mars = dest_data)


@app.route("/scrape")
def scrape():
    mars_data = scrape_data()

    mongo.db.mars.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

