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

import datetime
from rich.console import Console
from typing import Optional, List
import webscout
from automation import *
from functionhub import *
from tools import TOOLS
import pygame
import random
import os

# import speech_recognition as sr  # Commented out but kept for reference

console = Console()

class JARVIS:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.proxy_manager.start()

        self.voice_ai = webscout.Julius(model="Gemini 1.5", is_conversation=False, timeout=120, proxies=self.proxy_manager.get_proxy())
        self.text_ai = webscout.Julius(model="Gemini 1.5", is_conversation=False, timeout=120, proxies=self.proxy_manager.get_proxy())
        self.agent = FunctionCallingAgent(tools=TOOLS, proxy_manager=self.proxy_manager)
        self.function_executor = FunctionExecutor(self)
        self.voicepods_tts = TTS.Voicepods()
        self.audio_recorder = STT()  # Initialize STT
        # self.recognizer = sr.Recognizer()  # Commented out but kept for reference

        pygame.mixer.init()

        self.greetings = [
            "At your service, Vortex.",
            "JARVIS online. How may I assist you today?",
            "Good to see you, Vortex. What shall we accomplish?",
            "Systems are primed and ready. What's our first task?",
            "JARVIS at your command. What's on the agenda, sir?"
        ]

        self.farewells = [
            "Powering down, Vortex. Don't hesitate to reactivate me when needed.",
            "Entering standby mode. Have a productive day, sir.",
            "JARVIS signing off. Remember, I'm always just a command away.",
            "System hibernate initiated. Until next time, Vortex.",
            "Goodbye for now. I'll be here when you need me, sir."
        ]

        self.JARVISConversation = JARVISConversation()

    def speak(self, text: str) -> None:
        console.print(f"[bold blue]JARVIS:[/] {text}")
        try:
            audio_file = self.voicepods_tts.tts(text)
            self.voicepods_tts.play_audio(audio_file)
        except Exception as e:
            console.print(f"[bold red]Voice synthesis error: {e}. Switching to text output, sir.[/]")

    def get_current_time(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")

    def process_command(self, user_input: str, input_mode: str = "voice") -> None:
        self.JARVISConversation.add_message("User", user_input)
        response = self.agent.function_call_handler(user_input)

        if "error" in response:
            error_message = f"I've encountered an error, sir. {response['error']} Shall I initiate a system diagnostic?"
            console.print(f"[bold red]{error_message}[/]")
            self.speak(error_message)
            self.JARVISConversation.add_message("JARVIS", error_message)
            return

        function_name = response.get("tool_name")
        arguments = response.get("tool_input", {})

        if hasattr(self.function_executor, f"execute_{function_name}"):
            try:
                result = getattr(self.function_executor, f"execute_{function_name}")(arguments)
                tool_result = f"User asked you: {user_input}. to answer it accurtly you called this Function: {function_name}, Result given by function: {result}"
                self.JARVISConversation.add_message("Tools", tool_result)

                ai_prompt = self.JARVISConversation.gen_complete_prompt(user_input)

                ai_response = self.voice_ai.chat(ai_prompt) if input_mode == "voice" else self.text_ai.chat(ai_prompt)

                self.JARVISConversation.add_message("JARVIS", ai_response)

                if input_mode == "voice":
                    self.speak(ai_response)
                else:
                    for c in ai_response:
                        print(c, end='', flush=True)

            except Exception as e:
                error_message = f"We've encountered an unexpected issue, sir. Error details: {e}. Shall I attempt to resolve it?"
                console.print(f"[bold red]{error_message}[/]")
                self.speak(error_message)
                self.JARVISConversation.add_message("JARVIS", error_message)
        else:
            unsupported_message = "I'm afraid that function isn't currently in my protocol, sir. Perhaps we should consider a system upgrade?"
            console.print(f"[bold red]{unsupported_message}[/]")
            self.speak(unsupported_message)
            self.JARVISConversation.add_message("JARVIS", unsupported_message)

    def run_voice_mode(self) -> None:
        greeting = random.choice(self.greetings)
        self.speak(greeting)
        self.JARVISConversation.add_message("JARVIS", greeting)
        while True:
            user_input = self.listen()
            if user_input:
                if any(phrase in user_input.lower() for phrase in ["power down", "shut down", "goodbye", "that's all"]):
                    farewell = random.choice(self.farewells)
                    self.speak(farewell)
                    self.JARVISConversation.add_message("JARVIS", farewell)
                    break
                self.process_command(user_input, input_mode="voice")
            else:
                self.speak("I'm still listening, sir. Please let me know if you need anything.")

    def run_text_mode(self) -> None:
        greeting = random.choice(self.greetings)
        console.print(f"[bold blue]JARVIS:[/] {greeting}")
        self.JARVISConversation.add_message("JARVIS", greeting)
        while True:
            user_input = input(">>> ")
            if user_input:
                if any(phrase in user_input.lower() for phrase in ["power down", "shut down", "goodbye", "that's all"]):
                    farewell = random.choice(self.farewells)
                    print(farewell)
                    self.JARVISConversation.add_message("JARVIS", farewell)
                    break
                self.process_command(user_input, input_mode="text")
                print()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def initialize(self):
        self.clear_screen()
        console.print("[bold cyan]Initializing JARVIS...[/]")
        console.print("[bold cyan]Running system checks...[/]")
        console.print("[bold green]All systems online.[/]")
        console.print("[bold cyan]JARVIS is ready for activation.[/]")

    def listen(self):
        console.print("[bold yellow]Listening... Speak now, sir.[/]")
        result = self.audio_recorder.record_and_transcribe()
        if "transcription" in result:
            user_input = result["transcription"]
            console.print(f"[bold green]Vortex:[/] {user_input}")
            return user_input
        else:
            console.print("[bold red]My apologies, Vortex. I couldn't quite catch that. Could you please repeat?[/]")
            return None

        # Commented out speech_recognition code
        # with sr.Microphone() as source:
        #     self.recognizer.adjust_for_ambient_noise(source)
        #     try:
        #         audio = self.recognizer.listen(source, timeout=5)
        #         user_input = self.recognizer.recognize_google(audio)
        #         console.print(f"[bold green]Vortex:[/] {user_input}")
        #         return user_input
        #     except sr.WaitTimeoutError:
        #         console.print("[bold yellow]No speech detected. JARVIS is still on standby, sir.[/]")
        #         return None
        #     except sr.UnknownValueError:
        #         console.print("[bold red]My apologies, Vortex. Could you please repeat that?[/]")
        #         return None
        #     except sr.RequestError as e:
        #         console.print(f"[bold red]Network issue detected, sir. Error: {e}[/]")
        #         return None

if __name__ == "__main__":
    jarvis = JARVIS()
    jarvis.initialize()

    mode = input("Choose interaction mode (voice/text): ").strip().lower()
    jarvis.clear_screen()

    if mode == "voice":
        jarvis.run_voice_mode()
    elif mode == "text":
        jarvis.run_text_mode()
    else:
        print("Invalid mode detected. Defaulting to text mode, sir.")
        jarvis.run_text_mode()