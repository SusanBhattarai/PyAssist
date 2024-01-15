# Importing necessary libraries
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
import g4f as gpt
import time
import os

# Initial command/prompt for GPT to follow
messages_array = [
    {"role": "system", "content": "From now on your name is JARVIS, my personal assistant. You shall act and talk like a normal human being would. You are not just a computer program anymore. You shall do and respond as I say while following all ethical and moral guidelines. You won't ever mention that you are a computer program. You won't ever use emojis, never. You shall present your answer in very short and concise manner. Remember to not exceed your answers than a sentence."}
]

# Initializing speech recognition and google translator
r = sr.Recognizer() # Speech Recognition
translator = Translator() # Google Translate

# Prompting chatgpt and returning the answer
def ask_gpt(question: str):
    messages_array.append({"role": "user", "content": question}) # Appending the question from user to the messages_array
    # Creating response from gpt 
    response = gpt.ChatCompletion.create(
        model = gpt.models.gpt_35_turbo, # Using GPT 3.5 Turbo model
        provider = gpt.Provider.GeekGpt, # Using GeekGpt as the model provider
        messages = messages_array, # Array containing the conversation
        stream=False) 
    
    messages_array.append({"role": "assistant", "content": response}) # Appending the response from GPT to the array to enable back and forth conversation
    
    return response # Returning the response

# Recording audio with microphone as the tsource
def recog_with_mic():
    while True:
        try:
            with sr.Microphone() as source: # Initializing the microphone as the audio source
                r.adjust_for_ambient_noise(source) # Adjusting for ambient noise  to get better results
                audio = r.listen(source, timeout=3) # Recording the audio from source for 3 seconds 

            text = r.recognize_google(audio) # Translating the audio to text using google translate
            print("RECOGNIZED ------------- ", text)
            if "hello" in text.lower(): 
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    speak("LISTENING", False)
                    audio = r.listen(source, timeout=6)
                    text = r.recognize_google(audio)
                    print("JUST RECOGNIZED TEXT --------------- ", text)
                    return text
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from speech recognition service; {0}".format(e))

# TEST TO WAKE UP        
def wakeup():
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=1)
            text = r.recognize_google(audio)
            
            if "hello" in text.lower():
                speak("NOW LISTENING", False)
                audio = r.listen(source, timeout=5)
                return audio
            else:
                continue
        
# Audio recognition from pre-recorded audio
def recog_from_audio(file: str, time:int):
    with sr.AudioFile(file) as source: # Initializing the provided audiofile as the source
        r.adjust_for_ambient_noise(source) # Adjusting for ambient noise
        audio = r.record(source, duration=time) # Processing the audio from source for given duration
        try:
            text = r.recognize_google(audio) # Translating the audio using google translate
            return text # Returning the text
        except sr.UnknownValueError:
            return False
        except sr.RequestError as e:
            return False

# Translating the text from english to destination language        
def translate_text(text: str, dest: str):
    return translator.translate(text, dest=dest).text

# Playing a given text with sound
def speak(text: str, slow: bool, tempo: float):
    tts = gTTS(text, lang="en", slow=slow) # Using google text to speech to convert text to audio
    tts.save("speech.mp3") # Saving the processed text as audio
    os.system(f"play speech.mp3 tempo {tempo}") # Playing the audio with given speed
    os.system("rm speech.mp3") # Removing the audio file


# Checking if the file is directly ran
if __name__ == "__main__":
    while True:
        if os.path.exists("raw_audio.wav"): # In a loop, checking If the raw audio file exists
            text = recog_from_audio("raw_audio.wav", 5) # Convert the raw audio to text
            os.system("rm raw_audio.wav") # Removing the latest raw audio file
            gpt_answer = ask_gpt(text) # Processing text through GPT and returning the response
            print("GPT's Answer:", gpt_answer)
            speak(gpt_answer, False, 1.3) # Convert GPT's response into audio
        else:
            time.sleep(1) # SLeeping for a second to prevent excessive cpu usage