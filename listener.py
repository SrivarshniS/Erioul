import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise and listen with a timeout
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)

        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()

    except sr.WaitTimeoutError:
        print("Listening timed out.")
        return None
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; check your internet connection: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
