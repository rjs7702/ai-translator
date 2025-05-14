# Import necessary libraries
import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
import os

# Create recognizer objects
recog1 = spr.Recognizer()
recog2 = spr.Recognizer()

# Create microphone instance
mc = spr.Microphone(device_index=0)

# Capture voice command
with mc as source:
    recog1.adjust_for_ambient_noise(source, duration=1)
    print("Speak 'Hello' to initiate translation!")
    print("----------------------------")
    audio = recog1.listen(source)

# Initiate translation if "hello" is detected
if 'hello' in recog1.recognize_google(audio):
    recog1 = spr.Recognizer()
    translator = Translator()

    # Ask user for target language
    to_lang = input("Enter language code (e.g., 'hi' for Hindi, 'fr' for French, 'es' for Spanish): ")

    with mc as source:
        recog2.adjust_for_ambient_noise(source, duration=1)
        print("Speak a sentence to translate...")
        audio = recog2.listen(source)

    try:
        # Recognizing speech
        get_sentence = recog2.recognize_google(audio)
        print(f"Phrase to be translated: {get_sentence}")

        # Translating the text
        translated_text = translator.translate(get_sentence, src='en', dest=to_lang).text
        print(f"Translated text: {translated_text}")

        # **Saving the Translated Speech File**
        output_path = os.path.join(os.getcwd(), "captured_voice.mp3")
        speak = gTTS(text=translated_text, lang=to_lang, slow=False)
        speak.save("captured_voice.mp3")
        os.system("start captured_voice.mp3")

    except spr.UnknownValueError:
        print("Unable to understand the input.")
    except spr.RequestError as e:
        print(f"Request error: {e}")
