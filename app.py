import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import pygal

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['SECRET_KEY'] = 'your secret key'

@app.route('/', methods=('GET', 'POST'))
def index():

    file = open('stocks.csv')
    symbols = []

    for line in file:
        values = line.split(',')
        symbols.append(values[0])

    symbols.pop(0)

    if request.method == "POST":
        #get the title and content
        symbol = request.form['symbol']
        chart_type = request.form['chart_type']
        time_series = request.form['time_series']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        #display an error if title or content is not submitted
        #otherwise connect to the database and add the post
        if not start_date:
            flash('Start date is required!')
        elif not end_date:
            flash('End date is required!')
        else:
            flash('Does it work?')

    return render_template('index.html', symbols=symbols)
    
app.run(host="0.0.0.0", port=5001)
