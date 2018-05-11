from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app)


@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    #print(mars)
    data = scrape_mars.scrape()
    print(data)
    mars.update(
        {},
        data,
        upsert=True
    )
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)