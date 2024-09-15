# utils/speech_handler.py

import speech_recognition as sr
import streamlit as st

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def capture_voice_input():
    """Captures voice input from the microphone and converts it to text."""
    with sr.Microphone() as source:
        st.write("Listening... Please speak now!")
        try:
            # Adjust for ambient noise and record audio from the source
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            # Recognize speech using Google's speech recognition
            text = recognizer.recognize_google(audio)
            st.success(f"Recognized Speech: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            st.error(f"Error with the speech recognition service: {e}")
            return None
