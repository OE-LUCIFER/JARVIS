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
import time
import threading
import schedule
import json
from typing import Dict, Any, List
import pygame
import io
import os
from .TTS import Voicepods


pygame.mixer.init()

DATA_FOLDER = "DATA"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

ALARM_FILE = os.path.join(DATA_FOLDER, "alarms.json")
SCHEDULE_FILE = os.path.join(DATA_FOLDER, "schedules.json")

class AlarmManager:
    def __init__(self):
        self.alarms = self.load_alarms()
        self.schedules = self.load_schedules()
        self.thread = None
        self.running = False
        self.voicepods_tts = Voicepods()

    def load_alarms(self):
        if os.path.exists(ALARM_FILE):
            with open(ALARM_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("Error decoding alarms.json. Starting with an empty list.")
                    return []
        return []

    def save_alarms(self):
        with open(ALARM_FILE, "w") as f:
            json.dump(self.alarms, f, indent=2)

    def load_schedules(self):
        if os.path.exists(SCHEDULE_FILE):
            with open(SCHEDULE_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print("Error decoding schedules.json. Starting with an empty dictionary.")
                    return {}
        return {}

    def save_schedules(self):
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(self.schedules, f, indent=2)

    def add_alarm(self, time_str: str, message: str):
        alarm_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        self.alarms.append({"time": alarm_time.isoformat(), "message": message})
        self.alarms.sort(key=lambda x: datetime.datetime.fromisoformat(x["time"]))
        self.save_alarms()

    def add_schedule(self, name: str, time_str: str, message: str, repeat: str = "daily"):
        schedule.every().day.at(time_str).do(self.trigger_schedule, name, message).tag(name)
        self.schedules[name] = {"time": time_str, "message": message, "repeat": repeat}
        self.save_schedules()

    def remove_schedule(self, name: str):
        if name in self.schedules:
            schedule.clear(name)
            del self.schedules[name]
            self.save_schedules()

    def trigger_schedule(self, name: str, message: str):
        self.play_notification_sound(message)
        print(f"Schedule '{name}' triggered: {message}")

    def check_alarms(self):
        now = datetime.datetime.now()
        triggered_alarms = [alarm for alarm in self.alarms if datetime.datetime.fromisoformat(alarm["time"]) <= now]
        for alarm in triggered_alarms:
            self.play_notification_sound(alarm["message"])
            print(f"Alarm triggered: {alarm['message']}")
            self.alarms.remove(alarm)
        self.save_alarms()

    def play_notification_sound(self, message: str):
        try:
            audio_file = self.voicepods_tts.tts(message)
            self.voicepods_tts.play_audio(audio_file)
        except Exception as e:
            print(f"Error playing notification sound: {e}")

    def run(self):
        self.running = True
        while self.running:
            schedule.run_pending()
            self.check_alarms()
            time.sleep(1)

    def start(self):
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

# Example usage
if __name__ == "__main__":
    alarm_manager = AlarmManager()
    alarm_manager.add_alarm("2024-9-09 12:20:00", "Time to wake up!")
    alarm_manager.add_schedule("Lunch Reminder", "12:41", "It's lunchtime!")
    alarm_manager.start()

"""

1. **Imports and Initialization**:
   - We start by importing all the necessary libraries like `datetime` for time handling, `time` for sleep, `threading` for background tasks, `schedule` for scheduling, `json` for handling JSON data, `pygame` for playing audio, `io` for handling byte streams, and `os` for file operations. 📚
   - We also import the `Voicepods` class from the `TTS` module, which handles text-to-speech conversion and audio playback. 🎤

2. **Class Initialization**:
   - When we create an instance of the `AlarmManager` class, it loads existing alarms and schedules from JSON files, initializes a thread for running the manager, and sets up the `Voicepods` TTS (Text-to-Speech) for generating audio notifications. 🎛️

3. **Loading and Saving Data**:
   - The `load_alarms` and `load_schedules` methods load alarms and schedules from JSON files, handling any decoding errors gracefully. 📂
   - The `save_alarms` and `save_schedules` methods save the current state of alarms and schedules back to their respective JSON files. 💾

4. **Adding and Removing Alarms and Schedules**:
   - The `add_alarm` method adds a new alarm by parsing a time string and saving it to the alarms list. ⏰
   - The `add_schedule` method adds a new schedule by parsing a time string and setting up a daily schedule using the `schedule` library. 📅
   - The `remove_schedule` method removes a schedule by name, clearing it from the `schedule` library and the schedules dictionary. 🗑️

5. **Triggering Schedules and Checking Alarms**:
   - The `trigger_schedule` method plays a notification sound and prints a message when a schedule is triggered. 🔔
   - The `check_alarms` method checks if any alarms should be triggered based on the current time, plays a notification sound for each triggered alarm, and removes them from the list. ⏲️

6. **Playing Notification Sounds**:
   - The `play_notification_sound` method uses the `Voicepods` TTS to generate audio from a message and plays it using `pygame`. 🎧

7. **Running the Manager**:
   - The `run` method continuously checks for pending schedules and alarms, running them if necessary, and sleeps for a second between checks. 🔄
   - The `start` method starts the manager in a new thread if it's not already running. 🚀
   - The `stop` method stops the manager by setting the running flag to `False` and joining the thread. ⏹️

"""