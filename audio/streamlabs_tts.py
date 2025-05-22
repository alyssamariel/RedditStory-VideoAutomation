import requests
from requests.exceptions import JSONDecodeError
from pathlib import Path

def streamlabs_tts(text: str, voice: str, output_file):
    url = "https://streamlabs.com/polly/speak"

    payload = {
        "text": text,
        "voice": voice,
        "service": "polly"
    }

    headers = {
        "Referer": "https://streamlabs.com/"
    }

    response = requests.post(url, headers=headers, data=payload)

    try:
        voice_data = requests.get(response.json()["speak_url"])
        with open(output_file, "wb") as f:
            f.write(voice_data.content)

    except (KeyError, JSONDecodeError):
        try:
            if response.json()["error"] == "No text specified!":
                raise ValueError("Please specify a text to convert to speech.")
        except (KeyError, JSONDecodeError):
            print("Error occurred calling Streamlabs Polly")