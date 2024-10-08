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
    },
    "phrases": [
      "search the web for",
      "google search",
      "find information about",
      "look up",
      "research"
    ]
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
    },
    "phrases": [
      "open application",
      "launch app",
      "start",
      "open"
    ]
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
      },
      "phrases": [
        "close application",
        "shut down app",
        "exit",
        "quit"
      ]
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
      },
      "phrases": [
        "play YouTube video",
        "find on YouTube",
        "watch on YouTube",
        "search YouTube for"
      ]
  },
  # {
  #     "type": "function",
  #     "function": {
  #         "name": "system_control",
  #         "description": "Controls system settings (i.e, mute, unmute, volume down, minimize all, volume up, shutdown ).",
  #         "parameters": {
  #             "type": "object",
  #             "properties": {
  #                 "command": {
  #                     "type": "string",
  #                     "description": "The system control command to execute (i.e, mute, unmute, volume down, minimize all, volume up, shutdown )."
  #                 }
  #             },
  #             "required": ["command"]
  #         }
  #     },
  #     "phrases": [
  #       "mute the system",
  #       "unmute the system",
  #       "turn the volume down",
  #       "minimize all windows",
  #       "turn the volume up",
  #       "shut down the computer"
  #     ]
  # },
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
    },
    "phrases": [
      "open website",
      "go to website",
      "visit website",
      "open URL",
      "navigate to" 
    ]
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
    },
    "phrases": [
      "answer a question",
      "tell me about",
      "explain",
      "what is",
      "who is", 
      "how to",
      "define"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "get_weather",
      "description": "Gets the current weather for a given location.",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state (e.g., 'London, UK')."
          }
        },
        "required": ["location"]
      }
    },
    "phrases": [
      "get weather",
      "what's the weather in",
      "weather forecast for",
      "check weather"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "send_email",
      "description": "Sends an email.",
      "parameters": {
        "type": "object",
        "properties": {
          "to_email": {
            "type": "string",
            "description": "The recipient's email address."
          },
          "subject": {
            "type": "string",
            "description": "The subject of the email."
          },
          "body": {
            "type": "string",
            "description": "The body of the email."
          }
        },
        "required": ["to_email", "subject", "body"]
      }
    },
    "phrases": [
      "send email",
      "email someone",
      "send a message to",
      "compose an email"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "set_reminder",
      "description": "Sets a reminder for a specific time.",
      "parameters": {
        "type": "object",
        "properties": {
          "reminder_time": {
            "type": "string",
            "description": "The time for the reminder (e.g., '10:00 AM')."
          },
          "message": {
            "type": "string",
            "description": "The reminder message."
          }
        },
        "required": ["reminder_time", "message"]
      }
    },
    "phrases": [
      "set reminder",
      "remind me to",
      "create a reminder",
      "set an alert"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "get_current_time",
      "description": "Gets the current time.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    "phrases": [
      "what time is it",
      "get current time",
      "tell me the time",
      "what's the time"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "take_screenshot",
      "description": "Takes a screenshot of the current screen.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    "phrases": [
      "take screenshot",
      "capture screen",
      "screenshot",
      "snapshot"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "control_media",
      "description": "Controls media playback (e.g., play, pause, next track).",
      "parameters": {
        "type": "object",
        "properties": {
          "command": {
            "type": "string",
            "description": "The command to execute (e.g., 'play', 'pause', 'next')"
          }
        },
        "required": ["command"]
      }
    },
    "phrases": [
      "play music",
      "pause music",
      "next track",
      "previous track",
      "stop music"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "get_news",
      "description": "Get the latest news headlines on a specific topic.",
      "parameters": {
        "type": "object",
        "properties": {
          "topic": {
            "type": "string",
            "description": "The topic for the news headlines (e.g., 'technology', 'business', 'sports')."
          }
        },
        "required": ["topic"]
      }
    },
    "phrases": [
      "get news",
      "latest news on",
      "news headlines about",
      "what's happening in" 
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "research_topic",
      "description": "Research a given topic this is like a advance and deep web search.",
      "parameters": {
        "type": "object",
        "properties": {
          "topic": {
            "type": "string",
            "description": "The topic to research."
          }
        },
        "required": ["topic"]
      }
    },
    "phrases": [
      "research topic",
      "deep dive into",
      "learn more about",
      "investigate",
      "find information on"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "generate_image",
      "description": "Use this tool toGenerate image based on a detailed text description. (text to image) The description should include specific elements, colors, styles, and any other relevant details to accurately create the desired image.",
      "parameters": {
        "type": "object",
        "properties": {
          "description": {
            "type": "string",
            "description": "A detailed text description of the image to generate. Include specific elements, colors, styles, and any other relevant details."
          }
        },
        "required": ["description"]
      }
    },
    "phrases": [
      "generate image",
      "create image from text",
      "text to image",
      "visualize", 
      "imagine"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "internet_speed_test",
      "description": "Tests the internet connection speed (download, upload, ping).",
      "parameters": {
        "type": "object",
        "properties": {},
      }
    },
    "phrases": [
      "test internet speed",
      "check internet connection",
      "speed test",
      "how fast is my internet"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "summarize_website",
      "description": "Fetch the content of a webpage and return it for summarization.",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "description": "The URL of the webpage to fetch and summarize."
          }
        },
        "required": ["url"]
      }
    },
    "phrases": [
      "summarize website", 
      "get summary of webpage",
      "tldr",
      "summarize this URL"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "summarize_pdf",
      "description": "Summarize a PDF file.",
      "parameters": {
        "type": "object",
        "properties": {
          "pdf_path": {
            "type": "string",
            "description": "The path to the PDF file."
          }
        },
        "required": ["pdf_path"]
      }
    },
    "phrases": [
      "summarize PDF",
      "get summary of PDF",
      "tldr this PDF"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "summarize_yt_video",
      "description": "Summarize a YouTube video.",
      "parameters": {
        "type": "object",
        "properties": {
          "video_url": {
            "type": "string",
            "description": "The URL of the YouTube video."
          }
        },
        "required": ["video_url"]
      }
    },
    "phrases": [
      "summarize YouTube video",
      "get summary of YouTube video", 
      "tldr this YouTube video"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "ask_website",
      "description": "Enables users to ask a question and receive a response based on the content of a specified website. This function effectively allows users to chat with the website, extracting relevant information to answer their queries.",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "description": "The URL of the website to interact with."
          },
          "question": {
            "type": "string",
            "description": "The question to ask about the content of the specified website."
          }
        },
        "required": ["url", "question"]
      }
    },
    "phrases": [
      "ask website",
      "question website",
      "chat with website",
      "get information from website"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "set_alarm",
      "description": "Set an alarm for a specific time.",
      "parameters": {
        "type": "object",
        "properties": {
          "time": {
            "type": "string",
            "description": "The time for the alarm in YYYY-MM-DD HH:MM:SS format."
          },
          "message": {
            "type": "string",
            "description": "The message to be spoken when the alarm triggers."
          }
        },
        "required": ["time"]
      }
    },
    "phrases": [
      "set alarm",
      "wake me up at",
      "create an alarm", 
      "set a timer" 
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "set_schedule",
      "description": "Set a schedule to trigger actions at specific times.",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "The name of the schedule."
          },
          "time": {
            "type": "string",
            "description": "The time for the schedule in HH:MM format."
          },
          "message": {
            "type": "string",
            "description": "The message to be spoken when the schedule triggers."
          },
          "repeat": {
            "type": "string",
            "description": "The frequency of the schedule (e.g., daily, weekly, monthly).",
            "default": "daily" 
          }
        },
        "required": ["name", "time", "message"]
      }
    },
    "phrases": [
      "set schedule",
      "schedule a task",
      "create a schedule",
      "schedule an event"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "remove_schedule",
      "description": "Remove a previously set schedule.",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "The name of the schedule to remove."
          }
        },
        "required": ["name"]
      }
    },
    "phrases": [
      "remove schedule",
      "delete schedule",
      "cancel schedule",
      "unschedule" 
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "list_alarms",
      "description": "List all active alarms.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    "phrases": [
      "list alarms", 
      "show alarms",
      "what alarms are set",
      "my alarms"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "list_schedules",
      "description": "List all active schedules.",
      "parameters": {
        "type": "object",
        "properties": {}
      }
    },
    "phrases": [
      "list schedules",
      "show schedules",
      "what schedules are set", 
      "my schedules"
    ]
  },
  {
    "type": "function",
    "function": {
      "name": "convert_yt_to_blog",
      "description": "Converts a YouTube video to a blog post and saves it to a file.",
      "parameters": {
        "type": "object",
        "properties": {
          "video_url": {
            "type": "string",
            "description": "The URL of the YouTube video to be converted into a blog post."
          }
        },
        "required": ["video_url"]
      }
    },
    "phrases": [
      "convert YouTube to blog",
      "YouTube to blog post",
      "make a blog from YouTube" 
    ]
  },
  {
      "type": "function",
      "function": {
          "name": "generate_ppt",
          "description": "Generates a PowerPoint presentation based on a given topic.",
          "parameters": {
              "type": "object",
              "properties": {
                  "topic": {
                      "type": "string",
                      "description": "The topic for the presentation."
                  },
                  "design_number": {
                      "type": "integer",
                      "description": "The design template to use (1-N)",
                      "default": 1
                  }
              },
              "required": ["topic"]
          }
      },
      "phrases": [
        "generate PowerPoint",
        "create presentation", 
        "make a slideshow", 
        "prepare a presentation"
      ]
  },
  {
        "type": "function",
        "function": {
            "name": "execute_python_code",
            "description": "auto Writes and executes Python code based on a user's request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_request": {
                        "type": "string",
                        "description": "The user's request for the code to be written and executed (e.g., 'Take a screenshot and save it to the desktop')."
                    }
                },
                "required": ["user_request"] 
            }
        },
        "phrases": [
          "execute Python code",
          "run Python script",
          "write and run Python",
          "code in Python" 
        ]
    },
    {
    "type": "function",
    "function": {
      "name": "vision_chat",
      "description": "It is used for vision analysis or vision model with an image path. Sends a request to Homeworkify API for image analysis or text-based questions. You can provide an image attachment along with the question user has asked.",
      "parameters": {
        "type": "object",
        "properties": {
          "input_message": {
            "type": "string",
            "description": "The text message or question to send to Homeworkify. This is required"
          },
          "attachment_path": {
            "type": "string",
            "description": "The path to the image attachment (e.g., 'captured_image.jpg') This is optional if no filepath is given by the user just make it None"
          }
        },
        "required": ["input_message"]
      }
    },
    "phrases": [
      "analyze image",
      "ask about this image",
      "what's in this picture",
      "describe this image",
      "vision analysis"
    ]
  }
]