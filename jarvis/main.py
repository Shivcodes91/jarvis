import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import os  # To access environment variables
import musiclibrary

# Initialize the speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Get the API key from environment variables
newsapi = os.getenv('NEWS_API_KEY')

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    """Function to process voice commands."""
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
        speak("Opening Instagram")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak(f"Sorry, I couldn't find the song {song}")
    
    elif "news" in c.lower():
        try:
            if not newsapi:
                speak("Sorry, no API key was provided for news.")
                return
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                if articles:
                    for article in articles[:5]:  # Limit to 5 headlines
                        speak(article['title'])
                else:
                    speak("Sorry, no news articles available.")
            else:
                speak("Sorry, I couldn't retrieve the news.")
        except Exception as e:
            speak(f"Error fetching news: {e}")
    elif "exit" in c.lower() or "stop" in c.lower():
        speak("Goodbye sir, exiting now.")
        exit()
    else:
        pass

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    while True:
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for the activation word 'Jarvis'...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Hello sir, how can I help you?")
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                    command = recognizer.recognize_google(audio)
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("Listening timed out, please try again.")
        except sr.UnknownValueError:
            print("Could not understand audio, please try again.")
        except sr.RequestError as e:
            print(f"Error with the request: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
