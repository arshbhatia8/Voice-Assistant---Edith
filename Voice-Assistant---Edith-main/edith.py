import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
import wikipedia
import pyjokes
import bs4
import requests
import warnings

warnings.filterwarnings("ignore")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
r = sr.Recognizer()


def speak(audio):
    print(audio)
    print("\n")
    engine.say(audio)
    print("\n")
    engine.runAndWait()


def greeting():
    hour = int(datetime.now().hour)
    if hour > 0 and hour < 12:
        speak("Good morning. I am your voice assistant Edith. What can I do for you?")
    elif hour > 12 and hour < 18:
        speak("Good afternoon. I am your voice assistant Edith. What can I do for you?")
    else:
        speak("Good evening. I am your voice assistant Edith. What can I do for you?")


def take_command():
    with sr.Microphone() as source:
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

            voice_data = r.recognize_google(audio)
            execute_command(voice_data)
        except Exception as e:
            print(e)


def execute_command(command):
    command = command.lower()
    print("You said: " + command)

    if " hey " in command or " hi " in command or "hello" in command:
        speak("hello there!")

    elif "open youtube" in command:
        speak("opening youtube")
        webbrowser.open("https://youtube.com")

    elif "open google" in command:
        speak("opening google")
        webbrowser.open("https://google.co.in")

    elif "github" in command:
        speak("opening github")
        webbrowser.open("https://github.com")

    elif "joke" in command or "jokes" in command:
        speak("Ok! let me tell you a programming joke.")
        joke = str(pyjokes.get_joke())
        speak(joke)
        speak("ha ha")

    elif "shut up" in command or "exit" in command or "bye" in command:
        speak("ok! See you later")
        exit()

    elif "wikipedia" in command or "search" in command:
        speak("Searching wikipedia....")
        if "wikipedia" in command:
            command = command.replace("wikipedia", "")
        if "search" in command:
            command = command.replace("search", "")
        results = wikipedia.summary(command, sentences=2)
        speak("According to wikipedia, ")
        speak(results)

    elif "play music" in command or "play a song" in command or "play songs" in command or "play song" in command:
        speak("Which song do you want me to play?")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=2)
            audio = r.listen(source)
            voice_data = r.recognize_google(audio)
            if voice_data == "any" or voice_data == "anything" or voice_data == "random":
                voice_data = "I love you baby"
            url = "https://www.youtube.com/results?search_query=" + voice_data
            speak("Playing " + voice_data)
            text = requests.get(url).text
            soup = bs4.BeautifulSoup(text)
            div = [d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
            for d in div:
                a0 = d.find_all('a')[0]
                a0 = [x for x in d.find_all('a') if x.has_attr('title')][0]
                webbrowser.open('https://www.youtube.com/' + a0['href'])
                break

    elif "play" in command and "song" in command and "random" in command or "any" in command:
        url = "https://www.youtube.com/results?search_query=" + "I love you baby"
        speak("Playing " + "i love you baby")
        text = requests.get(url).text
        soup = bs4.BeautifulSoup(text)
        div = [d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
        for d in div:
            a0 = d.find_all('a')[0]
            a0 = [x for x in d.find_all('a') if x.has_attr('title')][0]
            webbrowser.open('https://www.youtube.com/' + a0['href'])
            break

    elif "time" in command:
        now = datetime.now()
        hour = int(now.hour)
        minutes = int(now.minute)
        speak("The time is {} hours and {} minutes.".format(str(hour), str(minutes)))

    elif "how are you" in command or "what's up" in command or "whats up" in command:
        speak("Everything's great. Thanks for asking.")

    elif "what can you do for me" in command or "do something" in command:
        speak("I can play a song for you. i can tell you jokes. Try me.")

    elif "sing a song" in command:
        speak("I am a robot. I am not able to sing yet.")

    elif "talk to me" in command:
        speak("Hey I am talking to you")

    elif "nothing" in command:
        speak("I am so sorry. I am useless.")

    elif "maps" in command or "location" in command:
        speak("Which location do you want me to show you on maps? ")
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=2)
            audio = r.listen(source)
            voice_data = r.recognize_google(audio)
            url = "https://www.google.com/maps/place/" + voice_data
            speak("Locating {}...".format(voice_data))
            webbrowser.open(url)

    else:
        speak("Sorry. I did not get you.")


if __name__ == "__main__":
    greeting()
    while True:
        take_command()