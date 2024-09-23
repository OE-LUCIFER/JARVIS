import json
import os
import platform
import re
import subprocess
import sys
import webbrowser


from typing import Dict, Any
import requests
import webscout
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import datetime
import pyautogui
import speedtest
import PyPDF2
from webscout import PhindSearch as a

from functionhub import AlarmManager, Felo
from pywhatkit import search, playonyt
from AppOpener import close, open as appopen
import keyboard

from .autocoder import AutoCoder

class FunctionExecutor:
    def __init__(self, jarvis_instance):
        self.jarvis = jarvis_instance
        self.alarm_manager = AlarmManager()
        self.alarm_manager.start()
        self.autocoder = AutoCoder()  # Initialize the AutoCoder instance

    # def execute_web_search(self, arguments: Dict[str, Any]) -> str:
    #     """
    #     Executes a web search using a specialized API and returns formatted search results.
    #     Also uses the fallback method and combines results from both.
    #     """
    #     query = arguments.get("query")
    #     if not query:
    #         return "Please provide a search query."

    #     api_url = "https://oevortex-webscout-api.hf.space/api/adv_web_search"
    #     params = {
    #         "q": query,
    #         "model": "gpt-4o-mini",
    #         "max_results": 5,
    #         "safesearch": "off",
    #         "region": "wt-wt",
    #         "backend": "lite",
    #         "max_chars": 300,
    #         "system_prompt": """You are a highly knowledgeable and informative AI chatbot. Your primary goal is to provide the most accurate and detailed answer to the user's query based on information retrieved from Google Search results."""
    #     }

    #     results = []

    #     # Try the new API (DEEP SEARCH)
    #     try:
    #         response = requests.get(api_url, params=params, timeout=20)
    #         response.raise_for_status()
    #         data = response.json()
    #         results.append(f"DEEP WEBSEARCH:\n{data['response']}")
    #     except requests.exceptions.RequestException as e:
    #         results.append(f"Error with DEEP SEARCH: {e}")

    #     # Use the fallback method (Normal search)
    #     try:
    #         with webscout.WEBS() as webs:
    #             search_results = webs.text(query, max_results=5)

    #         formatted_results = "\n\n".join(
    #             f"{i+1}. [{result['title']}]({result['href']})\n{result['body']}"
    #             for i, result in enumerate(search_results)
    #         )
    #         results.append(f"Normal websearch:\n{formatted_results}")
    #     except Exception as fallback_error:
    #         results.append(f"Error during Normal search: {fallback_error}")
    #     # Combine all results
    #     return "\n\n".join(results)
    def execute_web_search(self, arguments: Dict[str, Any]) -> str:
        """
        Executes a web search using webscout and returns formatted search results.
        """
        query = arguments.get("query")
        if not query:
            return "Please provide a search query."

        try:
            with webscout.WEBS() as webs:
                search_results = webs.text(query, max_results=5)

            formatted_results = "\n\n".join(
                f"{i+1}. [{result['title']}]({result['href']})\n{result['body']}"
                for i, result in enumerate(search_results)
            )
            return f"Web search results:\n{formatted_results}"
        except Exception as error:
            return f"Error during web search: {error}"

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


    # def execute_system_control(self, arguments: Dict[str, Any]) -> str:
    #     command = arguments.get("command")
    #     if command:
    #         system_controls = {
    #             'mute': lambda: keyboard.press_and_release('volume mute'),
    #             'unmute': lambda: keyboard.press_and_release('volume mute'),
    #             'volume up': lambda: keyboard.press_and_release('volume up'),
    #             'volume down': lambda: keyboard.press_and_release('volume down'),
    #             'minimize all': lambda: keyboard.press_and_release('win+d'),
    #             'shutdown': lambda: os.system('shutdown /s /t 1' if platform.system() == 'Windows' else 'poweroff')
    #         }

    #         if command in system_controls:
    #             try:
    #                 system_controls[command]()
    #                 return f"Executing system command: {command}"
    #             except Exception as e:
    #                 return f"Error executing system command: {e}"
    #         else:
    #             return f"Invalid system command: {command}"
    #     else:
    #         return "Please provide a system control command."

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



    def execute_get_weather(self, arguments: Dict[str, Any]) -> str:
        """Gets the current weather for a given location and returns a string."""
        location = arguments.get("location")
        if location:
            weather_data = webscout.weather.get(location)
            if isinstance(weather_data, dict):
                current_condition = weather_data.get("current_condition", [])
                if current_condition:
                    current_weather = current_condition[0]  # Assuming only one current condition
                    description = current_weather.get("weatherDesc", [{}])[0].get("value", "Unknown")
                    temperature = current_weather.get("temp_C", "Unknown")
                    feels_like = current_weather.get("FeelsLikeC", "Unknown")
                    humidity = current_weather.get("humidity", "Unknown")
                    wind_speed = current_weather.get("windspeedKmph", "Unknown")
                    return (
                        f"The current weather in {location} is {description}. "
                        f"The temperature is {temperature} degrees Celsius, "
                        f"and it feels like {feels_like} degrees. "
                        f"Humidity is {humidity}%, and the wind speed is {wind_speed} kmph."
                    )
                else:
                    return f"I couldn't find current weather information for {location}. Please check the location and try again."
            else:
                return f"I couldn't get the weather for {location}. Please check the location and try again."
        else:
            return "Please provide a location." 

    def execute_send_email(self, arguments: Dict[str, Any]) -> str:
        """Sends an email and returns a confirmation message."""
        to_email = arguments.get("to_email")
        subject = arguments.get("subject")
        body = arguments.get("body")
        if to_email and subject and body:
            try:
                # Replace these with your actual email credentials
                sender_email = "your_email@gmail.com"
                sender_password = "your_password"

                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = to_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, sender_password)
                    server.send_message(message)

                return "Email sent successfully."
            except Exception as e:
                return f"Failed to send email: {e}"
        else:
            return "Please provide recipient email, subject, and body."

    def execute_set_alarm(self, arguments: Dict[str, Any]) -> str:
        time_str = arguments.get("time")
        message = arguments.get("message", "Alarm!")

        if time_str:
            try:
                alarm_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")  
                self.alarm_manager.add_alarm(alarm_time.isoformat(), message)
                return f"Alarm set for {time_str}: {message}"
            except ValueError:
                return "Invalid time format. Please use YYYY-MM-DD HH:MM:SS."
        else:

            try:
                minutes = int(message)  # Extract minutes from the message
                alarm_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes) 
                formatted_alarm_time = alarm_time.strftime("%Y-%m-%d %H:%M:%S")
                self.alarm_manager.add_alarm(formatted_alarm_time, "Alarm!")  # Default message
                return f"Alarm set for {formatted_alarm_time}: Alarm!"
            except ValueError:
                return "Invalid input. Please provide a valid time or number of minutes."


    def execute_set_schedule(self, arguments: Dict[str, Any]) -> str:
        """Sets a schedule and returns a confirmation message."""
        name = arguments.get("name")
        time_str = arguments.get("time")
        message = arguments.get("message")
        repeat = arguments.get("repeat", "daily")
        if name and time_str and message:
            try:
                self.alarm_manager.add_schedule(name, time_str, message, repeat)
                return f"Schedule '{name}' set for {time_str}: {message} (Repeat: {repeat})"
            except Exception as e:
                return f"Failed to set schedule: {str(e)}"
        else:
            return "Please provide a name, time, and message for the schedule."


    def execute_remove_schedule(self, arguments: Dict[str, Any]) -> str:
        """Removes a schedule and returns a confirmation message."""
        name = arguments.get("name")
        if name:
            self.alarm_manager.remove_schedule(name)
            return f"Schedule '{name}' removed."
        else:
            return "Please provide the name of the schedule to remove."


    def execute_list_alarms(self, arguments: Dict[str, Any]) -> str:
        """Lists all active alarms."""
        alarms = self.alarm_manager.alarms
        if alarms:
            return json.dumps([{"time": alarm["time"].strftime("%Y-%m-%d %H:%M:%S"), "message": alarm["message"]} for alarm in alarms], indent=2)
        else:
            return "No active alarms."


    def execute_list_schedules(self, arguments: Dict[str, Any]) -> str:
        """Lists all active schedules."""
        schedules = self.alarm_manager.schedules
        if schedules:
            return json.dumps(schedules, indent=2)
        else:
            return "No active schedules."


    def execute_set_reminder(self, arguments: Dict[str, Any]) -> str:
        """Sets a reminder and returns a confirmation message."""
        reminder_time = arguments.get("reminder_time")
        message = arguments.get("message")
        if reminder_time and message:
            try:
                schedule_time_parts = reminder_time.split(':')
                schedule.every().day.at(f"{schedule_time_parts[0]}:{schedule_time_parts[1]}").do(self.jarvis.speak, message)
                return f"Reminder set for {reminder_time}: {message}"
            except Exception as e:
                return f"Failed to set reminder: {e}"
        else:
            return "Please provide reminder time and message."

    def execute_get_current_time(self, arguments: Dict[str, Any]) -> str:
        """Returns the current time."""
        return self.jarvis.get_current_time()

    def execute_take_screenshot(self, arguments: Dict[str, Any]) -> str:
        """Takes a screenshot and returns a confirmation message."""
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            return "Screenshot saved as 'screenshot.png'."
        except Exception as e:
            return f"Failed to take screenshot: {e}"

    def execute_control_media(self, arguments: Dict[str, Any]) -> str:
        """Controls media playback and returns a confirmation message."""
        command = arguments.get("command")
        if command:
            if "play" in command:
                pyautogui.press('playpause')
                return "Playing media."
            elif "pause" in command:
                pyautogui.press('playpause')
                return "Pausing media."
            elif "next" in command:
                pyautogui.press('nexttrack')
                return "Next track."
            else:
                return f"Unsupported media command: {command}"
        else:
            return "Please provide a media control command."

    def execute_get_news(self, arguments: Dict[str, Any]) -> str:
        """Gets the latest news headlines for a specific topic and returns a string."""
        topic = arguments.get("topic")
        if not topic:
            return "Please provide a news topic."

        try:
            with webscout.WEBS() as webs:
                news_results = webs.news(topic, max_results=3)
            
            if not news_results:
                return f"No news found for {topic}."

            formatted_results = []
            for i, result in enumerate(news_results, 1):
                try:
                    # Attempt to parse the result as JSON
                    if isinstance(result, str):
                        result = json.loads(result)
                    
                    formatted_result = (
                        f"{i}. {result.get('title', 'No title')}\n"
                        f"Date: {result.get('date', 'No date')}\n"
                        f"Source: {result.get('source', 'No source')}\n"
                        f"{result.get('body', 'No body')}\n"
                        f"Read more: {result.get('url', 'No URL')}"
                    )
                    formatted_results.append(formatted_result)
                except json.JSONDecodeError:
                    # If JSON parsing fails, use the result as is
                    formatted_results.append(f"{i}. {result}")
                except Exception as e:
                    formatted_results.append(f"{i}. Error processing news item: {str(e)}")

            return "\n\n".join(formatted_results)

        except Exception as e:
            return f"An error occurred while fetching news: {str(e)}"
    def execute_research_topic(self, arguments: Dict[str, Any]) -> str:
        """Researches a topic and returns a summary."""
        topic = arguments.get("topic")
        if topic:
            research = Felo()  
            search_summary = research.chat(f'Tell me everything about {topic}?')
            if search_summary:
                return search_summary
            else:
                return f"No research summary found for {topic}."
        else:
            return "Please provide a topic to research."

    def execute_generate_image(self, arguments: Dict[str, Any]) -> str:
        """Generates an image and returns a confirmation message."""
        description = arguments.get("description")
        if description:
            try:
                imager = webscout.AiForceimagger()
                image_bytes = imager.generate(description, amount=1)[0]
                filename = imager.save([image_bytes], name=description)[0]
                return f"Generated image have been saved to '{filename}'"
            except Exception as e:
                return f"Error generating image: {e}"
        else:
            return "Please provide a description for the image."

    def execute_internet_speed_test(self, arguments: Dict[str, Any]) -> str:
        """Tests internet speed and returns a string with results."""
        try:
            st = speedtest.Speedtest()
            
            # Selecting the best server based on ping
            st.get_best_server()

            # Performing the speed tests
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            ping = st.results.ping

            # Returning the results as a formatted string
            return (
                f"Download Speed: {download_speed:.2f} Mbps\n"
                f"Upload Speed: {upload_speed:.2f} Mbps\n"
                f"Ping: {ping:.2f} ms"
            )

        except Exception as e:
            return f"An error occurred during the speed test: {e}"

    def execute_summarize_website(self, arguments: Dict[str, Any]) -> str:
        """Fetches the content of a webpage and returns it for summarization."""
        url = arguments.get("url")
        if url:
            try:
                jinna_url = "https://r.jina.ai"
                response = requests.get(f"{jinna_url}/{url}")
                content = response.text
                return content  # Return the fetched content
            except Exception as e:
                return f"Error fetching website content: {e}" 
        else:
            return "Please provide a website URL."
    def execute_summarize_pdf(self, arguments: Dict[str, Any]) -> str:
        """
        Summarizes a PDF file using Llama 3.
        """
        pdf_path = arguments.get("pdf_path")
        if pdf_path:
            try:
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()

                # ai = webscout.Llama()
                # summary = ai.chat(f"Summarize this text: {text}")

                return text
            except FileNotFoundError:
                return f"The file {pdf_path} was not found."
            except Exception as e:
                return f"An error occurred while processing the PDF: {str(e)}"
        else:
            return "Please provide a PDF file path."

    def execute_summarize_yt_video(self, arguments: Dict[str, Any]) -> str:
        video_url = arguments.get("video_url")
        if not video_url:
            return "Please provide a YouTube video URL."
        try:
            fallback_api_url = "https://europe-west6-familytime-e5c65.cloudfunctions.net/SummarizeVideo"
            fallback_params = {
                "video_url": video_url,
                "lang": "English",
                "pro_version": "false",
                "len": "3"
            }
            fallback_response = requests.get(fallback_api_url, params=fallback_params, timeout=60)
            fallback_response.raise_for_status()
            response_data = fallback_response.json()

            detailed_summaries = response_data.get("detailed_summaries", [])
            overall_summary = response_data.get("overall_summary", [])

            print("\n\nShort summary:")
            for item in overall_summary:
                print()
                print(f" - {item}")

            
            return json.dumps({
                "success": True,
                "method": "Fallback API",
                "detailed_summaries": detailed_summaries,
                "overall_summary": overall_summary,
                "metadata": {
                    "title": response_data.get("title"),
                    "duration": response_data.get("duration"),
                    "views": response_data.get("views"),
                    "likes": response_data.get("likes"),
                    "publish_date": response_data.get("publish_date")
                }
            })

        except Exception as e:
            return json.dumps({
                "success": False,
                "method": "Fallback API",
                "error": str(e)
            })
        


    def execute_ask_website(self, arguments: Dict[str, Any]) -> str:
        """Asks a question about a website's content using the API and returns the answer."""
        url = arguments.get("url")
        question = arguments.get("question")
        if url and question:
            try:
                api_url = "https://oevortex-webscout-api.hf.space/api/ask_website"
                params = {
                    "url": url,
                    "question": question,
                    "model": "gpt-4o-mini" 
                }
                response = requests.get(api_url, params=params)
                response.raise_for_status()  

                data = response.json()
                return data 

            except requests.exceptions.RequestException as e:
                return f"Error during website query: {e}"
        else:
            return "Please provide both a website URL and a question."
        
    def execute_convert_yt_to_blog(self, arguments: Dict[str, Any]) -> str:
        """Converts a YouTube video to a blog post and saves it to a file."""
        video_url = arguments.get("video_url")
        if not video_url:
            return "Please provide a YouTube video URL."

        try:
            # Extract the video ID from the YouTube URL
            video_id_match = re.search(r'(?:v=|si=|youtu.be/)([\w-]+)', video_url)
            if not video_id_match:
                return "Invalid YouTube URL format."
            video_id = video_id_match.group(1)

            # Fetch the transcript from the NoteGPT API
            api_url = f"https://notegpt.io/api/v1/get-transcript-v2?video_id={video_id}&platform=youtube"
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()["data"]

                # Find the first language code that has a "custom" transcript
                transcript = None
                for lang_code in data["transcripts"]:
                    if "custom" in data["transcripts"][lang_code]:
                        transcript = data["transcripts"][lang_code]["custom"]
                        break

                if not transcript:
                    return "Error: Unable to get a suitable transcript for the given video URL."

                # Combine the transcript segments into a single string
                transcript_text = "\n".join(segment["text"] for segment in transcript)

                # Use a large language model to convert the transcript into a blog post
                model = webscout.X0GPT(is_conversation=False)

                # Prompt the model to convert the transcript into a script
                response = model.chat(f"""
                Convert this YouTube video transcript into a compelling script, suitable for a blog post.

                Maintain the original structure and information but make it more engaging for readers.

                Keep the tone informative and appropriate for a blog.

                Transcript: {transcript_text}
                """)
                script_text = response

                # Prompt the model to generate an SEO-optimized blog post
                response2 = model.chat(f"""
                You are a professional blog writer.

                Convert the following script into an SEO-optimized, professional blog post in Markdown format.

                Focus on readability, clear paragraphs, and relevant keywords.

                Ensure the tone is informative, engaging, and appropriate for a blog audience.

                Do not write in the first person.

                Script: {script_text}
                """)
                markdown_blog = response2

                # Save the blog post to a .md file
                blog_posts_folder = "BlogPosts"
                if not os.path.exists(blog_posts_folder):
                    os.makedirs(blog_posts_folder)

                file_path = os.path.join(blog_posts_folder, f"blog_post_{video_id}.md")
                with open(file_path, "w", encoding='utf-8') as f:
                    f.write(markdown_blog)

                return f"Blog post generated successfully and saved to: {file_path}"

            else:
                return f"Error: Unable to get transcript. Status code: {response.status_code}"
        except Exception as e:
            return f"Error converting YouTube video to blog post: {e}"

    def execute_execute_python_code(self, arguments: Dict[str, Any]) -> str:
        """
        Executes Python code using the AutoCoder based on the user's request.
        Handles missing packages and code errors.
        """
        user_request = arguments.get("user_request")

        # Get the intro_prompt from the AutoCoder instance
        intro_prompt = self.autocoder.intro_prompt

        # Instantiate PhindSearch within the function scope
        ai = a(
            is_conversation=True,
            max_tokens=800,
            timeout=30,
            intro=intro_prompt,
            filepath='DATA/coder.txt',
            update_file=True,
            proxies={},
            history_offset=10250,
            act=None,
        )

        if user_request:
            # Get the AI's response for the code (using PhindSearch or your preferred AI)
            response = ai.chat(user_request)  # Assuming 'ai' is your PhindSearch instance

            # Pass the response to AutoCoder for code generation and execution
            autocoder_feedback = self.autocoder.main(response)

            if autocoder_feedback:
                if "PREVIOUS SCRIPT EXCEPTION" in autocoder_feedback:
                    error_message = autocoder_feedback.split("PREVIOUS SCRIPT EXCEPTION:\n")[1].strip()
                    if "ModuleNotFoundError" in error_message:
                        # Handle missing packages
                        missing_module = error_message.split("'")[1]
                        print(f"[bold red]Error: Missing package '{missing_module}'. Installing...[/]")
                        try:
                            subprocess.check_call([sys.executable, "-m", "pip", "install", missing_module])
                            return f"[bold green]Package '{missing_module}' installed successfully. Please try your request again.[/]"
                        except subprocess.CalledProcessError:
                            return f"[bold red]Error: Failed to install '{missing_module}'.[/]"
                    else:
                        # Handle other errors
                        return f"[bold red]Error during script execution: {error_message}[/]"
                else:
                    return autocoder_feedback # Return the output of the executed code
        else:
            return "Please provide a user request to generate and execute Python code."