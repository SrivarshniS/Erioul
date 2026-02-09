# Erioul: Your Voice Task Organizer

Erioul is a smart voice assistant designed to help you organize multiple tasks seamlessly using natural language.

## 🚀 Getting Started

1. **Prerequisites**: Make sure you have Python 3.10+ installed.
2. **Install Dependencies**:
   ```bash
   pip install speechrecognition pyttsx3 dateparser pyaudio
   ```
   *(Note: `pyaudio` may require additional system libraries based on your OS.)*
3. **Run Erioul**:
   ```bash
   python main.py
   ```

## 🎙️ How to Use

1. Run the script and wait for the message: *"Hello, I am Erioul. Task organizer ready."*
2. **Press ENTER** when you are ready to talk.
3. Speak your command clearly into the microphone.
4. If Erioul asks for confirmation or more info, press ENTER again and speak.

## 💬 What can you say?

### ➕ Adding Tasks
You can add one or multiple tasks in a single sentence using natural language.
- *"Add buy milk tomorrow at 5pm"*
- *"Wake up at 7, do yoga at 8, and reach office by 10"*
- *"Remind me to call Mom in 20 minutes"*

### 📋 Viewing Tasks
- *"Show my tasks"*
- *"What's on my agenda?"*
- *"List my reminders"*

### 🗑️ Deleting Tasks
- *"Delete task 5"*
- *"Remove number 2"*
- *(Erioul will ask for confirmation before deleting)*

### 🆘 Help & Navigation
- *"Help"*: List available commands.
- *"Cancel"* or *"Stop"*: Terminate the current action.

## ✨ Advanced Features
- **Intelligent Splitting**: Automatically detects multiple tasks in one Go.
- **NLP Dates**: Understands "tomorrow", "next Friday", "in 10 minutes", etc.
- **Clarification**: If you forget to say a time, Erioul will ask you for it!
- **Background Reminders**: Reminders trigger automatically even when you aren't talking.
