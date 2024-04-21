
**Multilingual Chatbot with Speech Recognition and Translation**

This project is a Flask-based chatbot that incorporates speech recognition, translation, and text-to-speech functionalities. It allows users to interact with the chatbot by speaking, which is then transcribed, translated into English, processed using a GPT-based model for language translation, and finally converted back into speech.

**Key Features:**
- **Speech Recognition:** Utilizes Google Speech Recognition API to transcribe user input from speech to text.
- **Translation:** Translates the transcribed text into English using the Google Cloud Translation API.
- **Language Translation with GPT:** Uses a MarianMT model from Hugging Face's Transformers library to translate the English text into the detected language.
- **Text-to-Speech Conversion:** Converts the translated text back into speech using gTTS (Google Text-to-Speech).
- **MongoDB Integration:** Stores user queries and chatbot responses in a MongoDB database for future reference.

**Setup:**
- Ensure you have Python installed along with necessary libraries listed in the requirements.txt file.
- Set up a MongoDB database and provide the appropriate connection details.
- Obtain credentials for the Google Cloud Translation API and set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of your credentials file.
- Install dependencies using `pip install -r requirements.txt`.
- Run the Flask application with `python app.py`.

**Endpoints:**
- `/article_query`: Accepts POST requests with JSON data containing the user's query, user ID, and chatbot ID. Responds with JSON containing the recognized text, translated text, translated text using GPT, and the audio file generated from the translated text.

**Usage:**
- Users can send queries to the chatbot by speaking into their microphone.
- The chatbot transcribes, translates, processes, and responds with the translated text in audio format.

**Contributing:**
Contributions are welcome! Feel free to open issues or pull requests for any enhancements or bug fixes.

**Credits:**
- Flask: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- Google Cloud Translation API: [cloud.google.com/translate](https://cloud.google.com/translate)
- Hugging Face Transformers: [huggingface.co/transformers](https://huggingface.co/transformers)
- gTTS: [pypi.org/project/gTTS](https://pypi.org/project/gTTS/)
- MongoDB: [mongodb.com](https://www.mongodb.com/)

