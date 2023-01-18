import speech_recognition as sr
from gtts import gTTS # Google Text to Speech
import os # To play the converted audio (I changed this to Mixer due to playback issues)
import openai # OpenAI's GPT-3 API
from pygame import mixer # For audio playback

# Set up the speech recognition engine
r = sr.Recognizer()

# Set up the ChatGPT model
model_engine = "text-davinci-002" # You can change this to any of the other models provided by OpenAI
openai.api_key = "" # Get your own API key from https://beta.openai.com/
trigger_phrase = "OK Nexus" # This is the phrase that will trigger the bot to start listening for user input



mixer.init() # We're using Mixer for the voice playback

# This function will send the user's input to ChatGPT and return the response
def get_response(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

# This function will listen for user input and send it to ChatGPT
def listen_for_user_input():
    while True:
        
        with sr.Microphone() as source:
                print("Listening for user input")
                audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio)
            print("You said: ", text)
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that")
            continue
        except sr.RequestError as e:
            print("Error requesting results from Google Speech Recognition service: {0}".format(e))
            break   
  

        # Send the text to ChatGPT and get its response
        response = get_response(text)

        print("GPT said: ", response)

        # Convert the response to speech
        tts = gTTS(response)

        # Save the audio file
        mixer.music.stop()
        mixer.music.unload()
        tts.save("response.mp3")
        

        # mixer.init()
        mixer.music.load('response.mp3')
        mixer.music.play()
        wait_for_it(trigger_phrase)
    

# This function will listen for the trigger phrase and start the recognition loop
def wait_for_it(trigger_phrase):
    while True:
        # Listen for the user's input
        print("Listening for trigger phrase: '" + trigger_phrase + "'")

        with sr.Microphone() as source:
            audio = r.listen(source, phrase_time_limit=5)

        # Try to recognize the speech
        try:
            text = r.recognize_google(audio)
            print("You said: ", text)
        except sr.UnknownValueError:
            # print("Sorry, I didn't understand that")
            continue
        except sr.RequestError as e:
            print("Error requesting results from Google Speech Recognition service: {0}".format(e))
            break

        if text.lower() == trigger_phrase.lower():
            print("Trigger phrase detected, starting recoghition loop")
            break
        else:
            # print("Trigger phrase not detected, listening again")
            continue
    listen_for_user_input()

wait_for_it(trigger_phrase)
