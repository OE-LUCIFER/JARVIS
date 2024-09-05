import logging
import os
import threading
import time
import webscout

HISTORY_FOLDER = "History"
if not os.path.exists(HISTORY_FOLDER):
    os.makedirs(HISTORY_FOLDER)


class JARVISConversation:
    """Handles prompt generation based on history, including memory"""

    intro = (
        "You are JARVIS, Vortex's highly advanced AI assistant."
        "Respond concisely with a mix of professionalism and subtle humor. "
        "Always prioritize Vortex's efficiency and well-being and use emojis and show emotion"
        "Always answer user based on tool result"
    )

    def __init__(
        self,
        status: bool = True,
        max_tokens: int = 8000,
        filepath: str = os.path.join(HISTORY_FOLDER, "JARVISConversation_history.txt"),
        memory_filepath: str = os.path.join(HISTORY_FOLDER, "memory.txt"),
        chat_filepath: str = os.path.join(HISTORY_FOLDER, "chat.txt"),
        update_file: bool = True,
    ):
        
        self.status = status
        self.max_tokens_to_sample = max_tokens
        self.chat_history = self.intro + "\n"  # Add a newline after intro
        self.history_format = "\n%(role)s: %(content)s"
        self.file = filepath
        self.update_file = update_file
        self.history_offset = 10250
        self.prompt_allowance = 10
        self.memory_filepath = memory_filepath
        self.chat_filepath = chat_filepath
        self.memory = self.load_memory(memory_filepath)
        self.load_JARVISConversation(filepath, False)

        # Initialize 5-minute chat saving and summarization
        self.chat_buffer = []
        self.last_save_time = 0
        self.save_interval = 300  # 5 minutes in seconds
        self.summarization_thread = threading.Thread(target=self.summarize_and_save_chat)
        self.summarization_thread.daemon = True
        self.summarization_thread.start()

    def load_JARVISConversation(self, filepath: str, exists: bool = True) -> None:
        if not os.path.isfile(filepath):
            logging.debug(f"Creating new chat-history file - '{filepath}'")
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write(self.intro)
        else:
            logging.debug(f"Loading JARVISConversation from '{filepath}'")
            with open(filepath, encoding="utf-8") as fh:
                file_contents = fh.readlines()
                if file_contents:
                    self.intro = file_contents[0].strip()  # Remove newline from intro
                    self.chat_history = "\n".join(file_contents[1:])

    def load_memory(self, filepath: str) -> str:
        """Loads the memory from a file."""
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def __trim_chat_history(self, chat_history: str, intro: str) -> str:
        len_of_intro = len(intro)
        len_of_chat_history = len(chat_history)
        total = self.max_tokens_to_sample + len_of_intro + len_of_chat_history

        if total > self.history_offset:
            # Find the starting position of the second "User:" section
            first_user_index = chat_history.find("\nUser:")
            second_user_index = chat_history.find("\nUser:", first_user_index + 1)

            if second_user_index != -1:
                truncate_at = second_user_index + self.prompt_allowance
                trimmed_chat_history = chat_history[truncate_at:]
                return "... " + trimmed_chat_history
            else:
                return chat_history  # No second "User:" section found, don't trim
        else:
            return chat_history

    def gen_complete_prompt(self, prompt: str, intro: str = None) -> str:
        if self.status:
            intro = self.intro if intro is None else intro
            incomplete_chat_history = self.chat_history + self.history_format % dict(
                role="User", content=prompt
            )

            # Preserve Intro and Memory when trimming
            trimmed_history = self.__trim_chat_history(incomplete_chat_history, intro)
            
            # Add memory to the chat history using add_message
            self.add_message("Memory", self.memory)

            return intro + "\n" + trimmed_history  # Add newline after intro
        return prompt

    def update_chat_history(self, role: str, content: str, force: bool = False) -> None:
        if not self.status and not force:
            return
        new_history = self.history_format % dict(role=role, content=content)

        # Update chat.txt in real-time
        if self.chat_filepath and self.update_file:
            with open(self.chat_filepath, "a", encoding="utf-8") as fh:
                fh.write(new_history + "\n")

        if self.file and self.update_file:  # Update JARVISConversation_history.txt
            with open(self.file, "a", encoding="utf-8") as fh:
                fh.write(new_history + "\n")

        self.chat_history += new_history
        self.chat_buffer.append(new_history)  # Update the buffer

    def add_message(self, role: str, content: str) -> None:
        self.update_chat_history(role, content)

    def summarize_and_save_chat(self):
        """Periodically summarizes and saves the chat buffer to memory."""
        while True:
            time.sleep(self.save_interval)
            current_time = time.time()
            if current_time - self.last_save_time >= self.save_interval:
                self.last_save_time = current_time
                if self.chat_buffer:
                    chat_summary = self.summarize_chat(self.chat_buffer)
                    self.save_memory(chat_summary)
                    self.chat_buffer = []  # Clear the buffer after saving

    def summarize_chat(self, chat_log: list) -> str:
        """Summarizes the chat log into a 100-word summary."""
        full_chat = "".join(chat_log)
        prompt = f"""
        You are a highly advanced AI assistant tasked with summarizing a conversation.
        Given the following conversation, create a concise summary, focusing on user requests, actions taken, and important information exchanged. 
        Limit your summary to 100 words. 

        Conversation:
        {full_chat}

        Summary:
        """
        ai = webscout.Julius(model="Gemini Flash", is_conversation=False, intro=None)
        summary = ai.chat(prompt)
        return "".join(summary).strip()  # Return the summary

    def save_memory(self, summary: str) -> None:
        """Saves the memory summary to the file."""
        with open(self.memory_filepath, "w", encoding="utf-8") as f:
            f.write(summary)
        self.memory = summary