from listener import listen
from speaker import speak
from intent_parser import parse_intent
from scheduler import add_task, check_reminders
import threading

# start reminder thread
threading.Thread(target=check_reminders, daemon=True).start()

speak("Hello, I am Erioul.")

while True:
    input("Press ENTER to talk...")
    speak("I'm listening")

    text = listen()

    if not text:
        speak("Sorry, I didn't understand.")
        continue

    intent = parse_intent(text)

    if not intent:
        speak("I couldn't find a time in that.")
        continue

    speak(
        f"You have {intent['task']} at {intent['time']}. Should I save this?"
    )

    confirmation = listen()

    if "yes" in confirmation:
        add_task(intent['task'], intent['date'], intent['time'])
        speak("Task saved.")
    else:
        speak("Okay, not saved.")
