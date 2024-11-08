import streamlit as st
from nova_sdk import NovaClient, Message, TextToSpeech
import tempfile
from st_audiorec import st_audiorec
from PIL import Image

# Initialize the NovaSDK
nova = NovaClient(team_id="your_team_id", server_url="server_url")

st.title("Nova SDK Demo App")
st.write("This app demonstrates the Nova SDK's ability to handle text, images, and audio inputs.")

# Select Input Modality
input_modality = st.selectbox("Select Input Modality", ["Text", "Image", "Audio", "Text + Image", "Text + Audio"])

# Input fields based on modality
text_input = None
image_input = None
audio_file_input = None
recorded_audio_path = None

# Text Input
if input_modality in ["Text", "Text + Image", "Text + Audio"]:
    text_input = st.text_area("Enter text input")

# Image Input
if input_modality in ["Image", "Text + Image"]:
    image_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if image_file:
        image_input = Image.open(image_file)
        st.image(image_input, caption="Uploaded Image", use_column_width=True)

# Audio Input or Recording
if input_modality in ["Audio", "Text + Audio"]:
    st.write("Choose to upload or record audio input:")

    # Audio file upload
    audio_file_input = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])

    # Audio recording
    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file_input:
            temp_audio_file_input.write(wav_audio_data)
            audio_input_path = temp_audio_file_input.name

# Output Modality Selection
output_modality = st.selectbox("Select Output Modality", ["Text", "Image", "Audio"])

stream = st.toggle("Stream text response?")

# Process Input and Display Output
if st.button("Process"):
    audio_input_path = recorded_audio_path or (audio_file_input.name if audio_file_input else None)
    message = Message(
        text=text_input, 
        images=[image_input] if image_input else [], 
        audio=[audio_input_path] if audio_input_path else []
    )

    try:
        # Call Nova SDK process_message
        response = nova.process_message(message, output_modality=output_modality)
        
        if output_modality == "Text":
            st.write("Response Text:")
            if stream:
                for chunk in response:
                    st.write(response)
            else:
                st.write(response)
        
        elif output_modality == "Image":
            st.write("Response Image:")
            st.image(response, use_column_width=True)
        
        elif output_modality == "Audio":
            st.write("Response Audio:")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_response:
                temp_audio_response.write(response)
                st.audio(temp_audio_response.name, format="audio/wav")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Text-to-Speech Feature
st.header("Text-to-Speech Feature")
tts_text = st.text_input("Enter text for Text-to-Speech")
tts_provider = st.selectbox("Select TTS Provider", ["cartesia", "hume"])

if st.button("Generate Speech"):
    tts = TextToSpeech(nova, provider=tts_provider)
    try:
        tts_audio = tts.synthesize(tts_text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_tts_audio:
            temp_tts_audio.write(tts_audio)
            st.audio(temp_tts_audio.name, format="audio/wav")
    except Exception as e:
        st.error(f"Error: {e}")
