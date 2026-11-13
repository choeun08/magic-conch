
import pyttsx3

def speak(answer):
    engine = pyttsx3.init()

    engine.setProperty("rate", 185)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")

    for voice in voices:
        voice_info = (voice.name + " " + voice.id).lower()

        if "korean" in voice_info or "ko-kr" in voice_info or "한국" in voice_info:
            engine.setProperty("voice", voice.id)
            break

    engine.say(answer)
    engine.runAndWait()
    engine.stop()
