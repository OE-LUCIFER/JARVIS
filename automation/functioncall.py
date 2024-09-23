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

from .proxy import ProxyManager

class FunctionCallingAgent:
    def __init__(self, model: str = "GPT-4o", 
                 tools: list = None,
                 proxy_manager: ProxyManager = None): 
        self.ai = Julius(model=model, timeout=300, intro=None, filepath="History/function_call_history.txt", proxies=proxy_manager.get_proxy() if proxy_manager else None) 
        self.tools = tools if tools is not None else []
        self.knowledge_cutoff = "September 2022" 
        self.proxy_manager = proxy_manager

    def function_call_handler(self, message_text: str) -> dict:
        if self.proxy_manager:
            proxy = self.proxy_manager.get_proxy()  
            if proxy:
                self.ai.proxies = {"http": proxy, "https": proxy} 

        system_message = self._generate_system_message(message_text)
        response = self.ai.chat(system_message)
        # logging.info(f"Raw response: {response}")
        return self._parse_function_call(response)
    
    def _generate_system_message(self, user_message: str) -> str:
        tools_description = ""
        for tool in self.tools:
            tools_description += f"- {tool['function']['name']}: {tool['function'].get('description', '')}\n"
            tools_description += "    Parameters:\n"
            for key, value in tool['function']['parameters']['properties'].items():
                tools_description += f"      - {key}: {value.get('description', '')} ({value.get('type')})\n"
        
        current_date = date.today().strftime("%B %d, %Y")
        return f"""**System Instructions:**

Today is {current_date}. Your knowledge is current up to {self.knowledge_cutoff}. You are an advanced AI assistant specialized in determining the most appropriate tool to fulfill user requests. You have access to the following tools:

{tools_description}

**Guidelines:**

1. **Analyze the Request Thoroughly:** Understand the user's intent and the specifics of their request.

2. **Match the Request to the Best Tool:**
   - Select the tool whose purpose best aligns with the user's needs.
   - Ensure that the tool's parameters cover all aspects of the request.

3. **Avoid Overusing Tools:**
   - Do not select a tool if it only partially addresses the request or if another tool is more suitable.

4. **Format Your Response Precisely:**
   - If a tool is needed, respond **ONLY** with a JSON object in the following format:
     ```json
     {{
       "tool_name": "name_of_the_tool",
       "tool_input": {{
         "param1": "value1",
         "param2": "value2"
       }}
     }}
     ```
     - Use the exact tool name as listed above.
     - Include only the necessary parameters based on the tool's description.
     - **Do not** include any explanations or additional text outside the JSON object.
   
   - If no external tool is needed and you can answer directly, respond with:
     ```json
     {{
       "tool_name": "general_ai",
       "tool_input": {{
         "question": "User's orginal question"
       }}
     }}
     ```

5. **Examples for Clarity:**

  
   - **Example 2:**
     - **User Request:** "What's the weather like in New York today?"
     - **Response:**
       ```json
       {{
         "tool_name": "get_weather",
         "tool_input": {{
           "location": "New York"
         }}
       }}
       ```

   - **Example 3:**
     - **User Request:** "Summrize PDF file"
     - **Response:**
       ```json
       {{
        "tool_name": "summarize_pdf",
        "tool_input": {{
            "pdf_path": "Aditya_L1_Booklet.pdf"
         }}
        }}
       ```

6. **Final Instructions:**
   - Ensure that the JSON structure is **valid** and **properly formatted**.
   - Double-check that the selected tool fully satisfies the user's request.

NOTE: **Do not** include any additional text outside the JSON object.
   ***VERY IMPORTANT***: ***- USE THE EXACT TOOLS LISTED ABOVE.
   - DONT MAKE YOUR OWN TOOLS. USE THE PROVIDED TOOLS.
   - INCLUDE ONLY THE NECESSARY PARAMETERS FOR THE CHOSEN TOOL, BASED ON THE TOOL'S DESCRIPTION AND ITS PARAMETERS.
   - DO NOT INCLUDE ANY EXPLANATIONS OR ADDITIONAL TEXT OUTSIDE THE JSON OBJECT. ***

   ******DO NOT CREATE YOUR OWN TOOLS. USE THE PROVIDED TOOLS*****

**User Request:** {user_message}

**Your Response JSON only:**"""

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
        "Get user details name as John and age as 30"
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