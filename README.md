# Jarvis AI - Voice Assistant

A Python-based voice assistant powered by Google's Gemini AI that can listen to voice commands, perform web searches, open websites, and engage in natural conversations.

## Features

- 🎤 **Voice Recognition**: Listens and responds to voice commands
- 🤖 **AI-Powered Conversations**: Uses Google Gemini 2.5 Flash for intelligent responses
- 🔍 **Web Search Integration**: Can search the web for real-time information
- 🌐 **Website Control**: Opens popular websites via voice commands
- 🕐 **Time Announcements**: Tells you the current time
- 🧠 **Persistent Memory**: Maintains conversation context (can be cleared on command)
- 🔊 **Text-to-Speech**: Responds using your system's TTS engine

## Prerequisites

- Python 3.7+
- macOS (uses `say` command for TTS - can be modified for other OS)
- Microphone for voice input
- Google Gemini API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd jarvis-ai
   ```

2. **Install required packages**
   ```bash
   pip install speechrecognition
   pip install pyaudio
   pip install python-dotenv
   pip install google-genai
   ```

   **Note**: On macOS, if `pyaudio` installation fails, try:
   ```bash
   brew install portaudio
   pip install pyaudio
   ```

3. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```bash
   touch .env
   ```
   
   Add your Gemini API key to the `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
   
   Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

Run the assistant:
```bash
python main.py
```

### Voice Commands

**Website Commands:**
- "Open YouTube"
- "Open Wikipedia"
- "Open Facebook"
- "Open Google"

**Utility Commands:**
- "What's the time?" / "Tell me the time"
- "Forget everything" / "Clear memory" - Clears conversation history
- "Stop" / "Exit" / "Bye" - Exits the program

**Conversational:**
- Ask any question, and Jarvis will use Gemini AI to respond
- Jarvis can search the web for current information
- Have multi-turn conversations with context retention

## Project Structure

```
jarvis-ai/
│
├── main.py                 # Main application file
├── .env                    # API key configuration (create this)
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Configuration

### Customizing Website Shortcuts

Edit the `sites` list in `main.py`:
```python
sites = [
    ["youtube", "https://www.youtube.com"],
    ["wikipedia", "https://www.wikipedia.com"],
    # Add more sites here
    ["github", "https://www.github.com"]
]
```

### Adjusting Audio Settings

Modify these parameters in the `takeCommand()` function:
```python
r.pause_threshold = 0.8          # Pause detection sensitivity
audio = r.listen(source, 
                 timeout=5,       # Max wait time for speech
                 phrase_time_limit=10)  # Max speech duration
```

### Changing AI Model

Update the model in `main.py`:
```python
GEMINI_MODEL = 'gemini-2.5-flash'  # or 'gemini-pro', etc.
```

## Troubleshooting

**Microphone not working:**
- Check system microphone permissions
- Ensure no other application is using the microphone
- Try adjusting ambient noise duration

**API errors:**
- Verify your API key is correct in `.env`
- Check your internet connection
- Ensure you haven't exceeded API rate limits

**TTS not working:**
- On non-macOS systems, replace `os.system(f"say '{safe_text}'")` with platform-specific TTS
- For Windows: Use `pyttsx3` library
- For Linux: Use `espeak` or `festival`

## Cross-Platform TTS Alternative

For cross-platform support, consider using `pyttsx3`:

```bash
pip install pyttsx3
```

Replace the `say()` function:
```python
import pyttsx3

engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API key confidential
- Add `.env` to `.gitignore`

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

MIT License - feel free to use this project for personal or educational purposes.

## Acknowledgments

- Google Gemini AI for conversational intelligence
- SpeechRecognition library for voice input
- Python community for excellent libraries

---

**Made with ❤️ by [Your Name]**
