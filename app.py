import sqlite3
import requests
from datetime import datetime
import json
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import pygal

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['SECRET_KEY'] = 'your secret key'

def generate_chart(symbol, chart_type, time_series, start_date, end_date):
        
        try:
            
            if time_series == 'intraday':
                interval = '60min'
            else:
                interval = 'null'

            url = 'https://www.alphavantage.co/query?function=TIME_SERIES_{}&symbol={}&interval={}&apikey=9I22O100RNSZ6IPR'.format(time_series.upper(), symbol, interval)

            response = requests.get(url)
            data = json.loads(response.text)

            i = 0

            key = ""

            for item in data:

                if i == 1:
                    key = item
                i += 1

            dates = []

            for item in data[key]:

                dates.append(item)

            usable_dates = []
            open_values = []
            high_values = []
            low_values = []
            close_values = []

            for x in dates:

                x_time_obj = datetime.strptime(x, '%Y-%m-%d')

                if x_time_obj >= start_date and x_time_obj <= end_date:
                    
                    for item in data[key][x]:

                        if 'open' in item:

                            open_values.append(float(data[key][x][item]))

                        elif 'high' in item:

                            high_values.append(float(data[key][x][item]))

                        elif 'low' in item:

                            low_values.append(float(data[key][x][item]))

                        elif 'close' in item:

                            close_values.append(float(data[key][x][item]))

            if chart_type == "bar":

                bar_chart = pygal.Bar()
                bar_chart.title = 'Stock Data for IBM: {} to {}'.format(str(start_date), str(end_date))
                bar_chart.x_labels = [x for x in usable_dates]
                bar_chart.add('open', open_values)
                bar_chart.add('high', high_values)
                bar_chart.add('low', low_values)
                bar_chart.add('close', close_values)
                bar_chart.render_to_file('bar_chart.svg')
            
            elif chart_type == "line":

                line_chart = pygal.Line()
                line_chart.title = 'Stock Data for IBM: {} to {}'.format(str(start_date), str(end_date))
                line_chart.x_labels = [x for x in usable_dates]
                line_chart.add('open', open_values)
                line_chart.add('high', high_values)
                line_chart.add('low', low_values)
                line_chart.add('close', close_values)
                line_chart.render_to_file('line_chart.svg')

        except:

            flash('Oops! Something went wrong. Make sure you\'ve filled out all the forms.')

@app.route('/', methods=('GET', 'POST'))

def index():

    file = open('stocks.csv')
    symbols = []

    for line in file:
        values = line.split(',')
        symbols.append(values[0])

    symbols.pop(0)

    # Hmmm...

    if request.method == "POST":
        symbol = request.form['symbol']
        chart_type = request.form['chart_type']
        time_series = request.form['time_series']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        if not start_date:
            flash('Start date is required!')
        elif not end_date:
            flash('End date is required!')
        elif start_date_obj > end_date_obj:
            flash('Start date cannot be later than end date!')
        else:
            generate_chart(symbol, chart_type, time_series, start_date_obj, end_date_obj)

    return render_template('index.html', symbols=symbols)
    
app.run(host="0.0.0.0", port=5001)
