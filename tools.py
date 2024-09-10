TOOLS = [
  {
    "type": "function",
    "function": {
      "name": "web_search",
      "description": "Search the web for information using Google Search.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query to be executed."
          }
        },
        "required": ["query"]
      }
    }
  },
  {
    "type": "function",
    "function": {
        "name": "open_app",
        "description": "Opens a specified application.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {
                    "type": "string",
                    "description": "The name of the application to open."
                }
            },
            "required": ["app_name"]
        }
    }
  },
  {
      "type": "function",
      "function": {
          "name": "close_app",
          "description": "Closes a specified application.",
          "parameters": {
              "type": "object",
              "properties": {
                  "app_name": {
                      "type": "string",
                      "description": "The name of the application to close."
                  }
              },
              "required": ["app_name"]
          }
      }
  },
  {
      "type": "function",
      "function": {
          "name": "play_youtube",
          "description": "Plays a YouTube video.",
          "parameters": {
              "type": "object",
              "properties": {
                  "query": {
                      "type": "string",
                      "description": "The search query for the YouTube video."
                  }
              },
              "required": ["query"]
          }
      }
  },
  {
      "type": "function",
      "function": {
          "name": "system_control",
          "description": "Controls system settings (i.e, mute, unmute, volume down, minimize all, volume up, shutdown ).",
          "parameters": {
              "type": "object",
              "properties": {
                  "command": {
                      "type": "string",
                      "description": "The system control command to execute (i.e, mute, unmute, volume down, minimize all, volume up, shutdown )."
                  }
              },
              "required": ["command"]
          }
      }
  },
  {
    "type": "function",
    "function": {
      "name": "open_website",
      "description": "Open a website in the default browser.",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "description": "The URL of the website to open."
          }
        },
        "required": ["url"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "general_ai",
      "description": "Use general AI knowledge to answer questions or perform tasks that don't require external tools.",
      "parameters": {
        "type": "object",
        "properties": {
          "question": {
            "type": "string",
            "description": "The question or task to be processed."
          }
        },
        "required": ["question"]
      }
    }
  }
]