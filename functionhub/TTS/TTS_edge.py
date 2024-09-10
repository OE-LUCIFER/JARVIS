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
import time
import pathlib
import edge_tts
import pygame
import asyncio

class EdgeTTS:
    """
    Text-to-speech provider using the Edge TTS API.
    """

    cache_dir = pathlib.Path("./audio_cache")

    def __init__(self, timeout: int = 20):
        """Initializes the Edge TTS client."""
        self.timeout = timeout
        pygame.mixer.init()

    def tts(self, text: str, voice: str = "en-US-AriaNeural") -> str:
        """
        Converts text to speech using the Edge TTS API and saves it to a file.
        """
        filename = self.cache_dir / f"{int(time.time())}.mp3"

        try:
            # Create the audio_cache directory if it doesn't exist
            self.cache_dir.mkdir(parents=True, exist_ok=True)

            # Generate speech
            asyncio.run(self._save_audio(text, voice, filename))

            return str(filename.resolve())

        except Exception as e:
            raise RuntimeError(f"Failed to perform the operation: {e}")

    async def _save_audio(self, text: str, voice: str, filename: pathlib.Path):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

    def play_audio(self, filename: str):
        """
        Plays an audio file using pygame.

        Args:
            filename (str): The path to the audio file.
        """
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            raise RuntimeError(f"Error playing audio: {e}")

    @property
    def all_voices(self) -> dict[str, list[str]]:
        """Returns a dictionary of all available voices."""
        return {
            "English": [
                "en-US-AriaNeural",
                "en-US-GuyNeural",
                "en-US-JennyNeural",
                "en-US-ChristopherNeural",
                "en-US-EricNeural",
                "en-US-MichelleNeural",
                "en-US-RogerNeural",
                "en-US-SteffanNeural",
                "en-GB-SoniaNeural",
                "en-GB-RyanNeural",
                "en-AU-NatashaNeural",
                "en-AU-WilliamNeural",
                "en-CA-ClaraNeural",
                "en-CA-LiamNeural",
                "en-IN-NeerjaNeural",
                "en-IN-PrabhatNeural",
            ],
            "Hindi": [
                "hi-IN-SwaraNeural",
                "hi-IN-MadhurNeural"
            ]
        }

# Example usage
if __name__ == "__main__":
    tts_engine = EdgeTTS()
    
    # English TTS
    print("Generating English audio...")
    english_text = "This is a test of the Edge TTS system in English."
    english_audio = tts_engine.tts(english_text, voice="en-US-AriaNeural")
    print(f"English audio generated: {english_audio}")
    print("Playing English audio...")
    tts_engine.play_audio(english_audio)

    # Hindi TTS
    print("\nGenerating Hindi audio...")
    hindi_text = "नमस्ते, यह हिंदी में Edge TTS सिस्टम का एक परीक्षण है।"
    hindi_audio = tts_engine.tts(hindi_text, voice="hi-IN-SwaraNeural")
    print(f"Hindi audio generated: {hindi_audio}")
    print("Playing Hindi audio...")
    tts_engine.play_audio(hindi_audio)

    # # Print all available voices
    # print("\nAvailable voices:")
    # for language, voices in tts_engine.all_voices.items():
    #     print(f"\n{language}:")
    #     for voice in voices:
    #         print(f"  - {voice}")