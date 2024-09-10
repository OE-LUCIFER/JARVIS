import os
import platform
import webbrowser
from typing import Dict, Any
import requests
import webscout
from pywhatkit import playonyt
from AppOpener import close, open as appopen
import keyboard 

class FunctionExecutor:
    def __init__(self, jarvis_instance):
        self.jarvis = jarvis_instance


    def execute_web_search(self, arguments: Dict[str, Any]) -> str:
        """
        Executes a web search using a specialized API and returns formatted search results.
        Falls back to an older method if the new API times out or fails.
        """
        query = arguments.get("query")
        if query:
            try:
                api_url = "https://oevortex-webscout-api.hf.space/api/adv_web_search"
                params = {
                    "q": query,
                    "model": "llama3-8b",
                    "max_results": 5,
                    "safesearch": "off",
                    "region": "wt-wt",
                    "backend": "lite",
                    "max_chars": 6000,
                    "system_prompt": """You are a highly knowledgeable and informative AI chatbot. Your primary goal is to provide the most accurate and detailed answer to the user's query based on information retrieved from Google Search results."""
                }

                response = requests.get(api_url, params=params, timeout=10)
                response.raise_for_status() 

                data = response.json()
                return data["response"]

            except requests.exceptions.RequestException as e:

                try:
                    with webscout.WEBS() as webs:
                        search_results = webs.text(query, max_results=5)

                    formatted_results = "\n\n".join(
                        f"{i+1}. [{result['title']}]({result['href']})\n{result['body']}"
                        for i, result in enumerate(search_results)
                    )
                    return formatted_results

                except Exception as fallback_error:
                    return f"Error during fallback web search: {fallback_error}"

        else:
            return "Please provide a search query."

    def open_app(self, app_name):
        """Opens a specified application."""
        try:
            appopen(app_name, match_closest=True, output=True, throw_error=True)
            return True
        except Exception:
            return False

    def close_app(self, app_name):
        """Closes a specified application."""
        try:
            close(app_name, match_closest=True, output=True, throw_error=True)
            return True
        except Exception:
            return False

    def play_youtube(self, query):
        """Plays a YouTube video."""
        playonyt(query)
        return True


    def execute_open_app(self, arguments: Dict[str, Any]) -> str:
        app_name = arguments.get("app_name")
        if app_name:
            if self.open_app(app_name):
                return f"Opening {app_name}."
            else:
                return f"Failed to open {app_name}."
        else:
            return "Please provide an application name."

    def execute_close_app(self, arguments: Dict[str, Any]) -> str:
        app_name = arguments.get("app_name")
        if app_name:
            if self.close_app(app_name): 
                return f"Closing {app_name}."
            else:
                return f"Failed to close {app_name}."
        else:
            return "Please provide an application name."

    def execute_play_youtube(self, arguments: Dict[str, Any]) -> str:
        query = arguments.get("query")
        if query:
            if self.play_youtube(query):
                return f"Playing YouTube video: {query}."
            else:
                return f"Failed to play YouTube video: {query}."
        else:
            return "Please provide a YouTube search query."


    def execute_system_control(self, arguments: Dict[str, Any]) -> str:
        command = arguments.get("command")
        if command:
            system_controls = {
                'mute': lambda: keyboard.press_and_release('volume mute'),
                'unmute': lambda: keyboard.press_and_release('volume mute'),
                'volume up': lambda: keyboard.press_and_release('volume up'),
                'volume down': lambda: keyboard.press_and_release('volume down'),
                'minimize all': lambda: keyboard.press_and_release('win+d'),
                'shutdown': lambda: os.system('shutdown /s /t 1' if platform.system() == 'Windows' else 'poweroff')
            }

            if command in system_controls:
                try:
                    system_controls[command]()
                    return f"Executing system command: {command}"
                except Exception as e:
                    return f"Error executing system command: {e}"
            else:
                return f"Invalid system command: {command}"
        else:
            return "Please provide a system control command."

    def execute_open_website(self, arguments: Dict[str, Any]) -> str:
        """Opens a website in the default browser and returns a confirmation message."""
        url = arguments.get("url")
        if url:
            webbrowser.open(url)
            return f"Opening {url}"
        else:
            return "Please provide a website URL."


    def execute_general_ai(self, arguments: Dict[str, Any]) -> str:
        """Returns the question to be answered by the AI."""
        question = arguments.get("question")
        if question:
            return None

    