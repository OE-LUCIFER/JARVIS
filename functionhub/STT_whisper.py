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

import pyaudio
import wave
import requests
import json
import base64
import os
import numpy as np
import time

class STT:
    def __init__(self, filename="audio_cache/recorded_audio.wav", sample_rate=44100, chunk=1024, channels=1):
        self.filename = filename
        self.sample_rate = sample_rate
        self.chunk = chunk
        self.channels = channels
        self.silence_threshold = 1000
        self.silence_limit = int(3 * sample_rate / chunk)  # 3 seconds of silence
        self.max_record_time = 60  # Maximum recording time in seconds

    def is_silent(self, data_chunk):
        return np.max(np.abs(np.frombuffer(data_chunk, dtype=np.int16))) < self.silence_threshold

    def record_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.channels,
                        rate=self.sample_rate,
                        input=True,
                        frames_per_buffer=self.chunk)

        print("🎤 Listening... Speak now! 🗣️")
        frames = []
        silent_chunks = 0
        start_time = time.time()
        last_sound_time = start_time

        while True:
            data = stream.read(self.chunk)
            frames.append(data)

            if self.is_silent(data):
                silent_chunks += 1
                if silent_chunks >= self.silence_limit:
                    print("🔇 Stopped listening due to silence. 🔇")
                    break
            else:
                silent_chunks = 0
                last_sound_time = time.time()

            if time.time() - start_time > self.max_record_time:
                print("⏰ Stopped listening due to maximum recording time reached. ⏰")
                break

        total_duration = time.time() - start_time
        actual_speech_duration = last_sound_time - start_time

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        return total_duration, actual_speech_duration

    def encode_audio(self):
        with open(self.filename, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode('utf-8')

    def transcribe_audio(self):
        url = "https://api.deepinfra.com/v1/inference/openai/whisper-large-v3"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        encoded_audio = self.encode_audio()

        payload = {
            "audio": f"data:audio/wav;base64,{encoded_audio}"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def record_and_transcribe(self):
        total_duration, speech_duration = self.record_audio()
        
        if os.path.exists(self.filename):
            print("🔍 Transcribing audio... 🔍")
            result = self.transcribe_audio()
            if result and 'text' in result:
                return {
                    "total_duration": total_duration,
                    "speech_duration": speech_duration,
                    "transcription": result['text'].strip()
                }
            else:
                return {
                    "total_duration": total_duration,
                    "speech_duration": speech_duration,
                    "error": "Transcription failed or no text was returned. 😢"
                }
        else:
            return {"error": f"File {self.filename} not found. 🚫"}

if __name__ == "__main__":
    recorder = STT()
    result = recorder.record_and_transcribe()
    print(json.dumps(result, indent=2))
    print(f"🎉 Here's your transcription: {result['transcription']} 🎉")


"""
1. **Imports and Initialization**:
   - We start by importing all the necessary libraries like `pyaudio` for recording, `wave` for saving audio, `requests` for API calls, and others for handling audio data and encoding. 📚
   - The `STT` class is our superhero, encapsulating all the magic needed to record and transcribe audio. 🦸‍♂️

2. **Class Initialization**:
   - When we create an instance of the `STT` class, it sets up default parameters like the filename for the recorded audio, sample rate, chunk size, and number of audio channels. 🎛️
   - It also sets thresholds for silence detection and maximum recording time. ⏳

3. **Silence Detection**:
   - The `is_silent` method checks if a given chunk of audio data is silent based on a predefined threshold. 🔇

4. **Recording Audio**:
   - The `record_audio` method uses the `pyaudio` library to open a stream and start recording audio. 🎤
   - It listens for audio input and appends the data to a list of frames. 📦
   - If the audio is silent for a certain duration (3 seconds by default), it stops recording. 🔇
   - The recording also stops if the maximum recording time (60 seconds by default) is reached. ⏰
   - The recorded audio is saved as a WAV file. 🎵

5. **Encoding Audio**:
   - The `encode_audio` method reads the saved WAV file and encodes it in base64 format, which is required for the API call. 🔐

6. **Transcribing Audio**:
   - The `transcribe_audio` method sends the base64-encoded audio to an external API (in this case, the DeepInfra API) to transcribe the audio into text. 🌐
   - It handles the API response and returns the transcription or an error message if something goes wrong. ⚠️

7. **Recording and Transcribing**:
   - The `record_and_transcribe` method combines the recording and transcription processes. 🎙️➡️📝
   - It records the audio, checks if the file was saved correctly, and then transcribes it. 🔍
   - It returns a dictionary containing the total duration of the recording, the duration of actual speech, and the transcription result or an error message. 📊

8. **Main Execution**:
   - When the script is run, it creates an instance of the `STT` class and calls the `record_and_transcribe` method. 🚀
   - The result is printed in a JSON format, followed by the transcription text. 🎉

"""