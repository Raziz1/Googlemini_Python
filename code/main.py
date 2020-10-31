# RAHIM AZIZ
# Assignment #7
# 9/28/2020
# Python 3.8 with PYCHARM

# Import Libraries
from random import randint
import requests
import json
from datetime import datetime

# Variables_________________________________________________________________________________________________________
# Assign variable api key for OPENWEATHER
apiKey = "0498228c4cc70f8c9f9051d17dee5679"
cityName = ""
cityCode = ""
date = []
maxTemp = []
minTemp = []
rain = []
descriptor = []

# Assign variable api key for NEWSAPI
apinewsKey = "a12311ac38674b13a79a71bbb803a840"
# Create a list of news tags to store
author = []
title = []
cont = []
articleURL = []
choice = ""
exit = False
exitInput = ""

correctGuess = 0


# Forecast Function_____________________________________________________________________________
def forecast(lat, long):
    print("Would you like to see this weeks forecast? [y]/[n] :")
    inputForecast = str(input())  # Ask user whether they would like to see forecast

    if inputForecast == "y":
        # https://api.openweathermap.org/data/2.5/onecall?lat=45.41&lon=-75.7&exclude=minutely,hourly&appid=0498228c4cc70f8c9f9051d17dee5679
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + long + "&exclude=minutely," \
                                                                                              "hourly,current&appid=" + apiKey + "&units=metric"
        # Use parsed long and lat coordinates to request API JSON file
        response = requests.get(url)
        data = json.loads(response.text)
        # Catch exception of entered location is invalid
        try:
            for i in range(7):  # Cycle through 7 day forecast and store stats
                date.append(data["daily"][i]["dt"])
                maxTemp.append(data["daily"][i]["temp"]["max"])
                minTemp.append(data["daily"][i]["temp"]["min"])
                descriptor.append(data["daily"][i]["weather"][0]["description"])
                try:
                    rain.append(data["daily"][i]["rain"])  # If rain is null set to 0
                except KeyError:
                    rain.append(0)

                # Print centered forecast
                print(("____________________").center(40))
                print(("|" + str(datetime.fromtimestamp(date[i])) + "|").center(40))  # Convert unix time to standard
                print(("|" + "Max Temp: " + str(maxTemp[i]) + "°C" + "|").center(40))
                print(("|" + "Min Temp: " + str(minTemp[i]) + "°C" + "|").center(40))
                print(("|" + "Rain: " + str(rain[i]) + "%" + "|").center(40))
                print(("|" + "Description: " + descriptor[i] + "|").center(40))
                print(("____________________\n").center(40))
        except KeyError:
            print("Error! Try Again")
    elif inputForecast == "n":
        None


# Define Function for calling weather API____________________________________________________________________________
def weather(boolRequest):
    # Force user to input while request returns null
    while boolRequest == False:
        #  User Input for city
        print("Enter the name of your city (First letter Capital)")
        cityName = input()
        # User input for country
        print("Enter the first two letters of your country (LowerCase)")
        cityCode = input()
        # Combine user strings with url
        url = "https://api.openweathermap.org/data/2.5/weather?q=" + cityName + "," + cityCode + "&appid=" + apiKey + "&units=metric"
        # print(url)

        # Make a request for JSON file
        response = requests.get(url)
        data = json.loads(response.text)
        # print(data)
        # Assign and label data for weather

        # Catch exception of entered location is invalid
        try:
            currentTemp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            fahrenheit = currentTemp * 9 / 5 + 32  # Convert to fahrenheit (MATH)
            humidity = data["main"]["humidity"]
            lat = data["coord"]["lat"]
            long = data["coord"]["lon"]
            # Print weather conditions
            print("|" + cityName + ", " + cityCode + "|")
            print("Current Temp :", currentTemp, "°C")
            print("Current Temp :", fahrenheit, "°F")
            print("Description :", description)
            print("Humidity :", humidity, "%")
            forecast(str(lat), str(long))  # Check forecast for week while parsing longitude and latitude coords
            boolRequest = True  # Break while loop
            break
        except KeyError:
            print("Error! Try Again")


# News API_______________________________________________________________________________________________________
def news(artSize):
    url = "http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=a12311ac38674b13a79a71bbb803a840"
    # Make a request for JSON file
    response = requests.get(url)
    data = json.loads(response.text)
    totalResults = data["totalResults"]  # Figure out how many articles are available
    access = -1
    for i in range(totalResults):  # Loop through every article and store it in python list
        author.append(data["articles"][i]["author"])
        title.append(data["articles"][i]["title"])
        cont.append(data["articles"][i]["description"])
        articleURL.append(data["articles"][i]["url"])

    while not artSize:  # Loop through if error
        print("There are", totalResults, "articles. Which would you like to access? : ")
        access = int(input())  # Ask the user which article they would like to access
        if access > totalResults or access < 0:  # Make sure the user picks an article that exists
            artSize = False
            print("ERROR!")

        else:
            artSize = True  # Exit loop
            # Print article details
            print(author[access])
            print(title[access])
            print(cont[access])
            print(articleURL[access])


# Random Number Guesser______________________________________________________________________________________________
def numberGuess():
    global correctGuess  # Set Global Variable
    randInt = randint(0, 100)  # Generate a random int between 0 and 100

    # Ask the User to Guess the Number
    print("Guess a number between 0 and 100")
    userGuess = int(input())
    randStr = str(randInt)  # Convert to string for API callings

    # Make a request for JSON file
    url = "http://numbersapi.com/" + randStr + "?json"
    response = requests.get(url)
    data = json.loads(response.text)
    fact = data["text"]  # Retrieve Fun Fact

    # If the user guess is correct track their correct guesses
    if userGuess == randInt:
        print("CORRECT!")
        print("FUN FACT :", fact)
        correctGuess += 1
    else:
        print("INCORRECT!")
        print("FUN FACT :", fact)
    print("CORRECT GUESSES :", correctGuess)


# Main Functions_______________________________________________________________________________________________________
# Call weather Function
# Loop through functions until user would like to exit
while exit == False:
    print("Would you like to access the Weather or News or Number? : ")  # Check what the user would like to do
    choice = str(input())
    # Access Weather_____________________________________________________
    if choice == "weather" or choice == "Weather":
        weather(False)
        # Access News_____________________________________________________
    elif choice == "news" or choice == "News":
        news(False)
        # Access Number Guesser_________________________________________
    elif choice == "number" or choice == "Number":
        numberGuess()
        # Check if user would like to exit

    print("Would you like to exit? [y]/[n]: ")
    exitInput = str(input())
    if exitInput == "y":
        exit = True
    elif exitInput == "n":
        exit = False
