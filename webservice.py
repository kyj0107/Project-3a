import requests
import json
import pygal
from datetime import datetime
import lxml
import webbrowser

def get_symbol():

    symbol = input("Enter the stock symbol you are looking for: ")
    return symbol

def get_chart():
    while True:
        chart_type = ''
        try: 
            print("\nChart Types\n---------------\n 1. Bar \n 2. Line\n")
            chart = input("Enter the chart type you want (1,2): ")
            if chart == "1":
                chart_type = 'Bar'
                break
            elif chart == "2":
                chart_type = 'Line'
                break
            else:
                print("Invalid Chart Type! Try Again!")
        except Exception as error:
            print("Invalid Chart Type! Try Again!")
    return chart_type

def get_time_series():

    values = []

    while True:

        try:

            print("\nSelect the Time Series of the chart you want to Generate")
            print("--------------------------------------------------------")
            print("1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\n")
            number = int(input("Enter the time series option (1, 2, 3, 4): "))  

            if number == 1:
                values = ['INTRADAY', '60min']
                break
            elif number == 2:
                values = ['DAILY', 'null']
                break
            elif number == 3:
                values = ['WEEKLY', 'null']
                break
            elif number == 4:
                values = ['MONTHLY', 'null']
                break
            else:
                print("Invalid input. Please enter a number between 1 and 4.")
                continue
            
        except ValueError:

            print("Invalid input. Try again.")
            continue

    return values

def get_dates():

    while True:
    
        start_date = input("Enter the beginning date in YYYY-MM-DD format: ")
        end_date = input("Enter the end date in YYYY-MM-DD format: ")
        # Validate the dates
        try:

            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

            if end_date_obj < start_date_obj:

                print("End date cannot be before the start date.")
                continue

            break

        except ValueError:

            print("Invalid date format. Please use YYYY-MM-DD.")
            continue

    return [start_date_obj, end_date_obj]

def main():

    while True:

        try:

            symbol = get_symbol()
            chart_type = get_chart()
            values = get_time_series()
            start_end = get_dates()

            url = 'https://www.alphavantage.co/query?function=TIME_SERIES_{}&symbol={}&interval={}&apikey=9I22O100RNSZ6IPR'.format(values[0], symbol, values[1])

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

                if x_time_obj >= start_end[0] and x_time_obj <= start_end[1]:
                    
                    for item in data[key][x]:

                        if 'open' in item:

                            open_values.append(float(data[key][x][item]))

                        elif 'high' in item:

                            high_values.append(float(data[key][x][item]))

                        elif 'low' in item:

                            low_values.append(float(data[key][x][item]))

                        elif 'close' in item:

                            close_values.append(float(data[key][x][item]))

            if chart_type == 1:

                bar_chart = pygal.Bar()
                bar_chart.title = 'Stock Data for IBM: {} to {}'.format(str(start_end[0]), str(start_end[1]))
                bar_chart.x_labels = [x for x in usable_dates]
                bar_chart.add('open', open_values)
                bar_chart.add('high', high_values)
                bar_chart.add('low', low_values)
                bar_chart.add('close', close_values)
                bar_chart.render_to_file('bar_chart.svg')
                webbrowser.open('bar_chart.svg')
            
            elif chart_type == 2:

                line_chart = pygal.HorizontalLine()
                line_chart.title = 'Stock Data for IBM: {} to {}'.format(str(start_end[0]), str(start_end[1]))
                line_chart.x_labels = [x for x in usable_dates]
                line_chart.add('open', open_values)
                line_chart.add('high', high_values)
                line_chart.add('low', low_values)
                line_chart.add('close', close_values)
                line_chart.render_to_file('line_chart.svg')
                webbrowser.open('line_chart.svg')

            run_again = input("Would you like to view more stock data? Press 'y' to continue: ")

            if run_again.lower() != 'y':

                break

        except:

            print("Invalid option. Try again.")
            continue

main()