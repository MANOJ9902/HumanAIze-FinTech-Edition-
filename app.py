from flask import Flask, render_template, request, jsonify
import openai
import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from qdrant_client import QdrantClient
import logging

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = ''

# Initialize the model and client for Qdrant
model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

url = "http://localhost:6333"
client = QdrantClient(
    url=url, prefer_grpc=False
)

db = Qdrant(client=client, embeddings=embeddings, collection_name="vector_db")

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

    def voice_to_text(self):
        with sr.Microphone() as source:
            logging.info("Listening...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                logging.info(f"Recognized text: {text}")
                return text
            except sr.UnknownValueError:
                logging.error("Google Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None

    def text_to_speech(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def translate_text(self, text, target_language):
        translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translated_text

voice_assistant = VoiceAssistant()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Function to call GPT-4 for text completion
def gpt4_completion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200  # Increase tokens for more detailed responses
    )
    return response['choices'][0]['message']['content']

# Function to perform RAG with Qdrant and refine with GPT-4
def rag_gpt_integration(query):
    # Perform RAG with Qdrant for retrieval
    docs = db.similarity_search_with_score(query=query, k=5)
    documents = [{"text": doc.page_content, "score": score} for doc, score in docs]

    # Generate initial response using RAG
    initial_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Retrieve documents related to: {query}"},
            {"role": "user", "content": query, "documents": documents}
        ],
        max_tokens=200  # Increase tokens for more detailed responses
    )

    # Refine using GPT-4 based on the combined context
    refined_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": initial_response['choices'][0]['message']['content']},
            {"role": "user", "content": query}
        ],
        max_tokens=200  # Increase tokens for more detailed responses
    )

    return refined_response['choices'][0]['message']['content']

@app.route('/search', methods=['POST'])
def search():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.json
    query = data.get('query')
    target_lang = data.get('lang', 'en')  # Default to English if lang parameter is not provided
    integrated_response = rag_gpt_integration(query)
    if target_lang != 'en':
        integrated_response = voice_assistant.translate_text(integrated_response, target_lang)
    return jsonify({"response": integrated_response})

@app.route('/voice', methods=['POST'])
def voice():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415

    data = request.json
    text = voice_assistant.voice_to_text()
    if text:
        target_lang = data.get('lang', 'en')  # Default to English if lang parameter is not provided
        integrated_response = rag_gpt_integration(text)
        if target_lang != 'en':
            integrated_response = voice_assistant.translate_text(integrated_response, target_lang)
        voice_assistant.text_to_speech(integrated_response)
        return jsonify({"response": integrated_response})
    else:
        return jsonify({"response": "Could not understand audio."})

if __name__ == '__main__':
    app.run(debug=True)
