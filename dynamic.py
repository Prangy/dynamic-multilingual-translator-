import speech_recognition as sr
import os
from google.cloud import translate_v2
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import playsound

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/prangyaparamita/Desktop/translator/credentials_google.json"  # For speech-to-text API

# Initialize recognizer
recognizer = sr.Recognizer()

# Record   audio from the microphone
with sr.Microphone() as source:
    print("Please say something...")
    audio = recognizer.listen(source)
# Initialize the Google Cloud Translate client
translate_client = translate_v2.Client()

# Get the list of supported languages
all_languages = translate_client.get_languages()

# Print the list of supported languages and their language codes
#print("Supported languages:")
#for lang in all_languages:
   # print(f"{lang['name']}: {lang['language']}")

# Recognize speech using Google Speech Recognition
try:
    print("Recognizing...")
    text = recognizer.recognize_google_cloud(audio)
    print("You said:", text)
    
    # Save the audio as a WAV file
    with open("output.wav", "wb") as f:
        f.write(audio.get_wav_data())
    print("Audio saved as output.wav")
    
    # Detect the language of the recognized text
    translate_client = translate_v2.Client()
    detection = translate_client.detect_language(text)
    detected_language_code = detection['language']
    print("Detected language:", detected_language_code)

    
    
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


# Translate text to English
target = "en"
translate_client = translate_v2.Client()
translation_eng = translate_client.translate(text, target)
print("English translation:", translation_eng["translatedText"])



# Load the pre-trained GPT model and tokenizer
model_name = "Helsinki-NLP/opus-mt-en-" + detected_language_code
model = MarianMTModel.from_pretrained(model_name)
tokenizer = MarianTokenizer.from_pretrained(model_name)

# Translate English text to the detected language using GPT
inputs = tokenizer.encode(translation_eng["translatedText"], return_tensors="pt")
translated_ids = model.generate(inputs, max_length=512)
translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
print("Translated text in target language:", translated_text)

# Convert translated text to speech using gTTS
tts = gTTS(translated_text, lang=detected_language_code)
tts.save("translated_audio.mp3")

# Play the audio
playsound.playsound("translated_audio.mp3")