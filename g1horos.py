from flask import Flask, render_template, request, jsonify
import requests
import json
import os
import datetime
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/g1hor', methods=['GET', 'POST'])
def g1hor():
    user_input = request.args.get('user_input') if request.method == 'GET' else request.form['user_input']
    format_str = '%d/%m/%Y' # The format
    dt_obj = datetime.datetime.strptime(user_input, format_str)

    current_time = datetime.datetime.now()
    #print(current_time.day)month/year
    '''
    # convert to date String
    date = dt_obj.strftime("%d/%m/%Y")
    print('Date String:', date)
    # convert to time String
    time = now.strftime("%H:%M:%S")
    print('Time String:', time)
    # year
    year = now.strftime("%Y")
    print('Year String:', year)'''

    month = int(dt_obj.strftime("%m"))
    date = int(dt_obj.strftime("%d"))

    if date > 31:
        print("Please enter the correct date. The date should not exceed 31\n")
    if month > 12:
        print("Please enter the correct month. The month should not exceed 12\n")
    if month == 12:
        if (date < 22): sign = 'Sagittarius'
        else: sign = 'Capricorn'
    elif month == 1:
        if (date < 20): sign = 'Capricorn'
        else: sign = 'Aquarius'
    elif month == 2:
        if (date < 19): sign = 'Aquarius'
        else: sign = 'Pisces'
    elif month == 3:
        if (date < 21): sign = 'Pisces'
        else: sign = 'Aries'
    elif month == 4:
        if (date < 20): sign = 'Aries'
        else: sign = 'Taurus'
    elif month == 5:
        if (date < 21): sign = 'Taurus'
        else: sign = 'Gemini'
    elif month == 6:
        if (date < 21): sign = 'Gemini'
        else: sign = 'Cancer'
    elif month == 7:
        if (date < 23):sign = 'Cancer'
        else: sign = 'Leo'
    elif month == 8:
        if (date < 23): sign = 'Leo'
        else: sign = 'Virgo'
    elif month == 9:
        if (date < 23): sign = 'Virgo'
        else: sign = 'Libra'
    elif month == 10:
        if (date < 23): sign = 'Libra'
        else: sign = 'Scorpio'
    elif month == 11:
        if (date < 22): sign = 'Scorpio'
        else: sign = 'Sagittarius'
    
    # Make the GET request to the horoscope API
    response = requests.get("https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign="+sign+"&day=today")
    data = response.json()  # Convert the response to JSON
    mstatus = data["status"]

    # Store the JSON data in a file
    with open("horoscope_data.json", "w") as file:
        json.dump(data, file)

    # Retrieve JSON data from the file
    with open("horoscope_data.json", "r") as file:
        data = json.load(file)
    # Access and process the retrieved JSON data
    if mstatus == 200:
        date = data["data"]["date"]
        horoscope_data = data["data"]["horoscope_data"]
    else:
        horoscope_data = "The server is experiencing a high volume of requests for Aries!. Please try again later."
        date = current_time.strftime("%B %d, %Y")
        #https://www.scaler.com/topics/get-current-date-python/
    try:
        response = "this is the answer"
        #content = f"Horoscope for date {date}: {horoscope_data}"
        content = f"{horoscope_data}"
    except RateLimitError:
        content = "The server is experiencing a high volume of requests. Please try again later."
    return jsonify(content=content)

if __name__ == '__main__':
    app.run(debug=True)