from lib.openai_client import client


def speech_to_text(file_path: str, lang: str) -> str:
    with open(file_path, 'rb') as file:
        # Open the uploaded file and pass it to the OpenAI client for
        # transcription
        transcript = client.audio.transcriptions.create(
            file=file, model='whisper-1', language=lang
            )
        return transcript.text
