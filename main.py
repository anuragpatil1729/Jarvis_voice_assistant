import speech_recognition as sr
import os
import webbrowser
import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

# --- LOAD ENVIRONMENT VARIABLES ---
# This line reads the GEMINI_API_KEY from the .env file and sets it in os.environ
load_dotenv()
# ----------------------------------


# --- Setup Jarvis AI Client, Tools, and Chat Session ---

try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Jarvis AI Client: {e}")
    print("Please ensure you have the 'python-dotenv' package installed and your key is in a '.env' file.")
    exit()

GEMINI_MODEL = 'gemini-2.5-flash'
SEARCH_TOOL = types.Tool(google_search=types.GoogleSearch())
GENERATION_CONFIG = types.GenerateContentConfig(
    tools=[SEARCH_TOOL]
)

jarvis_chat = None


def initialize_chat():
    """Initializes or resets the persistent chat session, and enables the Google Search tool."""
    global jarvis_chat
    try:
        jarvis_chat = client.chats.create(
            model=GEMINI_MODEL,
            config=GENERATION_CONFIG
        )
        print("Jarvis AI chat session initialized/reset with Google Search enabled.")
        return True
    except Exception as e:
        print(f"Error initializing Jarvis AI Chat: {e}")
        return False


if not initialize_chat():
    exit()


# --------------------------------------------


# 🟢 FIX APPLIED HERE: ESCAPING SINGLE QUOTES
def say(text):
    """Uses the system's text-to-speech to speak the given text, safely handling quotes."""
    # Replace single quotes (') with an escaped single quote (\') to prevent shell syntax errors
    safe_text = text.replace("'", r"\'")

    # Use the safe_text in the os.system call
    os.system(f"say '{safe_text}'")


def takeCommand():
    """Listens for audio input from the microphone and returns the recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return "sorry from Jarvis, I did not catch that."
        except Exception as e:
            return "some Error Occurred. sorry from Jarvis"


def get_jarvis_response(prompt):
    """Sends the user's prompt to the persistent Jarvis AI chat session and returns the response."""
    print("Jarvis is thinking...")
    global jarvis_chat
    if jarvis_chat is None:
        return "Sorry, my core is offline. Please initialize the chat."

    try:
        response = jarvis_chat.send_message(prompt)
        return response.text
    except APIError as e:
        return f"Jarvis AI Core Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    print('pycharm - Jarvis is starting up...')
    say("Hello, I am Jarvis A.I. Welcome Back boss.")

    while True:
        query = takeCommand().lower()

        if not query or "sorry from jarvis" in query:
            if "sorry from jarvis" in query:
                say("I did not catch that. Please try again.")
            continue

        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["facebook", "https://www.facebook.com"],
            ["google", "https://www.google.com"]
        ]

        handled = False

        # --- Check Predefined Commands ---

        # 1. Website Opening Logic
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]}, sir.")
                webbrowser.open(site[1])
                handled = True
                break

        if handled:
            continue

        # 2. Time command
        if "the time" in query:
            time_str = datetime.datetime.now().strftime("%I:%M %p")
            say(f"Sir, the time is {time_str}")
            handled = True

        if handled:
            continue

        # 3. Clear Memory Command
        if "forget everything" in query or "clear memory" in query:
            if initialize_chat():
                say("My conversational memory has been completely wiped, sir.")
            else:
                say("I was unable to clear my memory.")
            handled = True

        if handled:
            continue

        # 4. Exit/Stop Command
        elif "stop" in query or "exit" in query or "bye" in query:
            say("Goodbye, sir.")
            break

        # 5. Jarvis Conversational Logic
        else:
            jarvis_response = get_jarvis_response(query)
            print(f"Jarvis: {jarvis_response}")
            say(jarvis_response)