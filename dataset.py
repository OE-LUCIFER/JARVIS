import json
import os
import time
from typing import Dict, Any

DATA_FOLDER = "DATA"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

DATASET_FILE = os.path.join(DATA_FOLDER, "dataset.json")

class DatasetBuilder:
    def __init__(self, dataset_file=DATASET_FILE):
        self.dataset_file = dataset_file
        self.dataset = self.load_dataset()

    def load_dataset(self):
        """Loads the dataset from a JSON file."""
        if os.path.exists(self.dataset_file):
            with open(self.dataset_file, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"Error decoding {self.dataset_file}. Starting with an empty list.")
                    return []
        return []

    def save_dataset(self):
        """Saves the dataset to a JSON file."""
        with open(self.dataset_file, "w", encoding="utf-8") as f:
            json.dump(self.dataset, f, indent=2, ensure_ascii=False)

    def add_datapoint(
        self,
        instruction: str,
        input: str,
        tool_called: Dict[str, Any],
        tool_output: str,
        output: str
    ):
        """Appends a new datapoint to the dataset."""
        datapoint = {
            "instruction": instruction,
            "input": input,
            "TOOL Called": tool_called,  # Keep the same structure as TOOLS.py
            "TOOLoutput": tool_output,
            "output": output
        }
        self.dataset.append(datapoint)
        self.save_dataset()

    def print_dataset(self):
        """Prints the current dataset."""
        print(json.dumps(self.dataset, indent=2, ensure_ascii=False))

# Example usage
if __name__ == "__main__":
    builder = DatasetBuilder()

    instruction = "What's the weather like in London today?"
    input_text = ""
    tool_called = {
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
        }
    }
    tool_output = "The current weather in London is cloudy with a chance of rain. ☁️🌧️"
    output = "The weather in London today is cloudy with a chance of rain. ☁️🌧️"

    builder.add_datapoint(instruction, input_text, tool_called, tool_output, output)

    builder.print_dataset()