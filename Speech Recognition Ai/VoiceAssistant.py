import os
import smtplib
import webbrowser as wb
import playsound

import requests
import speech_recognition as sr
import pandas_datareader.data as pdd
import datetime as dt
import matplotlib.pyplot as mpl
from matplotlib import style
from gtts import gTTS
from time import ctime

c = sr.Recognizer()  # Creating instance to recognize speech.


def JARVIS(voice):
    """Creating a function to allow JARVIS to speak"""

    tts = gTTS(text=voice, lang="en")  # Setting text to speech and setting lang to English.
    sound_file = "voice.mp3"
    tts.save(sound_file)  # Saving audio file in same folder as script, allowing playback.
    playsound.playsound(sound_file)  # Play audio file
    print(voice)
    os.remove(sound_file)


def myCommands(ask=""):
    """Listens for commands"""

    with sr.Microphone() as source:
        if ask:
            JARVIS(ask)
        c.pause_threshold = 1  # Creating pause threshold allowing time before and after commands
        c.adjust_for_ambient_noise(source, duration=1)  # Stops background noise affecting accuracy.
        sound = c.listen(source)  # Speech recognizer listening at source.

        try:
            task = c.recognize_google(sound)  # Creating variable to capture speech.

            return task.lower()

        # Creating loop to continuously listen to commands in the event speech is not recognised.
        except sr.UnknownValueError:
            JARVIS("I do not comprehend.")
            task = myCommands()

            return task.lower()

        except sr.RequestError:
            JARVIS("Unfortunately, services are down.")

            return task.lower()


def assistant(task):
    """if statements tasked with executing commands"""

    if "google" in task:  # Activates when "Google" is heard, "recognize_google" uses Google Chrome.
        Google = myCommands("What do you want to search for?")
        url = "https://google.com/search?q=" + Google  # Passing url
        wb.get().open_new(url)
        JARVIS("Returning results for " + Google)

    elif "youtube" in task:  # Activates when "Youtube" is heard.
        YouTube = myCommands("What videos do you want to search for?")
        url = "https://www.youtube.com/results?search_query=" + YouTube  # Passing url
        wb.get().open_new(url)
        JARVIS("Returning results for " + YouTube)

    if "facebook" in task:
        url = "https://www.facebook.com/"  # Passing url
        wb.get().open_new(url)
        JARVIS("Opening Facebook")

    elif "twitter" in task:
        url = "https://twitter.com/"  # Passing url
        wb.get().open_new(url)
        JARVIS("Opening Twitter")

    if "reddit" in task:
        url = "https://www.reddit.com/"  # Passing url
        wb.get().open_new(url)
        JARVIS("Opening Reddit")

    elif "locate" in task:
        area = myCommands("What is the Location?")
        url = "https://google.nl/maps/place/" + area + "/&amp"
        wb.get().open_new(url)
        JARVIS("Here\"s the location of " + area)

    if "weather status" in task:
        City = myCommands("Enter your city : ")
        url = "http://openweathermap.org/data/2.5/weather?q={}&" \
              "appid=439d4b804bc8187953eb36d2a8c26a02&units=metric".format(City)
        res = requests.get(url)
        data = res.json()

        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']
        description = data['weather'][0]['description']

        JARVIS("Temperature : {} degree celsius".format(temp))
        JARVIS("Wind Speed : {} m/s".format(wind_speed))
        JARVIS("Latitude : {}".format(latitude))
        JARVIS("Longitude : {}".format(longitude))
        JARVIS("Description : {}".format(description))
        JARVIS("Finished stating the weather status for " + City)

    elif "finance" in task:
        JARVIS('Beginning to retrieve finance data.')
        style.use('ggplot')

        start = dt.datetime(2000, 1, 1)
        finish = dt.datetime(2017, 1, 1)
        CompanyTicker = myCommands('Say the companies ticker')

        df = pdd.DataReader(CompanyTicker, 'yahoo', start, finish)
        print(df[['Open', 'High']].head)
        df['Adj Close'].plot()
        mpl.show()

    if "email" in task:
        recipient = myCommands("Who is the recipient")

        if "friend" in recipient:

            Username = "doryansadi@gmail.com"
            Recipient = "cherylbartels4@gmail.com"
            Password = input(str("Please enter your password : "))
            Content = myCommands("What should I say?")

            # init gmail SMTP
            mail = smtplib.SMTP("smtp.gmail.com", 587)

            # Encrypting session
            mail.starttls()

            # login
            mail.login(Username, Password)
            print("Successfully logged in")

            # Send Message
            mail.sendmail(Username, Recipient, Content)
            JARVIS("Email has been sent")

            # Closing Connection
            mail.close()

        else:
            JARVIS("I do not comprehend!")
            recipient = myCommands()

            return recipient

    elif "what is your name" in task:
        JARVIS("My name is JARVIS")

    if "what is the time" in task:
        JARVIS(ctime())

    elif "what is your status" in task:
        JARVIS("All systems are operational")
    if "joke" in task:
        res = requests.get(
            "https://icanhazdadjoke.com/",
            headers={"Accept": "application/json"}
        )
        if res.status_code == requests.codes.ok:
            JARVIS(str(res.json()["joke"]))
        else:
            JARVIS("Sorry! I got no more funnies.")

    elif "exit" in task:
        JARVIS("Goodbye")
        exit()


JARVIS("How may I be of assistance?")

# Continues executing multiple commands
while True:
    assistant(myCommands())
