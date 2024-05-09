import speech_recognition as sr
from gtts import gTTS
import random
import os
import webbrowser
from time import ctime, sleep
from pydub import AudioSegment
import winsound
import spacy
import pyjokes


nlp = spacy.load("en_core_web_sm")


recognizer = sr.Recognizer()

# Function to convert text to speech
def speak(response_text):
    tts = gTTS(text=response_text, lang='en')
    random_num = random.randint(1, 1000000)
    audio_file_mp3 = 'audio-' + str(random_num) + '.mp3'
    audio_file_wav = 'audio-' + str(random_num) + '.wav'
    tts.save(audio_file_mp3)
    sound = AudioSegment.from_mp3(audio_file_mp3)
    sound.export(audio_file_wav, format="wav")
    winsound.PlaySound(audio_file_wav, winsound.SND_FILENAME)
    print(response_text)
    os.remove(audio_file_mp3)
    os.remove(audio_file_wav)

# Function to capture audio input
def record(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = recognizer.listen(source)
        voice_data = ''
        try:
            voice_data = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, my speech service is unavailable.")
        return voice_data.lower()

# Intent functions
def time():
    speak(ctime())

def search():
    search_query = record('What do you want to search for?')
    if search_query:
        url = 'https://google.com/search?q=' + search_query
        webbrowser.open(url)
        speak(f"Here are the search results for {search_query}")

def name():
    speak('My name is Jackie')

def spell_word():
    word = record("Please say a word and I will spell it for you.")
    spelled_out = ' '.join(word).upper()
    speak(f"{word} is spelled as {spelled_out}.")

def joke():
    joke = pyjokes.get_joke()
    speak(joke)

def exit_app():
    speak("Goodbye!")
    exit()

# Function to identify intents using spaCy
def detect_intent(text):
    doc = nlp(text)
    for token in doc:
        if token.lemma_ == 'time':
            return 'time'
        if token.lemma_ == 'search':
            return 'search'
        if token.lemma_ == 'name':
            return 'name'
        if token.lemma_ == 'joke':
            return 'joke'
        if token.lemma_ == 'spell':
           return 'spell'
        if token.lemma_ == 'exit':
            return 'exit'
    return None

# Function to respond based on detected intent
def respond(voice_data):
    intent = detect_intent(voice_data)
    if intent == 'time':
        time()
    elif intent == 'search':
        search()
    elif intent == 'name':
        name()
    elif intent == 'exit':
        exit_app()
    elif intent == 'joke':
        joke()
    elif intent == 'spell':
        spell_word()
    else:
        speak("Sorry, I cannot handle that request yet.")


sleep(1)
speak('How can I help you?')
while True:
    voice_input = record()
    respond(voice_input)
