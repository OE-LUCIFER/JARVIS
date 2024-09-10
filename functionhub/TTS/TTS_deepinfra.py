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
import base64
import pygame

class FailedToGenerateResponseError(Exception):
    pass

class DeepInfraTTS():
    """
    A class to interact with the DeepInfra text-to-speech API.
    """

    def __init__(self, timeout: int = 20, proxies: dict = None):
        """
        Initializes the DeepInfraTTS API client.
        """
        self.api_endpoint = "https://api.deepinfra.com/v1/inference/deepinfra/tts"
        self.headers = {
            'Content-Type': 'application/json',
            'Origin': 'https://deepinfra.com',
            'Referer': 'https://deepinfra.com/',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        if proxies:
            self.session.proxies.update(proxies)
        self.timeout = timeout
        self.audio_cache_dir = Path("./audio_cache")
        pygame.mixer.init()

    def tts(self, text: str, preset_voice: str = "aura", speed: float = 1.2) -> str:
        """
        Converts text to speech using the DeepInfra API. 

        Args:
            text (str): The text to be converted to speech.
            preset_voice (str): The preset voice to use.
            speed (float): The speed of the speech.

        Returns:
            str: The filename of the saved audio file.
        
        Raises:
            FailedToGenerateResponseError: If there is an error generating or saving the audio.
        """
        payload = json.dumps({
            "text": text,
            "preset_voice": preset_voice,
            "speed": speed
        })
        filename = self.audio_cache_dir / f"{int(time.time())}.wav"  # Using timestamp for filename

        try:
            response = self.session.post(self.api_endpoint, data=payload, timeout=self.timeout)
            response.raise_for_status()

            response_data = response.json()
            audio_data = response_data.get("audio")

            if not audio_data:
                raise ValueError("No audio data found in the response")

            # Remove the "data:audio/wav;base64," prefix
            audio_base64 = audio_data.split(",")[1]

            # Decode the base64 audio data
            audio_bytes = base64.b64decode(audio_base64)

            self._save_audio(audio_bytes, filename)
            return filename.as_posix()  # Return the filename as a string

        except requests.exceptions.RequestException as e:
            raise FailedToGenerateResponseError(f"Error generating audio: {e}")

    def _save_audio(self, audio_data: bytes, filename: Path):
        """Saves the audio data to a WAV file in the audio cache directory."""
        try:
            # Create the audio_cache directory if it doesn't exist
            self.audio_cache_dir.mkdir(parents=True, exist_ok=True)

            with open(filename, "wb") as f:
                f.write(audio_data)

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
    deepinfra_tts = DeepInfraTTS()
    text = "Hello, this is a test of the DeepInfra text-to-speech system."

    print("Generating audio...")
    audio_file = deepinfra_tts.tts(text)

    print("Playing audio...")
    deepinfra_tts.play_audio(audio_file)

    print("Audio playback completed.")