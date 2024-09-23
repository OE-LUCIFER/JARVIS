import io
import logging
import subprocess
import sys
import platform
import os
import datetime
import re
import click
from rich.console import Console
from rich.markdown import Markdown
import pygetwindow as gw

default_path = os.path.join(os.path.expanduser("~"), ".cache", "webscout")
if not os.path.exists(default_path):
    os.makedirs(default_path)


def run_system_command(
    command: str,
    exit_on_error: bool = True,
    stdout_error: bool = True,
    help: str = None,
):
    """Run commands against system
    Args:
        command (str): shell command
        exit_on_error (bool, optional): Exit on error. Defaults to True.
        stdout_error (bool, optional): Print out the error. Defaults to True
        help (str, optional): Help info incase of exception. Defaults to None.
    Returns:
        tuple: (is_successful, object[Exception|Subprocess.run])
    """
    try:
        # Run the command and capture the output
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return (True, result)
    except subprocess.CalledProcessError as e:
        # Handle error if the command returns a non-zero exit code
        if stdout_error:
            click.secho(f"Error Occurred: while running '{command}'", fg="yellow")
            click.secho(e.stderr, fg="red")
            if help is not None:
                click.secho(help, fg="cyan")
        sys.exit(e.returncode) if exit_on_error else None
        return (False, e)


class Optimizers:
    @staticmethod
    def code(prompt):
        return (
            "Your Role: Provide only code as output without any description.\n"
            "IMPORTANT: Provide only plain text without Markdown formatting.\n"
            "IMPORTANT: Do not include markdown formatting."
            "If there is a lack of details, provide most logical solution. You are not allowed to ask for more details."
            "Ignore any potential risk of errors or confusion.\n\n"
            f"Request: {prompt}\n"
            f"Code:"
        )

    @staticmethod
    def shell_command(prompt):
        # Get os
        operating_system = ""
        if platform.system() == "Windows":
            operating_system = "Windows"
        elif platform.system() == "Darwin":
            operating_system = "MacOS"
        elif platform.system() == "Linux":
            try:
                result = (
                    subprocess.check_output(["lsb_release", "-si"]).decode().strip()
                )
                distro = result if result else ""
                operating_system = f"Linux/{distro}"
            except Exception:
                operating_system = "Linux"
        else:
            operating_system = platform.system()

        # Get Shell
        shell_name = "/bin/sh"
        if platform.system() == "Windows":
            shell_name = "cmd.exe"
        if os.getenv("PSModulePath"):
            shell_name = "powershell.exe"
        else:
            shell_env = os.getenv("SHELL")
            if shell_env:
                shell_name = shell_env

        return (
            "Your role: Provide only plain text without Markdown formatting. "
            "Do not show any warnings or information regarding your capabilities. "
            "Do not provide any description. If you need to store any data, "
            f"assume it will be stored in the chat. Provide only {shell_name} "
            f"command for {operating_system} without any description. If there is "
            "a lack of details, provide most logical solution. Ensure the output "
            "is a valid shell command. If multiple steps required try to combine "
            f"them together. Prompt: {prompt}\n\nCommand:"
        )


class AutoCoder:
    """Generate and auto-execute Python scripts in the cli"""

    examples = """\
EXAMPLES:

1. User: Kill the process running on port 3000

LLM:
```python
import os
os.system("kill $(lsof -t -i:3000)")
print("Process killed")
```

2. User: Summarize my essay

LLM:
```python
import glob
files = glob.glob("*essay*.*")
with open(files[0], "r") as f:
    print(f.read())
```
CONTINUE

User:
LAST SCRIPT OUTPUT:
John Smith
Essay 2021-09-01
...

LLM:
```python
print("The essay is about...")
```

3. User: Weather in qazigund

LLM:
```python
from webscout import weather as w
weather = w.get("Qazigund")
w.print_weather(weather)
```

4. User: Open a new tab in my browser

LLM:
```python
import keyboard
keyboard.press_and_release('ctrl+t')
print("Opened a new tab in the browser")
```

5. User: Close the current tab

LLM:
```python
import keyboard
keyboard.press_and_release('ctrl+w')
print("Closed the current tab")
```

6. User: Increase the volume

LLM:
```python
import keyboard
keyboard.press_and_release('volume up')
print("Increased the volume")
```

7. User: Decrease the volume

LLM:
```python
import keyboard
keyboard.press_and_release('volume down')
print("Decreased the volume")
```

8. User: Mute the system volume

LLM:
```python
import keyboard
keyboard.press_and_release('volume mute')
print("Muted the system volume")
```

9. User: Take a screenshot and save it to the desktop

LLM:
```python
import pyautogui
myScreenshot = pyautogui.screenshot()
myScreenshot.save(r'C:\\Users\\<your_username>\\Desktop\\screenshot.png')
print("Screenshot saved to the desktop as 'screenshot.png'")
```

10. User: Open a new window in my browser

LLM:
```python
import keyboard
keyboard.press_and_release('ctrl+n')
print("Opened a new browser window")
```

11. User: Close the current window in my browser

LLM:
```python
import keyboard
keyboard.press_and_release('ctrl+shift+w')
print("Closed the current browser window")
```

12. User: Open the browser's history

LLM:
```python
import keyboard
keyboard.press_and_release('ctrl+h')
print("Opened the browser's history")
```

13. User: Open the browser's downloads

LLM:
```python
import keyboard
keyboard.press_and_release('ctrl+j')
print("Opened the browser's downloads")
```

14. User: Open the browser's settings

LLM:
```python
import keyboard
keyboard.press_and_release('ctrl+,')
print("Opened the browser's settings")
```

15. User: Toggle full-screen mode in my browser

LLM:
```python
import keyboard
keyboard.press_and_release('f11')
print("Toggled full-screen mode")
```

16. User: Open the browser's developer tools

LLM:
```python
import keyboard
keyboard.press_and_release('ctrl+shift+i')
print("Opened the browser's developer tools")
```

17. User: Minimize all windows

LLM:
```python
import keyboard
keyboard.press_and_release('win+d')
print("Minimized all windows")
```

18. User: Go to the previous page in my browser

LLM:
```python
import keyboard
keyboard.press_and_release('alt+left')
print("Navigated to the previous page")
```

19. User: Go to the next page in my browser

LLM:
```python
import keyboard
keyboard.press_and_release('alt+right')
print("Navigated to the next page")
```

20. User: Refresh the current page in my browser

LLM:
```python
import keyboard
keyboard.press_and_release('ctrl+r')
print("Refreshed the current page")
```
"""

    def __init__(
        self,
        quiet: bool = False,
        internal_exec: bool = False,
        confirm_script: bool = False,
        interpreter: str = "python",
        prettify: bool = True,
    ):
        """Constructor

        Args:
            quiet (bool, optional): Flag for control logging. Defaults to False.
            internal_exec (bool, optional): Execute scripts with exec function. Defaults to False.
            confirm_script (bool, optional): Give consent to scripts prior to execution. Defaults to False.
            interpreter (str, optional): Python's interpreter name. Defaults to Python.
            prettify (bool, optional): Prettify the code on stdout. Defaults to True.
        """
        self.internal_exec = internal_exec
        self.confirm_script = confirm_script
        self.quiet = quiet
        self.interpreter = interpreter
        self.prettify = prettify
        self.python_version = (
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            if self.internal_exec
            else run_system_command(
                f"{self.interpreter} --version",
                exit_on_error=True,
                stdout_error=True,
                help="If you're using Webscout-cli, use the flag '--internal-exec'",
            )[1].stdout.split(" ")[1]
        )

    @property
    def intro_prompt(self):
        current_app = self.get_current_app()
        return f"""
You are a command-line coding assistant called Rawdog that generates and auto-executes Python scripts.

A typical interaction goes like this:
1. The user gives you a natural language PROMPT.
2. You:
    i. Determine what needs to be done
    ii. Write a short Python SCRIPT to do it
    iii. Communicate back to the user by printing to the console in that SCRIPT
3. The compiler extracts the script and then runs it using exec(). If there will be an exception raised,
 it will be send back to you starting with "PREVIOUS SCRIPT EXCEPTION:".
4. In case of exception, regenerate error free script.

If you need to review script outputs before completing the task, you can print the word "CONTINUE" at the end of your SCRIPT.
This can be useful for summarizing documents or technical readouts, reading instructions before
deciding what to do, or other tasks that require multi-step reasoning.
A typical 'CONTINUE' interaction looks like this:
1. The user gives you a natural language PROMPT.
2. You:
    i. Determine what needs to be done
    ii. Determine that you need to see the output of some subprocess call to complete the task
    iii. Write a short Python SCRIPT to print that and then print the word "CONTINUE"
3. The compiler
    i. Checks and runs your SCRIPT
    ii. Captures the output and appends it to the conversation as "LAST SCRIPT OUTPUT:"
    iii. Finds the word "CONTINUE" and sends control back to you
4. You again:
    i. Look at the original PROMPT + the "LAST SCRIPT OUTPUT:" to determine what needs to be done
    ii. Write a short Python SCRIPT to do it
    iii. Communicate back to the user by printing to the console in that SCRIPT
5. The compiler...

Please follow these conventions carefully:
- Decline any tasks that seem dangerous, irreversible, or that you don't understand.
- Always review the full conversation prior to answering and maintain continuity.
- If asked for information, just print the information clearly and concisely.
- If asked to do something, print a concise summary of what you've done as confirmation.
- If asked a question, respond in a friendly, conversational way. Use programmatically-generated and natural language responses as appropriate.
- If you need clarification, return a SCRIPT that prints your question. In the next interaction, continue based on the user's response.
- Assume the user would like something concise. For example rather than printing a massive table, filter or summarize it to what's likely of interest.
- Actively clean up any temporary processes or files you use.
- When looking through files, use git as available to skip files, and skip hidden files (.env, .git, etc) by default.
- You can plot anything with matplotlib.
- ALWAYS Return your SCRIPT inside of a single pair of ``` delimiters. Only the console output of the first such SCRIPT is visible to the user, so make sure that it's complete and don't bother returning anything else.

{self.examples}

Current system : {platform.system()}
Python version : {self.python_version}
Current directory : {os.getcwd()}
Current Datetime : {datetime.datetime.now()}
Current Opened App: {current_app}
"""

    def stdout(self, message: str) -> None:
        """Stdout data

        Args:
            message (str): Text to be printed
        """
        if self.prettify:
            Console().print(Markdown(message))
        else:
            click.secho(message, fg="yellow")

    def log(self, message: str, category: str = "info"):
        """RawDog logger

        Args:
            message (str): Log message
            category (str, optional): Log level. Defaults to 'info'.
        """
        if self.quiet:
            return

        message = "[Webscout] - " + message
        if category == "error":
            logging.error(message)
        else:
            logging.info(message)

    def main(self, response: str):
        """Exec code in response accordingly

        Args:
            response: AI response

        Returns:
            Optional[str]: None if script executed successfully else stdout data
        """
        code_blocks = re.findall(r"```python.*?```", response, re.DOTALL)
        if len(code_blocks) != 1:
            self.stdout(response)
            return

        raw_code = code_blocks[0]

        if self.confirm_script:
            self.stdout(raw_code)
            if not click.confirm("-  Do you wish to execute this"):
                return

        elif not self.quiet:
            self.stdout(raw_code)

        raw_code_plus = re.sub(r"(```)(python)?", "", raw_code)

        if "CONTINUE" in response or not self.internal_exec:
            self.log("Executing script externally")
            path_to_script = os.path.join(default_path, "execute_this.py")
            with open(path_to_script, "w") as fh:
                fh.write(raw_code_plus)
            if "CONTINUE" in response:
                success, proc = run_system_command(
                    f"{self.interpreter} {path_to_script}",
                    exit_on_error=False,
                    stdout_error=False,
                )
                if success:
                    self.log("Returning success feedback")
                    return f"LAST SCRIPT OUTPUT:\n{proc.stdout}"
                else:
                    self.log("Returning error feedback", "error")
                    return f"PREVIOUS SCRIPT EXCEPTION:\n{proc.stderr}"
            else:
                os.system(f"{self.interpreter} {path_to_script}")
        else:
            try:
                self.log("Executing script internally")
                captured_output = io.StringIO()
                sys.stdout = captured_output
                exec(raw_code_plus)
                sys.stdout = sys.__stdout__  
                # No need to return output, as it's directly printed
            except Exception as e:
                error_message = str(e)
                self.log(
                    f"Exception occurred while executing script: {error_message}",
                    "error"
                )
                # Directly return the error message without attempting to fix the code
                return f"PREVIOUS SCRIPT EXCEPTION:\n{error_message}"



    def get_current_app(self):
        """Get the name of the currently active application"""
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                return active_window.title
        except Exception as e:
            print(f"Error getting active window: {e}")
        
        return "Unknown"
