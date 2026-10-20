
import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

try:
    with sr.Microphone() as source:
        print("Calibrating microphone. Stay quiet for 2 seconds...")
        recognizer.adjust_for_ambient_noise(source, duration=2)

        print("Energy threshold:", recognizer.energy_threshold)
        print("\nSpeak clearly now: NEXT TRACK")
        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=5
        )

        print("Audio captured! Recognizing...")
        print("Recognized:", recognizer.recognize_google(audio))

except sr.WaitTimeoutError:
    print("No speech detected. Check your microphone.")
except sr.UnknownValueError:
    print("Speech unclear. Try speaking closer to the microphone.")
except sr.RequestError as e:
    print("Internet or recognition service error:", e)
except Exception as e:
    print("Error:", repr(e))
