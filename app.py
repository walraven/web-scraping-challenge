#imports
from flask import Flask, render_template, redirect
from pymongo import MongoClient

app = Flask(__name__)

#setup database
conn = 'mongodb://localhost:27017'
client = MongoClient(conn)
db = client.mars_db


@app.route('/')
def index():
    mars_data = db.scrapes.find_one()
    return render_template("index.html", data=mars_data)


@app.route('/scrape')
def scrape():
    #imports
    from scrape_mars import scrape_mars
    #do the scrape and save it in the database
    info = db.scrapes
    mars_data = scrape_mars()
    info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)