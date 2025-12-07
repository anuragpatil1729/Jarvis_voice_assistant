# 🤖 Jarvis AI Assistant

A sophisticated voice-activated AI assistant powered by Google's Gemini 2.5 Flash, designed to help you manage tasks, control your Mac, and interact intelligently with your digital environment.

## ✨ Features

### Core Capabilities
- **Voice & Text Modes**: Switch between voice commands or text input
- **Gemini AI Integration**: Persistent chat sessions with Google Search capabilities
- **Password Protection**: Secure access with authentication system
- **Memory System**: Remember personal information and preferences
- **Task Management**: Built-in to-do list functionality

### System Control (macOS)
- **Application Launcher**: Open Chrome, VS Code, Spotify, Notes, Calculator, and more
- **Volume Control**: Set, mute, or maximize system volume
- **File Management**: Create folders, list files, delete files on Desktop
- **Screenshot Capture**: Take and save screenshots instantly

### Productivity Features
- **Web Navigation**: Quick access to YouTube, Wikipedia, Facebook, Google, GitHub
- **Alarm System**: Set time-based alarms with natural language
- **WhatsApp Messaging**: Schedule and send WhatsApp messages (optional)
- **Time Queries**: Check current time on demand

## 🚀 Installation

### Prerequisites
- macOS (for system-specific features)
- Python 3.8 or higher
- Google Gemini API key

### Required Python Packages

```bash
pip install google-genai
pip install SpeechRecognition
pip install pyaudio
pip install python-dotenv
pip install pywhatkit  # Optional, for WhatsApp features
```

### Setup Steps

1. **Clone or download the project**
```bash
cd jarvisAI
```

2. **Create a `.env` file** in the project directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

3. **Get your Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy it to your `.env` file

4. **Configure the assistant** (optional):
   - Edit `PASSWORD` in `main.py` to set your own password
   - Update `WHATSAPP_CONTACTS` with your contacts' phone numbers
   - Add more apps to the `APPS` dictionary as needed

## 🎯 Usage

### Starting Jarvis

```bash
python main.py
```

1. Enter the password when prompted (default: `anuragpatil`)
2. Select mode:
   - Press `1` for Voice Mode (speak commands)
   - Press `2` for Text Mode (type commands)

### Example Commands

#### Basic Interactions
```
"Hello Jarvis"
"What time is it?"
"Exit" / "Goodbye"
```

#### Web Navigation
```
"Open YouTube"
"Open Google"
"Open GitHub"
```

#### Application Control
```
"Open Chrome"
"Open VS Code"
"Open Spotify"
```

#### System Control
```
"Set volume to 50"
"Mute volume"
"Max volume"
"Take screenshot"
```

#### File Management
```
"Create folder ProjectFiles"
"List files"
"Delete file example.txt"
```

#### Memory System
```
"Remember that my birthday is 15th October"
"What do you remember?"
"When is my birthday?"
```

#### Task Management
```
"Add task buy groceries"
"Show my tasks"
"Clear tasks"
```

#### Alarms
```
"Set alarm for 7 am"
"Set alarm for 6:30 pm"
```

#### WhatsApp Messaging (if configured)
```
"Send WhatsApp to Anurag saying Hello, how are you?"
```

#### AI Conversations
Ask Jarvis anything! It uses Gemini AI with Google Search:
```
"What's the weather today?"
"Explain quantum computing"
"What are the latest tech news?"
```

## 📁 File Structure

```
jarvisAI/
├── main.py                 # Main application file
├── jarvis_memory.json      # Stores memories (auto-created)
├── jarvis_tasks.json       # Stores tasks (auto-created)
├── .env                    # API keys (create this)
└── README.md              # This file
```

## 🔒 Security Features

- Password authentication with 3-attempt limit
- Secure API key storage via environment variables
- Local data storage (no cloud sync by default)

## ⚙️ Configuration

### Customizing Applications

Edit the `APPS` dictionary in `main.py`:

```python
APPS = {
    "chrome": "Google Chrome",
    "vscode": "Visual Studio Code",
    "yourapp": "Your Application Name",
}
```

### Adding WhatsApp Contacts

Edit the `WHATSAPP_CONTACTS` dictionary:

```python
WHATSAPP_CONTACTS = {
    "name": "+91XXXXXXXXXX",
    "friend": "+1XXXXXXXXXX",
}
```

### Changing Password

Update the `PASSWORD` variable:

```python
PASSWORD = "your_new_password"
```

## 🎤 Voice Mode Tips

- Speak clearly and at a moderate pace
- Wait for "Listening..." prompt before speaking
- Minimize background noise for better recognition
- If recognition fails, the system will wait for the next command

## 🐛 Troubleshooting

**Speech recognition not working:**
- Install/reinstall PyAudio: `pip install pyaudio`
- Check microphone permissions in System Preferences
- Try text mode if issues persist

**Gemini API errors:**
- Verify your API key in `.env` file
- Check your API quota at [Google AI Studio](https://aistudio.google.com)
- Ensure internet connection is stable

**App launching not working:**
- Verify exact application names in macOS Applications folder
- Update `APPS` dictionary with correct names

## 📝 Notes

- Memory and task data are stored locally in JSON files
- Chat history persists until you say "forget everything" or restart
- WhatsApp messaging requires phone to be connected to internet
- Some features are macOS-specific (volume control, app launching)

## 🤝 Contributing

Feel free to customize and extend Jarvis for your needs! Some ideas:
- Add more application shortcuts
- Integrate with additional APIs
- Create custom voice commands
- Add reminder notifications
- Implement email functionality

## 📜 License

This project is open source and available for personal use and modification.

## 🙏 Acknowledgments

- Powered by [Google Gemini AI](https://ai.google.dev/)
- Speech recognition by Google Speech API
- Built with Python ❤️

---

**Your birthday has been remembered:** October 15th 🎂

Made with 🧠 by your local AI enthusiast
