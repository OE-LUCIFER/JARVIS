import concurrent.futures as cf

import os

import wave
from pathlib import Path
from typing import List, Literal, Optional, Generator

from pydantic import BaseModel, ValidationError
import requests
from loguru import logger
from pypdf import PdfReader


import requests
import json
from pathlib import Path
from typing import Generator
from playsound import playsound
from webscout import exceptions
from webscout.AIbase import TTSProvider
from tenacity import retry, stop_after_attempt, wait_fixed
from webscout import (
    Julius, 
)


INSTRUCTION_TEMPLATES = {
    "podcast (English)": {
        "intro": """Your task is to take the input text provided and turn it into a lively, engaging, informative podcast dialogue, in the style of NPR.  The input text may be messy or unstructured, as it could come from a variety of sources like PDFs or web pages.

Don't worry about formatting issues or irrelevant information; your goal is to extract the key points, identify definitions, and interesting facts that could be discussed in a podcast.

Define all terms used carefully for a broad audience of listeners.
""",
        "text_instructions": "First, carefully read through the input text and identify the main topics, key points, and any interesting facts or anecdotes. Think about how you could present this information in a fun, engaging way that would be suitable for a high-quality presentation.",
        "scratch_pad": """Brainstorm creative ways to discuss the main topics and key points you identified in the input text. Consider using analogies, examples, storytelling techniques, or hypothetical scenarios to make the content more relatable and engaging for listeners.

Keep in mind that your podcast should be accessible to a general audience, so avoid using too much jargon or assuming prior knowledge of the topic. If necessary, think of ways to briefly explain any complex concepts in simple terms.

Use your imagination to fill in any gaps in the input text or to come up with thought-provoking questions that could be explored in the podcast. The goal is to create an informative and entertaining dialogue, so feel free to be creative in your approach.

Define all terms used clearly and spend effort to explain the background.

Write your brainstorming ideas and a rough outline for the podcast dialogue here. Be sure to note the key insights and takeaways you want to reiterate at the end.

Make sure to make it fun and exciting.
""",
        "prelude": """Now that you have brainstormed ideas and created a rough outline, it's time to write the actual podcast dialogue. Aim for a natural, conversational flow between the host and any guest speakers. Incorporate the best ideas from your brainstorming session and make sure to explain any complex topics in an easy-to-understand way.
""",
        "dialog": """Write a very long, engaging, informative podcast dialogue here, based on the key points and creative ideas you came up with during the brainstorming session. Use a conversational tone and include any necessary context or explanations to make the content accessible to a general audience.

Never use made-up names for the hosts and guests, but make it an engaging and immersive experience for listeners. Do not include any bracketed placeholders like [Host] or [Guest]. Design your output to be read aloud -- it will be directly converted into audio.

Make the dialogue as long and detailed as possible, while still staying on topic and maintaining an engaging flow. Aim to use your full output capacity to create the longest podcast episode you can, while still communicating the key information from the input text in an entertaining way.

At the end of the dialogue, have the host and guest speakers naturally summarize the main insights and takeaways from their discussion. This should flow organically from the conversation, reiterating the key points in a casual, conversational manner. Avoid making it sound like an obvious recap - the goal is to reinforce the central ideas one last time before signing off.

The podcast should have around 20000 words.
""",
    },
    "podcast (Hindi)": {  # Hindi version remains the same
        "intro": """आपका कार्य दिए गए इनपुट टेक्स्ट को लेकर उसे एक जीवंत, आकर्षक और जानकारीपूर्ण पॉडकास्ट वार्तालाप में बदलना है, NPR की शैली में। इनपुट टेक्स्ट असंगठित या अव्यवस्थित हो सकता है, क्योंकि यह विभिन्न स्रोतों जैसे PDFs या वेब पेजों से आ सकता है।

फ़ॉर्मेटिंग समस्याओं या अप्रासंगिक जानकारी की चिंता न करें; आपका उद्देश्य मुख्य बिंदुओं को निकालना, परिभाषाओं और दिलचस्प तथ्यों को पहचानना है जिन्हें पॉडकास्ट में चर्चा की जा सकती है।

सभी उपयोग किए गए शब्दों को सावधानीपूर्वक व्यापक दर्शकों के लिए परिभाषित करें।
""",
        "text_instructions": "सबसे पहले, इनपुट टेक्स्ट को ध्यान से पढ़ें और मुख्य विषयों, प्रमुख बिंदुओं और किसी भी दिलचस्प तथ्य या उपाख्यानों की पहचान करें। इस जानकारी को प्रस्तुत करने के बारे में सोचें कि आप इसे एक मज़ेदार, आकर्षक तरीके से कैसे प्रस्तुत कर सकते हैं जो उच्च गुणवत्ता वाली प्रस्तुति के लिए उपयुक्त हो।",
        "scratch_pad": """मुख्य विषयों और प्रमुख बिंदुओं पर चर्चा करने के रचनात्मक तरीकों के बारे में सोचें जिन्हें आपने इनपुट टेक्स्ट में पहचाना है। उदाहरणों, कहानियों की तकनीकों, या काल्पनिक परिदृश्यों का उपयोग करके सामग्री को श्रोताओं के लिए अधिक सम्बंधित और आकर्षक बनाने पर विचार करें।

ध्यान रखें कि आपका पॉडकास्ट एक सामान्य दर्शक के लिए सुलभ होना चाहिए, इसलिए बहुत अधिक तकनीकी शब्दजाल से बचें या यह न मानें कि विषय का पूर्व ज्ञान है। यदि आवश्यक हो, तो किसी भी जटिल अवधारणा को सरल शब्दों में संक्षेप में समझाने के तरीकों के बारे में सोचें।

अपनी कल्पना का उपयोग करके इनपुट टेक्स्ट में किसी भी अंतराल को भरें या पॉडकास्ट में खोजे जा सकने वाले विचारोत्तेजक सवालों के साथ आएं। उद्देश्य एक जानकारीपूर्ण और मनोरंजक वार्तालाप बनाना है, इसलिए अपने दृष्टिकोण में रचनात्मक होने से न डरें।

सभी उपयोग किए गए शब्दों को स्पष्ट रूप से परिभाषित करें और पृष्ठभूमि समझाने के लिए समय दें।

यहां अपने विचार-मंथन और पॉडकास्ट वार्तालाप के लिए एक मोटा खाका लिखें। सुनिश्चित करें कि आपने उन प्रमुख अंतर्दृष्टियों और निष्कर्षों को नोट किया है जिन्हें आप अंत में दोहराना चाहते हैं।

इसे मजेदार और रोमांचक बनाएं।
""",
        "prelude": """अब जब आपने विचार-मंथन किया है और एक मोटा खाका तैयार कर लिया है, तो वास्तविक पॉडकास्ट वार्तालाप लिखने का समय आ गया है। होस्ट और किसी भी अतिथि वक्ता के बीच एक स्वाभाविक, संवादात्मक प्रवाह की दिशा में कार्य करें। अपने विचार-मंथन सत्र से सर्वश्रेष्ठ विचारों को शामिल करें और सुनिश्चित करें कि किसी भी जटिल विषय को आसानी से समझ में आने वाले तरीके से समझाया जाए।
""",
        "dialog": """यहां एक बहुत लंबा, आकर्षक और जानकारीपूर्ण पॉडकास्ट वार्तालाप लिखें, जो उन प्रमुख बिंदुओं और रचनात्मक विचारों पर आधारित हो जो आपने विचार-मंथन सत्र के दौरान बनाए थे। एक संवादात्मक शैली का उपयोग करें और सामग्री को एक सामान्य दर्शक के लिए सुलभ बनाने के लिए किसी भी आवश्यक संदर्भ या व्याख्याएं शामिल करें।

होस्ट और अतिथि वक्ताओं के लिए कभी भी काल्पनिक नामों का उपयोग न करें, बल्कि श्रोताओं के लिए इसे एक आकर्षक और immersive अनुभव बनाएं। किसी भी प्रकार के ब्रैकेटेड प्लेसहोल्डर्स जैसे [होस्ट] या [अतिथि] को शामिल न करें। अपनी आउटपुट को इस तरह डिज़ाइन करें कि इसे ज़ोर से पढ़ा जा सके – इसे सीधे ऑडियो में परिवर्तित किया जाएगा।

डायलॉग को यथासंभव लंबा और विस्तृत बनाएं, फिर भी विषय पर बने रहें और प्रवाह को आकर्षक बनाए रखें। अपनी पूरी आउटपुट क्षमता का उपयोग करते हुए यथासंभव लंबे पॉडकास्ट एपिसोड को बनाएं, जबकि फिर भी इनपुट टेक्स्ट से प्रमुख जानकारी को मनोरंजक तरीके से संप्रेषित करें।

वार्तालाप के अंत में, होस्ट और अतिथि वक्ता अपने चर्चा से स्वाभाविक रूप से मुख्य अंतर्दृष्टियों और निष्कर्षों को संक्षेप में प्रस्तुत करें। यह वार्तालाप से स्वाभाविक रूप से प्रवाहित होना चाहिए, अनौपचारिक, संवादात्मक तरीके से प्रमुख बिंदुओं को फिर से स्पष्ट करें। इसे स्पष्ट पुनरावृत्ति की तरह न बनाएं – उद्देश्य केंद्रीय विचारों को एक आखिरी बार सुदृढ़ करना है, इससे पहले कि वार्तालाप समाप्त हो जाए।

पॉडकास्ट में लगभग 20,000 शब्द होने चाहिए।
""",
    },
}


class Voicepods(TTSProvider):
    """
    A class to interact with the Voicepods text-to-speech API.
    """

    def __init__(self, timeout: int = 20, proxies: dict = None):
        """Initializes the Voicepods API client."""
        self.api_endpoint = "https://voicepods-stream.vercel.app/api/resemble"
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8',
            'Content-Type': 'application/json',
            'DNT': '1',
            'Origin': 'https://voicepods-stream.vercel.app',
            'Referer': 'https://voicepods-stream.vercel.app/',
            'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        if proxies:
            self.session.proxies.update(proxies)
        self.timeout = timeout
        self.audio_cache_dir = Path("./audio_cache")

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def tts(self, text: str, speaker: str = "speaker-1", line_number: int = 1) -> str:
        """
        Converts text to speech using the Voicepods API and saves it to a file with speaker and line number.

        Args:
            text (str): The text to be converted to speech.
            speaker (str, optional): The speaker identifier (speaker-1 or speaker-2). Defaults to "speaker-1".
            line_number (int, optional): The line number in the dialogue. Defaults to 1.

        Returns:
            str: The filename of the saved audio file.

        Raises:
            exceptions.FailedToGenerateResponseError: If there is an error generating or saving the audio.
        """
        payload = json.dumps({"query": text})
        filename = self.audio_cache_dir / f"{speaker}_{line_number}.wav"  # Speaker and line number in filename

        try:
            response = self.session.post(self.api_endpoint, data=payload, timeout=self.timeout)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            if "audio/wav" not in content_type.lower():
                raise ValueError(f"Unexpected content type: {content_type}")

            audio_data = response.content
            self._save_audio(audio_data, filename)
            return filename.as_posix()  # Return the filename as a string

        except requests.exceptions.RequestException as e:
            raise exceptions.FailedToGenerateResponseError(f"Error generating audio after multiple retries: {e}") from e
        except ValueError as e:
            raise exceptions.FailedToGenerateResponseError(f"Invalid audio data received from API: {e}") from e
        except Exception as e:
            raise exceptions.FailedToGenerateResponseError(f"An unexpected error occurred: {e}") from e

    def _save_audio(self, audio_data: bytes, filename: Path):
        """Saves the audio data to a WAV file in the audio cache directory."""
        try:
            self.audio_cache_dir.mkdir(parents=True, exist_ok=True)

            riff_start = audio_data.find(b'RIFF')
            if riff_start == -1:
                raise ValueError("RIFF header not found in audio data")

            trimmed_audio_data = audio_data[riff_start:]

            with open(filename, "wb") as f:
                f.write(trimmed_audio_data)

        except Exception as e:
            raise exceptions.FailedToGenerateResponseError(f"Error saving audio: {e}")

    def play_audio(self, filename: str):
        """
        Plays an audio file using playsound.

        Args:
            filename (str): The path to the audio file.

        Raises:
            RuntimeError: If there is an error playing the audio.
        """
        try:
            playsound(filename)
        except Exception as e:
            raise RuntimeError(f"Error playing audio: {e}")
        
class DialogueItem(BaseModel):
    text: str
    speaker: Literal["speaker-1", "speaker-2"]

class Dialogue(BaseModel):
    scratchpad: str
    dialogue: List[DialogueItem]


def update_instructions(template: str) -> tuple:
    return (
        INSTRUCTION_TEMPLATES[template]["intro"],
        INSTRUCTION_TEMPLATES[template]["text_instructions"],
        INSTRUCTION_TEMPLATES[template]["scratch_pad"],
        INSTRUCTION_TEMPLATES[template]["prelude"],
        INSTRUCTION_TEMPLATES[template]["dialog"],
    )


def extract_text_from_pdf(file_path: str) -> str:
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            text = "\n\n".join([page.extract_text() for page in reader.pages])
            return text
    except Exception as e:
        return f"Error reading PDF: {e}"


def generate_audio(
    files: List[str],
    llm_provider: Julius,  # webscout's LLM provider
    tts_provider: Voicepods,  # webscout's TTS provider
    template: str = "podcast (English)",
    debug: bool = False,
) -> tuple[Optional[str], str, str, str]:
    """Generates audio from PDF files using specified parameters."""

    try:
        combined_text = ""
        for file in files:
            combined_text += extract_text_from_pdf(file) + "\n\n"

        (
            intro_instructions,
            text_instructions,
            scratch_pad_instructions,
            prelude_dialog,
            podcast_dialog_instructions,
        ) = update_instructions(template)

        # Using webscout's LLM provider
        def generate_dialogue(text: str) -> str:
            """Generates dialogue using LLM"""
            try:
                return llm_provider.chat(
                    f"""{intro_instructions}
                    Here is the original input text:

                    <input_text>
                    {text}
                    </input_text>

                    {text_instructions}

                    <scratchpad>
                    {scratch_pad_instructions}
                    </scratchpad>

                    {prelude_dialog}

                    <podcast_dialogue>
                    {podcast_dialog_instructions}
                    </podcast_dialogue>
                    """,
                    stream=False,
                )
            except Exception as e:
                return f"Error generating dialogue: {e}"

        # Generate dialogue
        llm_output = generate_dialogue(combined_text)

        #Basic parsing - improve for production use
        try:
            dialogue_lines = [line.strip() for line in llm_output.splitlines() if line.strip()]
            dialogue = []
            for i, line in enumerate(dialogue_lines):
                speaker = "speaker-1" if i % 2 == 0 else "speaker-2"
                dialogue.append(DialogueItem(text=line, speaker=speaker))
            dialogue_object = Dialogue(scratchpad="", dialogue=dialogue)

        except ValidationError as e:
            return None, "", combined_text, f"Error parsing LLM output: {e}"
        except Exception as e:
            return None, "", combined_text, f"Error parsing LLM output: {e}"


        # Generate individual WAV files and store filenames
        wav_files = []
        with cf.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    tts_provider.tts, line.text, line.speaker, i + 1 
                )
                for i, line in enumerate(dialogue_object.dialogue)
            ]
            for future in cf.as_completed(futures):
                try:
                    wav_file = future.result()
                    wav_files.append(wav_file)
                except Exception as e:
                    return None, "", combined_text, f"Error generating audio: {e}"

        # Merge WAV files
        merged_audio_file = merge_wav_files(wav_files, "merged_podcast.wav")

        #Cleanup individual WAV files
        for wav_file in wav_files:
            os.remove(wav_file)

        transcript = "\n\n".join(
            [f"{line.speaker}: {line.text}" for line in dialogue_object.dialogue]
        )
        characters = sum([len(line.text) for line in dialogue_object.dialogue])
        logger.info(f"Generated {characters} characters of audio")

        return merged_audio_file, transcript, combined_text, None

    except Exception as e:
        return None, "", "", str(e)


def merge_wav_files(input_files: List[str], output_file: str) -> str:
    """Merges multiple WAV files into a single output WAV file."""
    data = []
    framerate = None

    for infile in input_files:
        with wave.open(infile, 'rb') as wf:
            if framerate is None:
                framerate = wf.getframerate()
                nchannels = wf.getnchannels()
                sampwidth = wf.getsampwidth()
            else:
                assert framerate == wf.getframerate(), "Mismatched frame rates"
                assert nchannels == wf.getnchannels(), "Mismatched channel counts"
                assert sampwidth == wf.getsampwidth(), "Mismatched sample widths"
            data.append(wf.readframes(wf.getnframes()))

    with wave.open(output_file, 'wb') as outfile:
        outfile.setnchannels(nchannels)
        outfile.setsampwidth(sampwidth)
        outfile.setframerate(framerate)
        outfile.writeframes(b''.join(data))

    return output_file


def main(
    files: List[str],
    llm_provider: Julius,
    tts_provider: Voicepods,
    template: str = "podcast (English)",
):
    """Main function to handle PDF to audio conversion."""

    audio_file, transcript, original_text, error = generate_audio(
        files, llm_provider, tts_provider, template
    )

    if audio_file:
        print(f"Audio saved to: {audio_file}")
        print(f"\nTranscript:\n{transcript}")
        print(f"\nOriginal Text:\n{original_text}")

    if error:
        print(f"Error: {error}")


if __name__ == "__main__":
    # Example usage (replace with your actual file paths)
    files = ["Aditya_L1_Booklet.pdf"]  # Replace with your file paths
    llm_provider = Julius(timeout=10000)  # Use Julius as the LLM provider
    tts_provider = Voicepods(timeout=10000)  # Use Voicepods as the TTS provider
    template = "podcast (English)"  # Choose your preferred language template

    main(files, llm_provider, tts_provider, template=template)