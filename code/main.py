# ======================================== Libraries ========================================
from googlehomepush import GoogleHome  # Import Google Home library
import requests  # Library for making HTTP requests
import time
from bs4 import \
    BeautifulSoup  # Beautiful Soup Library is a python library for parsing structured data. In this case HTML data
import re
import json
import datetime

# ======================================== Variables ========================================
# SnowDay Predictor URL request
URL = "https://www.snowdaycalculator.com/prediction.php?zipcode=K2S1Y9&snowdays=0&extra=-0.4&"
res = requests.get(URL)
html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')
# OSTA Predictor URL request
URL1 = "http://www.ottawaschoolbus.ca/"
res1 = requests.get(URL1)
html_page1 = res1.content
soup1 = BeautifulSoup(html_page1, 'html.parser')
# Weather URL request
"""
The Weather one uses OPENWEATHER API which requires you to sign up for free to access their API keys
The Weather one struggles to be passed to the google home mini because it contains such a long string
"""
URL2 = "http://api.openweathermap.org/data/2.5/forecast?q=Ottawa,CA&units=metric&cnt=1&appid=0498228c4cc70f8c9f9051d17dee5679"
res2 = requests.get(URL2)
html_page2 = res2.json()
# soup2 = BeautifulSoup(html_page2, 'html.parser')

# Get tomorrows date
date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)
set_time = datetime.datetime.now()
greeting = "Good Morning Buddha Bowl. "
ready = False


# Function that gets the OSTA bus status
def busStatus():
    try:
        osta_status = soup1.find("h4", attrs={"class": "alert"}).get_text()  # get_text() strips the HTML tags
        # print(osta_status)
        return osta_status
    except:
        GoogleHome(host="192.168.50.180").say("An error occurred")


# Function that returns the snow day predictor percentage
def getPredictor():
    # Gets tomorrows date and prints it like the following: 20201101
    snowDate = ''.join((str(date_tomorrow.year), str(date_tomorrow.month), str(date_tomorrow.day).zfill(2)))
    try:
        # Get the text under the following html tag
        gdp_table = soup.find("table", attrs={"class": "prediction"})
        gdp_data = gdp_table.getText
        data_str = str(gdp_data)  # Convert the text to string

        # Find the string containg the prediction percentage
        for item in data_str.split("\n"):
            if "theChance[" + snowDate + "]" in item:
                # print(item.strip())
                # Strip the item and remove unnecessary strings
                s = item.strip()
                s = s.replace("theChance[" + snowDate + "] = ", "")
                s = s.replace("//PREDICTION", "")
                s = s.replace(";", "")
                s = s.replace("\t", "")
                # print(s)
                # Convert and round the float
                s = float(s)
                s = round(s)
                # print(s)
                # The predictor can return numbers larger than 100 and smaller 0 so round those so round them
                if s < 0:
                    s = 0
                elif s > 100:
                    s = 100
                return s
    except ValueError as err:
        GoogleHome(host="192.168.50.180").say("An error occurred" + str(err))


# Function that gets the weather using OPENWEATHER API
def getWeather():
    temp = html_page2["list"][0]["main"]["temp"]
    temp_low = html_page2["list"][0]["main"]["temp_min"]
    temp_high = html_page2["list"][0]["main"]["temp_max"]
    precipitation = html_page2["list"][0]["pop"]
    description = html_page2["list"][0]["weather"][0]["description"]
    # print(description)
    return str(temp), str(temp_high), str(temp_low), str(precipitation), description


# ========================================MAIN FUNCTION========================================

# https://github.com/deblockt/google-home-push/issues/5
while True:
    time.sleep(5)  # You can change the delay because you don't need to constantly be requesting time
    date_tomorrow = datetime.date.today() + datetime.timedelta(days=1)  # Get the current date
    set_time = datetime.datetime.now()  # Get the current time
    get_time = set_time.strftime("%H:%M")  # Get the only the hours and minutes
    print(get_time)  # Use this so that when you run as an executable you can see the output to test it is working
    # Runs if it is a specific time and it hasn't been triggered
    if get_time == "05:55" and ready == False:
        ready = True
        """ ## Weather Things##
        temp, temp_high, temp_low, precipitation, description = getWeather() 
        weather_text = "Currently it is " + temp + " degrees. " + " There will be a high of " + temp_high + " degrees and a low of " + temp_low + "degrees. The description is " + description + ". The chance of precipitation is " + precipitation + "percent."
        GoogleHome(host="192.168.50.180").say(weather_text)
        """
        # Get the OSTA bust status and the snowday predictor for tomorrow
        bus_text = busStatus()
        snow_text = ". Tomorrows snow day prediction is " + str(getPredictor()) + " percent"

        # Try and catch exception
        try:
            GoogleHome(host="192.168.50.180").say(greeting + bus_text + snow_text)

        except ValueError as err:
            print(ValueError)
            GoogleHome(host="192.168.50.180").say("An error occurred" + str(err))
    elif get_time != "05:55":
        ready = False
