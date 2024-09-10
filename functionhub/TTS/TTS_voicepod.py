"""
🌟 Subscribe to OEvortex (https://youtube.com/@OEvortex) 🌟
Made with ❤️ by Vortex
Telegram Channel: https://t.me/vortexcodebase
Discord: https://discord.gg/YweJwNqrnH

Follow me on:
GitHub: https://github.com/OE-LUCIFER
HuggingFace: https://huggingface.co/OEvortex
Instagram: https://www.instagram.com/oevortex/
"""

import requests
import json
import time
from pathlib import Path
from typing import Generator
import pygame

class FailedToGenerateResponseError(Exception):
    pass

class Voicepods():
    """
    A class to interact with the Voicepods text-to-speech API.
    """

    def __init__(self, timeout: int = 20, proxies: dict = None):
        """
        Initializes the Voicepods API client.
        """
        self.api_endpoint = "https://voicepods-stream.vercel.app/api/resemble"
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
            'Content-Type': 'application/json',
            'DNT': '1',
            'Origin': 'https://voicepods-stream.vercel.app',
            'Referer': 'https://voicepods-stream.vercel.app/',
            'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        if proxies:
            self.session.proxies.update(proxies)
        self.timeout = timeout
        self.audio_cache_dir = Path("./audio_cache")
        pygame.mixer.init()

    def tts(self, text: str) -> str:
        """
        Converts text to speech using the Voicepods API. 

        Args:
            text (str): The text to be converted to speech.

        Returns:
            str: The filename of the saved audio file.
        
        Raises:
            FailedToGenerateResponseError: If there is an error generating or saving the audio.
        """
        payload = json.dumps({"query": text})
        filename = self.audio_cache_dir / f"{int(time.time())}.wav"  # Using timestamp for filename

        try:
            response = self.session.post(self.api_endpoint, data=payload, timeout=self.timeout)
            response.raise_for_status()

            content_type = response.headers.get('Content-Type', '')
            if 'audio' not in content_type.lower():
                raise ValueError(f"Unexpected content type: {content_type}")

            audio_data = response.content
            self._save_audio(audio_data, filename)
            return filename.as_posix()  # Return the filename as a string

        except requests.exceptions.RequestException as e:
            raise FailedToGenerateResponseError(f"Error generating audio: {e}")

    def _save_audio(self, audio_data: bytes, filename: Path):
        """Saves the audio data to a WAV file in the audio cache directory."""
        try:
            # Create the audio_cache directory if it doesn't exist
            self.audio_cache_dir.mkdir(parents=True, exist_ok=True)

            riff_start = audio_data.find(b'RIFF')
            if riff_start == -1:
                raise ValueError("RIFF header not found in audio data")
            
            trimmed_audio_data = audio_data[riff_start:]

            with open(filename, "wb") as f:
                f.write(trimmed_audio_data)

        except Exception as e:
            raise FailedToGenerateResponseError(f"Error saving audio: {e}")

    def play_audio(self, filename: str):
        """
        Plays an audio file using pygame.

        Args:
            filename (str): The path to the audio file.

        Raises:
            RuntimeError: If there is an error playing the audio.
        """
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            raise RuntimeError(f"Error playing audio: {e}")

# Example usage
if __name__ == "__main__":
    voicepods = Voicepods()
    text = "Hello, this is a test of the Voicepods text-to-speech system."

    print("Generating audio...")
    audio_file = voicepods.tts(text)

    print(f"Audio generated: {audio_file}")
    print("Playing audio...")
    voicepods.play_audio(audio_file)

    print("Audio playback completed.")
"""
1. **Imports and Initialization**:
   - We start by importing all the necessary libraries like `requests` for API calls, `json` for handling JSON data, `time` for timestamps, `Path` for file paths, and `pygame` for playing audio. 📚
   - The `Voicepods` class is our superhero, encapsulating all the magic needed to convert text to speech and play it. 🦸‍♂️

2. **Class Initialization**:
   - When we create an instance of the `Voicepods` class, it sets up the API endpoint, headers, and session for making requests. 🎛️
   - It also initializes the audio cache directory and pygame mixer for playing audio. 🎵

3. **Text to Speech Conversion**:
   - The `tts` method converts text to speech using the Voicepods API. 🗣️
   - It sends the text as a JSON payload to the API and saves the returned audio data as a WAV file. 📦
   - If there's an error during the request or saving the audio, it raises a `FailedToGenerateResponseError`. ⚠️

4. **Saving Audio**:
   - The `_save_audio` method saves the audio data to a WAV file in the audio cache directory. 💾
   - It ensures the audio data starts with the RIFF header and creates the cache directory if it doesn't exist. 📂

5. **Playing Audio**:
   - The `play_audio` method plays the saved audio file using pygame. 🎧
   - It loads the audio file and plays it, waiting until playback is complete. ⏳

6. **Example Usage**:
   - When the script is run, it creates an instance of the `Voicepods` class and converts a sample text to speech. 🚀
   - It then plays the generated audio file and prints messages to indicate the process. 🎉
"""