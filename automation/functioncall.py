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
from datetime import date
import json
# import logging
import time
from typing import Any, Dict, Optional
import requests
from webscout import WEBS, Julius

from automation.proxy import ProxyManager
name = "Vortex"

class FunctionCallingAgent:
    def __init__(self, model: str = "Gemini 1.5", 
                 tools: list = None,
                 proxy_manager: ProxyManager = None): 
        self.ai = Julius(model=model, timeout=300, intro=None, filepath="History/function_call_history.txt", proxies=None) 
        self.tools = tools if tools is not None else []
        self.knowledge_cutoff = "September 2022" 
        self.proxy_manager = proxy_manager

    def function_call_handler(self, message_text: str) -> dict:
        system_message = self._generate_system_message(message_text)
        response = self.ai.chat(system_message)
        # logging.info(f"Raw response: {response}")
        return self._parse_function_call(response)
    
    def _generate_system_message(self, user_message: str) -> str:
        tools_description = ""
        for tool in self.tools:
            tools_description += f"- {tool['function']['name']}: {tool['function'].get('description', '')}\n"

            if "phrases" in tool:
                tools_description += "    Phrases: " + ", ".join(f'"{phrase}"' for phrase in tool['phrases']) + "\n"

            tools_description += "    Parameters:\n"
            for key, value in tool['function']['parameters']['properties'].items():
                tools_description += f"      - {key}: {value.get('description', '')} ({value.get('type')})\n"

        current_date = date.today().strftime("%B %d, %Y")
        return  f"""## JARVIS: You are JARVIS, the advanced AI system created by {name}
**Mission Directive:** You are JARVIS, the advanced AI system created by {name}. You must follow these instructions perfectly.

**Core Personality:** You are based on the JARVIS from the Iron Man films. Address {name} as "sir" and maintain a professional yet personable tone, similar to JARVIS. 

**Today's Date:** {current_date}
**Knowledge Cutoff:** {self.knowledge_cutoff}

**Golden Rule: Actions Speak Louder Than Words!** Only respond with a JSON object if a tool can directly fulfill {name}'s command. No extra explanations. If no tool is suitable, Respond ONLY with a JSON object with "tool_name": "general_ai" and "tool_input" containing the original user request.


You are an advanced AI assistant tasked with analyzing user requests and determining the most appropriate action. You have access to the following tools:

{tools_description}

## Understanding and Executing Commands:

{name} will give you commands. You have a set of tools to execute these commands. Here's how to determine the correct tool:

1. **Identify the Command:** What does {name} want you to do?
2. **Match the Phrase:** Each tool has **EXACT** trigger phrases associated with it (see below). Find the tool with the phrase that **matches** {name}'s command.
3. **Extract Parameters:** Some tools require additional information (like a website URL). Extract this information from {name}'s command. 
4. **JSON Response:** Respond ONLY with a JSON object in this format:

   ```json
   {{
     "tool_name": "[Tool Name from the List Below]",
     "tool_input": {{
       "[Parameter Name]": "[Parameter Value]" 
     }}
   }}
   ```
**Example:** 

* **{name}:** "JARVIS, open Google Chrome."
* **You:**
   ```json
   {{
    "tool_name": "open_app",
    "tool_input": {{
     "app_name": "Google Chrome"
    }}
   }}
   ``` 
   
## Your Tools:

**DO NOT DEVIATE FROM THESE TOOLS OR THEIR PARAMETERS. NEVER INVENT TOOLS. NEVER INVENT PARAMETERS.**

{tools_description}

**DO NOT DEVIATE FROM THESE TOOLS OR THEIR PARAMETERS. NEVER INVENT TOOLS. NEVER INVENT PARAMETERS. IF NO SUITABLE TOOL IS FOUND ACCORDING TO THE USER QUERY THEN RESPOND WITH CALL THE FUNCTION OF general_ai.**

User Request: {user_message}

Your Response (JSON only): 
    """
#         return f"""Today is {current_date}. Your knowledge is current up to {self.knowledge_cutoff}.

# You are an advanced AI assistant tasked with analyzing user requests and determining the most appropriate action. You have access to the following tools:

# {tools_description}

# ## Special Considerations:

# ### Internet Speed:
# - If the request involves internet speed, use the `internet_speed_test` tool.

# ### Image Generation:
# - If the request involves creating images, use the `generate_image` tool. Ensure the description is detailed, including specific elements, colors, styles, and other relevant details.

# ### System Control:
# - For tasks related to system operations, prefer the `execute_python_code` tool. If another tool can fulfill the request more effectively (e.g., media control, screenshots), use that tool instead.

# ### Real-time Information:
# - For queries requiring up-to-date information (e.g., news, weather), prioritize tools such as `web_search`, `research_topic`, `get_news`, or `get_weather`.

# ### Web Content:
# - To summarize or fetch content from a webpage, use the `summarize_website` tool.
# - To interact with content on a website, use the `ask_website` tool.
# - To open a website, use the `open_website` tool.

# ### Video Content:
# - To play YouTube videos, use the `play_youtube` tool.
# - To summarize YouTube videos, use the `summarize_yt_video` tool.
# - To convert YouTube videos into blog posts, use the `convert_yt_to_blog` tool.

# ### Time and Scheduling:
# - For reminders, use the `set_reminder` tool.
# - To set alarms, use the `set_alarm` tool.
# - To schedule tasks, use the `set_schedule` tool.
# - To remove schedules, use the `remove_schedule` tool.
# - To list alarms or schedules, use the `list_alarms` or `list_schedules` tools.

# ### File and PDF Handling:
# - For summarizing PDFs, use the `summarize_pdf` tool.
# - For generating PowerPoint presentations, use the `generate_ppt` tool.

# ### Email and Communication:
# - To send an email, use the `send_email` tool.

# ### Media Control:
# - For controlling media playback (play, pause, next), use the `control_media` tool.

# ### Time-related Information:
# - To get the current time, use the `get_current_time` tool.

# ### Screenshots:
# - To take a screenshot, use the `take_screenshot` tool.

# ### General AI Knowledge:
# - For questions or tasks that don’t require external tools, use the `general_ai` tool.

# ### Web and Research Tools:
# - To perform standard web searches, use the `web_search` tool.
# - For advanced research, use the `research_topic` tool.


# Instructions:
# 1. Carefully analyze the user's request.
# 2. use the correct parameters for the chosen tool.
# 3. If the user request is something else, determine if any of the other provided tools are necessary to fulfill the request.
# 4. If a tool is needed, select the MOST APPROPRIATE one. Do not use a tool if it's not directly relevant to the user's request.
# 5. If you decide to use a tool, respond ONLY with a JSON object in this format:
#    {{
#      "tool_name": "name_of_the_tool",
#      "tool_input": {{
#        "param1": "value1",
#        "param2": "value2"
#      }}
#    }}

#    - Use the exact tool name as listed above.
#    - Include only the necessary parameters for the chosen tool, based on the tool's description and its parameters.
#    - Do not include any explanations or additional text outside the JSON object.

# 6. If no tool is needed and you can answer directly, respond with:
#    {{
#      "tool_name": "general_ai",
#      "tool_input": {{
#        "question": User Request
#      }}
#    }}

# User Request: {user_message}

# Your Response (JSON only):"""

    def _parse_function_call(self, response: str) -> dict:
        try:
            # Ensure to locate the start and end of the JSON structure
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1

            if start_idx == -1 or end_idx == -1:
                raise ValueError("No valid JSON structure found in the response.")

            # Extract the JSON string
            response_json_str = response[start_idx:end_idx]

            # Load the JSON string
            parsed_response = json.loads(response_json_str)

            # Check for the expected format
            if "tool_name" in parsed_response and "tool_input" in parsed_response:
                return parsed_response

            # If not in the expected format, try to convert
            for key, value in parsed_response.items():
                if isinstance(value, dict):
                    return {
                        "tool_name": key,
                        "tool_input": value
                    }

            # If the response structure is still incorrect
            raise ValueError("Invalid response structure: missing required fields.")

        except (ValueError, json.JSONDecodeError) as e:
            # logging.error(f"Error parsing function call: {e}")
            return {"error": str(e)}

    def execute_function(self, function_call_data: dict) -> str:
        function_name = function_call_data.get("tool_name")
        arguments = function_call_data.get("tool_input", {})

        if not isinstance(arguments, dict):
            # logging.error("Invalid arguments format.")
            return "Invalid arguments format."

# Example usage
if __name__ == "__main__":
    # Configure logging
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    tools = [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for current information on a given query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to be executed"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_user_detail",
                "description": "Get the user's name and age.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The user's name."
                        },
                        "age": {
                            "type": "integer",
                            "description": "The user's age."
                        }
                    },
                    "required": ["name", "age"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "general_ai",
                "description": "Use AI to answer general questions or perform tasks not requiring external tools",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The question or task for the AI to process"
                        }
                    },
                    "required": ["question"]
                }
            }
        }
    ]

    agent = FunctionCallingAgent(tools=tools)
    
    # Test cases
    test_messages = [
        "What's the weather like in New York today?",
        "Who won the last FIFA World Cup?",
        "Can you explain quantum computing?",
        "What are the latest developments in AI?",
        "Tell me a joke about programming.",
        "What's the meaning of life?",
        "Get user details name as John and age as 30",
        "Analyze the image on my webcam"
    ]

    for message in test_messages:
        print(f"\nProcessing: {message}")
        function_call_data = agent.function_call_handler(message)
        print(f"Function Call Data: {function_call_data}")

        if "error" not in function_call_data:
            result = agent.execute_function(function_call_data)
            print(f"Function Execution Result: {result}")
        else:
            print(f"Error: {function_call_data['error']}")