import os
import re
import time
import json
import threading
import datetime
import webbrowser

import speech_recognition as sr
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

# Optional: WhatsApp messaging
try:
    import pywhatkit
except ImportError:
    pywhatkit = None

# ----------------- SECURITY & MODE -----------------

PASSWORD = "anuragpatil"
USE_VOICE = True  # will be set by select_mode()

def authenticate():
    """Ask for password up to 3 times."""
    for attempt in range(3):
        pwd = input("🔒 Enter Jarvis password: ").strip()
        if pwd == PASSWORD:
            print("✅ Access granted.\n")
            return True
        else:
            print("❌ Wrong password.")
    print("🚫 Access denied. Exiting.")
    return False


def select_mode():
    """Choose voice or text mode."""
    global USE_VOICE
    print("🎛 Select Mode:")
    print("1. Voice Mode (default)")
    print("2. Text Mode")
    choice = input("Enter choice (1 or 2): ").strip()
    USE_VOICE = (choice != "2")
    if USE_VOICE:
        print("🎤 Voice mode activated.\n")
    else:
        print("⌨ Text mode activated.\n")


# ----------------- ENV + GEMINI SETUP -----------------

load_dotenv()

try:
    client = genai.Client()  # assumes API key from env
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    print("Make sure GEMINI_API_KEY is set in your .env file.")
    raise SystemExit(1)

GEMINI_MODEL = "gemini-2.5-flash"
SEARCH_TOOL = types.Tool(google_search=types.GoogleSearch())
GENERATION_CONFIG = types.GenerateContentConfig(
    tools=[SEARCH_TOOL]
)

jarvis_chat = None  # global chat session


def initialize_chat():
    """Create / reset persistent Gemini chat session."""
    global jarvis_chat
    try:
        jarvis_chat = client.chats.create(
            model=GEMINI_MODEL,
            config=GENERATION_CONFIG
        )
        print("✅ Jarvis AI chat session initialized with Google Search.")
        return True
    except Exception as e:
        print(f"Error initializing Jarvis chat: {e}")
        return False


if not initialize_chat():
    raise SystemExit(1)


# ----------------- PATHS & CONFIG -----------------

MEMORY_FILE = "jarvis_memory.json"
TASKS_FILE = "jarvis_tasks.json"
DESKTOP_PATH = os.path.join(os.path.expanduser("~"), "Desktop")

# macOS application names
APPS = {
    "chrome": "Google Chrome",
    "google chrome": "Google Chrome",
    "vscode": "Visual Studio Code",
    "visual studio code": "Visual Studio Code",
    "spotify": "Spotify",
    "notes": "Notes",
    "calculator": "Calculator",
}

# WhatsApp contacts (edit phone numbers)
WHATSAPP_CONTACTS = {
    "anurag": "+91XXXXXXXXXX",
    "boss": "+91XXXXXXXXXX",
}

# ----------------- JSON UTILITIES -----------------

def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving JSON to {path}: {e}")


# ----------------- SPEECH / I/O -----------------

def say(text: str):
    """Speak or print depending on mode."""
    if USE_VOICE:
        safe_text = text.replace("'", r"\'")
        os.system(f"say '{safe_text}'")
    else:
        print(f"Jarvis ▶ {text}")


def takeCommand() -> str:
    """Return user input from mic (voice mode) or console (text mode)."""
    if not USE_VOICE:
        try:
            return input("You ▶ ").strip().lower()
        except EOFError:
            return ""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            query = r.recognize_google(audio, language="en-in")
            print(f"You ▶ {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print("Speech error:", e)
            return ""


# ----------------- GEMINI RESPONSE -----------------

def get_jarvis_response(prompt: str) -> str:
    global jarvis_chat
    if jarvis_chat is None:
        return "My core is offline, sir. Please reinitialize my chat."

    try:
        print("Jarvis is thinking...")
        response = jarvis_chat.send_message(prompt)
        return response.text
    except APIError as e:
        return f"Jarvis AI Core Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# ----------------- MEMORY SYSTEM -----------------

def add_memory(memory_text: str):
    memories = load_json(MEMORY_FILE, [])
    memories.append(memory_text)
    save_json(MEMORY_FILE, memories)


def get_memories():
    return load_json(MEMORY_FILE, [])


def find_memory_about(keyword: str):
    for m in get_memories():
        if keyword.lower() in m.lower():
            return m
    return None


# ----------------- TO-DO SYSTEM -----------------

def add_task(task_text: str):
    tasks = load_json(TASKS_FILE, [])
    tasks.append(task_text)
    save_json(TASKS_FILE, tasks)


def get_tasks():
    return load_json(TASKS_FILE, [])


def clear_tasks():
    save_json(TASKS_FILE, [])


# ----------------- ALARM SYSTEM -----------------

def parse_time_string(time_str: str):
    """
    Parse '6', '6:30', '6 am', '6:30 pm'.
    Return (hour_24, minute).
    """
    time_str = time_str.strip().lower()
    am = "am" in time_str
    pm = "pm" in time_str
    time_str = time_str.replace("am", "").replace("pm", "").strip()

    if ":" in time_str:
        h_str, m_str = time_str.split(":", 1)
        hour = int(h_str.strip())
        minute = int(m_str.strip())
    else:
        hour = int(time_str.strip())
        minute = 0

    if pm and hour < 12:
        hour += 12
    if am and hour == 12:
        hour = 0

    return hour, minute


def alarm_thread(message: str, delay_seconds: float):
    time.sleep(delay_seconds)
    say(message)


def set_alarm_from_query(query: str):
    match = re.search(r"set alarm for ([0-9: ]+(am|pm)?)", query)
    if not match:
        say("Sorry, I could not understand the alarm time, sir.")
        return

    time_str = match.group(1)
    try:
        hour, minute = parse_time_string(time_str)
        now = datetime.datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target <= now:
            target += datetime.timedelta(days=1)

        delay = (target - now).total_seconds()
        threading.Thread(
            target=alarm_thread,
            args=("Sir, this is your alarm.", delay),
            daemon=True
        ).start()
        say(f"Alarm set for {target.strftime('%I:%M %p')}, sir.")
    except Exception as e:
        print("Alarm error:", e)
        say("Something went wrong while setting the alarm, sir.")


# ----------------- VOLUME CONTROL (macOS) -----------------

def set_volume_percent(percent: int):
    percent = max(0, min(100, percent))
    os.system(f"osascript -e 'set volume output volume {percent}'")


def handle_volume_command(query: str) -> bool:
    if "mute" in query:
        set_volume_percent(0)
        say("Volume muted, sir.")
        return True

    if "max volume" in query or "full volume" in query:
        set_volume_percent(100)
        say("Volume set to maximum, sir.")
        return True

    match = re.search(r"set volume to (\d+)", query)
    if match:
        vol = int(match.group(1))
        set_volume_percent(vol)
        say(f"Volume set to {vol} percent, sir.")
        return True

    return False


# ----------------- OPEN LOCAL APPS (macOS) -----------------

def handle_open_app(query: str) -> bool:
    if not query.startswith("open "):
        return False

    name = query.replace("open ", "", 1).strip()
    app_name = None

    if name in APPS:
        app_name = APPS[name]
    else:
        for key, value in APPS.items():
            if key in name:
                app_name = value
                break

    if not app_name:
        return False

    os.system(f"open -a '{app_name}'")
    say(f"Opening {app_name}, sir.")
    return True


# ----------------- FILE / FOLDER & SCREENSHOT -----------------

def handle_file_folder_commands(query: str) -> bool:
    # Create folder on Desktop
    if "create folder" in query:
        match = re.search(r"create folder (.+)", query)
        if match:
            folder_name = match.group(1).strip()
            folder_path = os.path.join(DESKTOP_PATH, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            say(f"Folder {folder_name} created on your desktop, sir.")
            return True

    # List files on Desktop
    if "list files" in query or "show files" in query:
        try:
            items = os.listdir(DESKTOP_PATH)
            if not items:
                say("Your desktop is empty, sir.")
            else:
                say("Files and folders on your desktop include:")
                for item in items[:7]:
                    say(item)
                print("\nAll items on desktop:")
                for item in items:
                    print(item)
            return True
        except Exception as e:
            print("Desktop list error:", e)
            say("I could not access the desktop, sir.")
            return True

    # Delete file on Desktop
    if "delete file" in query:
        match = re.search(r"delete file (.+)", query)
        if match:
            file_name = match.group(1).strip()
            file_path = os.path.join(DESKTOP_PATH, file_name)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    say(f"File {file_name} deleted from your desktop, sir.")
                except Exception as e:
                    print("Delete error:", e)
                    say("I was unable to delete that file, sir.")
            else:
                say("I could not find that file on your desktop, sir.")
            return True

    # Screenshot
    if "screenshot" in query or "take screenshot" in query:
        screenshot_path = os.path.join(DESKTOP_PATH, "jarvis_screenshot.png")
        os.system(f"screencapture '{screenshot_path}'")
        say("Screenshot taken and saved on your desktop, sir.")
        return True

    return False


# ----------------- WHATSAPP MESSAGING -----------------

def handle_whatsapp_command(query: str) -> bool:
    if "send whatsapp" not in query:
        return False

    if pywhatkit is None:
        say("WhatsApp messaging is not ready. Please install pywhatkit first, sir.")
        return True

    match = re.search(r"send whatsapp to ([a-zA-Z ]+) saying (.+)", query)
    if not match:
        say("Please say: send WhatsApp to name saying your message, sir.")
        return True

    name = match.group(1).strip().lower()
    message = match.group(2).strip()

    phone = WHATSAPP_CONTACTS.get(name)
    if not phone:
        say(f"I don't have a WhatsApp number saved for {name}, sir.")
        return True

    now = datetime.datetime.now()
    send_minute = now.minute + 2
    send_hour = now.hour
    if send_minute >= 60:
        send_minute -= 60
        send_hour = (send_hour + 1) % 24

    try:
        say(f"Scheduling WhatsApp message to {name}, sir.")
        pywhatkit.sendwhatmsg(
            phone,
            message,
            send_hour,
            send_minute,
            wait_time=10,
            tab_close=True
        )
        say("WhatsApp message sent or scheduled, sir.")
    except Exception as e:
        print("WhatsApp error:", e)
        say("Something went wrong while sending the WhatsApp message, sir.")

    return True


# ----------------- MAIN LOOP -----------------

if __name__ == "__main__":
    print("🧠 Jarvis Security System Booting...\n")

    if not authenticate():
        raise SystemExit(0)

    select_mode()

    say("Hello, I am Jarvis A.I. Welcome back, boss.")

    while True:
        query = takeCommand()
        if not query:
            continue

        # --------- Exit / Stop ---------
        if any(word in query for word in ["exit", "stop", "bye", "goodbye", "shutdown"]):
            say("Goodbye, sir.")
            break

        handled = False

        # --------- Open Websites ---------
        sites = [
            ("youtube", "https://www.youtube.com"),
            ("wikipedia", "https://www.wikipedia.org"),
            ("facebook", "https://www.facebook.com"),
            ("google", "https://www.google.com"),
            ("github", "https://github.com"),
        ]
        for name, url in sites:
            if f"open {name}" in query:
                say(f"Opening {name}, sir.")
                webbrowser.open(url)
                handled = True
                break
        if handled:
            continue

        # --------- Time ---------
        if "the time" in query or "what time" in query:
            time_str = datetime.datetime.now().strftime("%I:%M %p")
            say(f"Sir, the time is {time_str}.")
            continue

        # --------- Clear AI Chat Memory ---------
        if "forget everything" in query or "clear memory" in query:
            if initialize_chat():
                say("My conversational memory has been wiped, sir.")
            else:
                say("I was unable to reset my core, sir.")
            continue

        # --------- Volume Commands ---------
        if handle_volume_command(query):
            continue

        # --------- Open Local Apps ---------
        if handle_open_app(query):
            continue

        # --------- File / Folder / Screenshot ---------
        if handle_file_folder_commands(query):
            continue

        # --------- Alarm ---------
        if "set alarm for" in query:
            set_alarm_from_query(query)
            continue

        # --------- Memory Commands ---------
        if query.startswith("remember that"):
            mem_text = query.replace("remember that", "", 1).strip(" .")
            if mem_text:
                add_memory(mem_text)
                say("Got it, I will remember that, sir.")
            else:
                say("Please tell me what to remember, sir.")
            continue

        if "what do you remember" in query or "show my memories" in query:
            memories = get_memories()
            if not memories:
                say("I don't have any memories stored yet, sir.")
            else:
                say("Here are some things I remember, sir.")
                for m in memories[:5]:
                    say(m)
            continue

        if "my birthday" in query:
            mem = find_memory_about("birthday")
            if mem:
                say(f"You once told me that {mem}")
            else:
                say("I don't know your birthday yet, sir. You can say, remember that my birthday is...")
            continue

        # --------- To-Do List ---------
        if "add task" in query:
            task = query.split("add task", 1)[1].strip(" .")
            if task:
                add_task(task)
                say("Task added to your list, sir.")
            else:
                say("Please tell me the task to add, sir.")
            continue

        if "show my tasks" in query or "show tasks" in query or "list my tasks" in query:
            tasks = get_tasks()
            if not tasks:
                say("You have no tasks in your list, sir.")
            else:
                say("Here are your tasks, sir.")
                for i, t in enumerate(tasks, start=1):
                    say(f"Task {i}: {t}")
            continue

        if "clear tasks" in query or "delete all tasks" in query:
            clear_tasks()
            say("All tasks have been cleared, sir.")
            continue

        # --------- WhatsApp ---------
        if handle_whatsapp_command(query):
            continue

        # --------- Default: Gemini Conversation ---------
        reply = get_jarvis_response(query)
        print(f"Jarvis ▶ {reply}")
        say(reply)