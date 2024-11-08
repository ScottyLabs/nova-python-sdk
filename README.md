# Nova Python SDK

The Nova Python SDK is a Python client library for use in the NOVA hackathon hosted by ScottyLabs. It allows users to create messages containing text, images, and audio and process them for various generative models that support output modalities like text, images, or audio.

## Installation

```bash
pip install nova-client-sdk
```

## Basic Usage

```python
# import nova_sdk
from nova_sdk import NovaClient, Message, TextToSpeech

# Initialize the NovaClient with a team ID and server url
nova = NovaClient(team_id='your_team_id', server_url="[SERVER_URL]")

# Create a message with text and an image
message = Message(
    text="Describe this image.",
    images=['path/to/image.jpg']
)

# Process the message to get text output
response = nova.process_message(message, output_modality='text')
print(response)

# Use TextToSpeech
tts = TextToSpeech(nova, provider='hume')
audio_content = tts.synthesize("Hello, this is a test.")
with open('output_audio.wav', 'wb') as f:
    f.write(audio_content)
```
