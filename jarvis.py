import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import pywhatkit
import requests


# -------------------- TEXT TO SPEECH -------------------- #

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# -------------------- WISH ME -------------------- #

def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("I am Jarvis sir. Please tell me how may I help you?")


# -------------------- TAKE COMMAND -------------------- #

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception:
        print("Say that again please...")
        return "none"

    return query.lower()


# -------------------- WHATSAPP FUNCTION -------------------- #

def send_whatsapp_message(number, message):
    try:
        pywhatkit.sendwhatmsg_instantly(
            number, message, wait_time=10, tab_close=True, close_time=3
        )
        print("WhatsApp message sent successfully.")
    except Exception as e:
        print("Error:", e)
        speak("Sorry, I could not send the WhatsApp message.")


# -------------------- CONTACT LIST -------------------- #

contacts = {
    "devansh": "+913450993699",
    "mummy": "+919000000000",
    "papa": "+918000000000",
    "friend": "+917000000000"
}


# -------------------- WEATHER FUNCTION (NO API KEY) -------------------- #

def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        data = response.json()

        if "current_condition" not in data:
            return "Sorry, I could not find the weather for that city."

        current = data["current_condition"][0]
        temp = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        desc = current["weatherDesc"][0]["value"]

        report = f"The temperature in {city} is {temp} degree celsius, feels like {feels_like}, with {desc}."
        return report

    except Exception as e:
        print("Weather Error:", e)
        return "Sorry, I am not able to fetch the weather right now."


# -------------------- MAIN PROGRAM -------------------- #

if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand()

        # ---------------- WIKIPEDIA ---------------- #
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except:
                speak("Sorry, I could not find results.")

        # ---------------- OPEN WEBSITES ---------------- #
        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://google.com")

        elif 'open geeksforgeeks' in query:
            webbrowser.open("https://geeksforgeeks.org")

        # ---------------- TIME ---------------- #
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        # ---------------- SYSTEM CONTROL ---------------- #
        elif 'shutdown' in query:
            speak("Shutting down the system. Goodbye!")
            os.system("shutdown /s /t 1")

        elif 'restart' in query:
            speak("Restarting your system.")
            os.system("shutdown /r /t 1")

        elif 'log out' in query or 'logout' in query:
            speak("Logging out now.")
            os.system("shutdown -l")

        # ---------------- WHATSAPP MESSAGE ---------------- #
        elif 'send message' in query or 'whatsapp' in query:
            speak("Who do you want to message?")
            name = takeCommand()

            number = contacts.get(name)

            if number is None:
                speak("I don't have this contact saved. Please say the full mobile number.")
                number = takeCommand()

            speak("What should I say?")
            message = takeCommand()

            speak("Sending your message on WhatsApp.")
            send_whatsapp_message(number, message)
            speak("Message sent successfully.")

        # ---------------- WEATHER ---------------- #
        elif 'weather' in query or 'temperature' in query:
            speak("For which city do you want the weather?")
            city = takeCommand()

            if city == "none":
                speak("Sorry, I did not get the city name.")
            else:
                report = get_weather(city)
                print(report)
                speak(report)

        # ---------------- EXIT ---------------- #
        elif 'quit' in query or 'exit' in query or 'stop' in query:
            speak("Goodbye sir. Have a nice day!")
            break


