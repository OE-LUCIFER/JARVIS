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

import re
import requests
from uuid import uuid4
import json

class Felo:
    def __init__(
        self,
        timeout: int = 30,
        proxies: dict = {},
        history_offset: int = 10250,
    ):
        self.session = requests.Session()
        self.chat_endpoint = "https://api.felo.ai/search/threads"
        self.timeout = timeout
        self.last_response = {}
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "content-type": "application/json",
        }
        self.session.headers.update(self.headers)
        self.history_offset = history_offset
        self.session.proxies = proxies

    def ask(self, prompt: str, stream: bool = False, raw: bool = False) -> dict:
        payload = {
            "query": prompt,
            "search_uuid": uuid4().hex,
            "search_options": {"langcode": "en-US"},
            "search_video": True,
        }

        def for_stream():
            response = self.session.post(
                self.chat_endpoint, json=payload, stream=True, timeout=self.timeout
            )
            streaming_text = ""
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith('data:'):
                    try:
                        data = json.loads(line[5:].strip())
                        if 'text' in data['data']:
                            new_text = data['data']['text']
                            delta = new_text[len(streaming_text):]
                            streaming_text = new_text
                            self.last_response.update(dict(text=streaming_text))
                            yield line if raw else dict(text=delta)
                    except json.JSONDecodeError:
                        pass

        def for_non_stream():
            return ''.join([chunk['text'] for chunk in for_stream()])

        return for_stream() if stream else for_non_stream()

    def chat(self, prompt: str, stream: bool = False) -> str:
        return self.ask(prompt, stream)

    def get_message(self, response: dict) -> str:
        return re.sub(r'\[\[\d+\]\]', '', response.get("text", ""))

if __name__ == '__main__':
    from rich import print
    ai = Felo()
    response = ai.chat(input(">>> "))
    if isinstance(response, str):
        print(response)
    else:
        for chunk in response:
            print(chunk, end="", flush=True)

"""

1. **Imports and Initialization**:
   - We start by importing all the necessary libraries like `re` for regular expressions, `requests` for API calls, `uuid` for generating unique IDs, and `json` for handling JSON data. 📚
   - The `Felo` class is our superhero, encapsulating all the magic needed to interact with the Felo AI chat API. 🦸‍♂️

2. **Class Initialization**:
   - When we create an instance of the `Felo` class, it sets up the session, API endpoint, headers, and other configurations like timeout and proxies. 🎛️
   - It also initializes the history offset and sets up the session headers and proxies. 🌐

3. **Asking Questions**:
   - The `ask` method sends a prompt to the Felo AI API and handles both streaming and non-streaming responses. 🗣️
   - It constructs the payload with the prompt and other necessary details. 📦
   - If streaming is enabled, it processes the response line by line, updating the streaming text and yielding each chunk. 📤
   - If streaming is disabled, it collects all chunks and returns the complete response as a string. 📥

4. **Chatting with AI**:
   - The `chat` method is a wrapper around the `ask` method, making it easier to start a chat. 💬
   - It simply calls the `ask` method with the provided prompt and streaming option. 🚀

5. **Cleaning Up Responses**:
   - The `get_message` method cleans up the response text by removing any unwanted tags or markers. 🧹
   - It uses a regular expression to remove patterns like `[[number]]` from the text. 🔍

6. **Example Usage**:
   - When the script is run, it creates an instance of the `Felo` class and starts a chat with the AI. 🚀
   - It takes user input, sends it to the AI, and prints the response either as a complete string or as streaming chunks. 🎉

"""