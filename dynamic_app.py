from flask import Flask, request, jsonify
import os
import speech_recognition as sr
from google.cloud import translate_v2
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import playsound
from pymongo import MongoClient


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/prangyaparamita/Desktop/translator/credentials_google.json"  # For speech-to-text API

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb+srv://pragyaparamita08:user@cluster0.vafrivl.mongodb.net/')
db = client['chatbot']
collection = db['customize']

# Function to record audio from the microphone
def record_audio(wav_file):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source, timeout=10)  # Adjust the timeout as needed
    with open(wav_file, "wb") as f:
        f.write(audio.get_wav_data())
    return wav_file


# Function to translate text to English
def translate_to_english(text):
    translate_client = translate_v2.Client()
    translation = translate_client.translate(text, target_language="en")
    return translation['translatedText']

# Function to translate text using GPT
def translate_with_gpt(text, detected_language_code):
    model_name = "Helsinki-NLP/opus-mt-en-" + detected_language_code
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    inputs = tokenizer.encode(text, return_tensors="pt")
    translated_ids = model.generate(inputs, max_length=512)
    translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
    return translated_text

# Function to convert text to speech using gTTS
def text_to_speech(text, output_file):
    tts = gTTS(text, lang='en')
    tts.save(output_file)

@app.route('/article_query', methods=['POST'])
def get_query():
    # Extract parameters from the form data
    query = request.json.get('query')
    user_id = request.json.get('userID')
    chatbot_id = request.json.get('chatbotID')

    if not query or not user_id or not chatbot_id:
        return jsonify({"error": "query, userID, or chatbotID not provided", "success": False}), 400

    try:
        # Record audio from the user
        audio_file = f"/Users/prangyaparamita/Desktop/translator/output.wav"
        record_audio(audio_file)


        # Recognize speech using Google Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google_cloud(audio_data)

        # Detect the language of the recognized text
        translate_client = translate_v2.Client()
        detection = translate_client.detect_language(text)
        detected_language_code = detection['language']

        # Translate text to English
        translated_text = translate_to_english(text)
        # Translate English text to the detected language using GPT
        translated_text_gpt = translate_with_gpt(translated_text, detected_language_code)

        # Convert translated text to speech using gTTS
        audio_output_file = f"{user_id}_{chatbot_id}_audio.mp3"
        text_to_speech(translated_text_gpt, audio_output_file)

        # Prepare the data to be inserted into MongoDB
        data = {
            "query": query,
            "userID": user_id,
            "chatbotID": chatbot_id,
            "recognized_text": text,
            "translated_text": translated_text,
            "translated_text_gpt": translated_text_gpt,
            "audio_file": audio_output_file
        }
        # Insert the data into the MongoDB collection
        collection.insert_one(data)

        # Return the response
        response_data = {
            "query": query,
            "userID": user_id,
            "chatbotID": chatbot_id,
            "recognized_text": text,
            "translated_text": translated_text,
            "translated_text_gpt": translated_text_gpt,
            "audio_file": audio_output_file
        }
        return jsonify({"success": True, "data": response_data}), 200

    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

if __name__ == '__main__':
    app.run(debug=True)
