from flask import Flask, render_template
import speech_recognition as sr
import pyttsx3
import threading
import time

app = Flask(__name__)

def normalize_text(text):
    # Normalize text to lowercase
    return text.lower()

def process_command(command):
    # Process custom commands using pyttsx3
    normalized_command = normalize_text(command)

    if 'hello' in normalized_command:
        return "Hello! How can I help you?"
    
    if 'jarvis' in normalized_command:
        return 'tell me what to do for you'
    if 'what is your name' in normalized_command:
        return 'My name is Jarvis'

    # Add more custom commands here

    return "I'm sorry, I didn't understand that."

def listen_and_respond():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    with sr.Microphone() as source:
        while True:
            print("Say something...")
            audio = recognizer.listen(source, timeout=5)

            try:
                command = recognizer.recognize_google(audio)
                print(f"Recognized: {command}")

                if command.lower() == 'quit':
                    print("Terminating the listening loop.")
                    engine.say("Goodbye!")
                    engine.runAndWait()
                    break

                time.sleep(1)

                response = process_command(command)
                print(f"Response: {response}")

                engine.say(response)
                engine.runAndWait()

            except sr.UnknownValueError:
                print("Could not understand audio")

            except sr.RequestError as e:
                print(f'Recognition request failed: {str(e)}')

if __name__ == '__main__':
    if 'listening_thread' not in locals():
        listening_thread = threading.Thread(target=listen_and_respond)
        listening_thread.start()

   
    app.run(debug=True)