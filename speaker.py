import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print("Erioul:", text)
    engine.say(text)
    engine.runAndWait()
