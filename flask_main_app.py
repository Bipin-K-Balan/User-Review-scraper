from flask import Flask, render_template, request,jsonify
# from flask_cors import CORS,cross_origin
import requests
from web_scrapper import Scrapper

app = Flask(__name__)

@app.route('/',methods =['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/scrape',methods=['GET','POST'])
def scrap():
    if request.method == 'POST':
        keyword = request.form['content']

        sc = Scrapper(keyword)
        reviews = sc.scrape()

    return render_template('results.html',reviews=reviews)


if __name__ == "__main__":
    app.run(port=8000,debug=True)


