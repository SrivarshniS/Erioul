import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Erioul:", text)
    engine.say(text)
    engine.runAndWait()
