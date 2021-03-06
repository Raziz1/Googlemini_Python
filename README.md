# Googlemini_Python 🐍📶
Google Home Mini + Python + WebScrapper

<p> 
  <img width = 256 height = 256 align='Right' src="https://github.com/Raziz1/Googlemini_Python/blob/main/image/googlehome_python.png? raw=true">
</p>

## Libraries & Resources 📚
* [googlehomepush](https://pypi.org/project/googlehomepush/)
  - [googlehomepush on GITHUB](https://github.com/deblockt/google-home-push)
* [Python Webscraping](https://realpython.com/beautiful-soup-web-scraper-python/)
* [OpenWeather API](https://openweathermap.org/)
* [Snowday Calculator](https://www.snowdaycalculator.com/calculator.php)
* [OSTA](http://www.ottawaschoolbus.ca/)
* [JSON parsing assistant](http://json.parser.online.fr/)

## Setup 📝
This project scrapes data from the internet and pushes text messages to a google home mini at a specific time
* Import the following libraries: googlehomepush, requests, time, BeautifulSoup, datetime
  - *If you do use OpenWeather API make sure you set up a free account and obtain your API key*
  - *For OpenWeather API you will have to scrape it like a JSON file which is included in the 'main.py'*
* Set the time you would like the script to send a text message to your Google Home mini
* Add your Google Home's IP address to the script. You can find your Google Home mini's IP address by doing the following: 
  - Navigate to the Google Home app > Click on the device > Click on the gear icon > Scroll down to the bottom where it says Information > IP address

## Windows Automation ⚙
You can tell Windows 10 or Mac Os to automatically run this script at specific times.
1. The first step is to turn the Python program into an executable application file. You can do this by following the instructions on the following website:
    1. [Turn Python script into Executable](https://datatofish.com/executable-pyinstaller/)
2. The next step is to create a scheduled task in the Windows Task Scheduler. You do this by following the instructions on the following website: 
    1. [Windows Task Scheduling](https://www.jcchouinard.com/python-automation-using-task-scheduler/)

## Notes 📜
* When Scheduling the task ensure you allow the task to wake the computer and take a look at your computer's power options
* Scheduled tasks will not work if the computer is hibernating
* If the laptop is sleeping and the lid is closed the task will not run (Unsolved). The lid has to be open
