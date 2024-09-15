# Ensure that tempfile is imported
import tempfile
from gtts import gTTS
import streamlit as st

def generate_audio(answer, language='en'):
    try:
        # Use gTTS to generate the MP3 file
        tts = gTTS(answer, lang=language[:2].lower())
        
        # Create a temporary MP3 file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save('answer_final.mp3')  # Save the TTS output to the file
        
        # Store the file path in session state
        st.session_state.generated_audio_file = 'answer_final.mp3'
        st.success("Audio generated successfully.")

        return 'answer_final.mp3'
        
    except Exception as e:
        st.error(f"Error generating audio: {e}")
