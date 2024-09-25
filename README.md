# JARVIS: Your Advanced AI Assistant (Function Calling Architecture)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

JARVIS is a sophisticated AI assistant built using a function-calling architecture.  Unlike traditional rule-based systems with extensive `if-else` chains, JARVIS leverages external tools and APIs to perform a wide range of tasks, resulting in a more flexible, scalable, and robust system.

## Features

* **Natural Language Understanding:** JARVIS understands and responds to natural language commands.
* **Function Calling:**  Employs a function-calling architecture to interact with various external tools and services (APIs). This eliminates the need for hardcoded rules and allows for easy extensibility.
* **Multimodal Interaction:** Supports both text and voice-based interactions.  (Voice support requires additional libraries and configuration).
* **Tool Integration:**  Integrates with numerous tools, including:
    * Web Search (Google Search)
    * Application Control (Opening and closing applications)
    * YouTube Video Playback
    * Website Navigation
    * Weather Information
    * Email Sending
    * Reminders and Scheduling
    * Screenshot Capture
    * Media Control
    * News Retrieval
    * Advanced Research (using various APIs)
    * Image Generation (using various APIs)
    * Internet Speed Testing
    * PDF Summarization
    * Website Summarization and Question Answering
    * YouTube Video Summarization
    * Python Code Execution
    * PowerPoint Presentation Generation
    * **Image Analysis (using Homeworkify API)**
* **Conversation Management:** Maintains conversation context and history to provide more relevant responses.
* **Proxy Support:**  Includes proxy management for improved network reliability.
* **Dataset Building:** Records user interactions and tool results to a JSON file for potential training data.

## Architecture

JARVIS uses a three-tiered architecture:

1. **User Interface:** Provides a command-line interface (CLI) for interaction. Voice interaction is optionally supported.
2. **Function Calling Agent:**  Analyzes user requests and determines the appropriate tool or API to use.
3. **Function Executor:** Executes the selected functions, interacts with external tools and services, and returns the results.

This architecture promotes modularity, making it easy to add new features and tools by simply modifying the `tools.py` file and adding new functions in `function_executor.py`.


## Getting Started

1. **Prerequisites:**
   - Python 3.9 or higher
   - `pip` (Python package manager)
   - Install required libraries:
     ```bash
     pip install -r requirements.txt 
     ```
2. **Clone the Repository:**
   ```bash
   git clone https://github.com/OE-LUCIFER/JARVIS.git
   ```
3. **Configure APIs:**  You will need to obtain API keys for various services used by JARVIS (e.g., Homeworkify, Voicepods). Replace placeholders in the code with your actual API keys.
4. **Run JARVIS:**4. **Run JARVIS:**
   ```bash
   python main.py
   ```
   Choose your interaction mode (voice or text).  If using voice mode, ensure that you have the necessary speech recognition libraries installed and configured.


## Contributing

Contributions are welcome! Please feel free to open issues and submit pull requests.


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is provided "as is" without any warranty. Use at your own risk. The developer is not responsible for any issues or damages arising from the use of this software.  This project is intended for educational purposes.
