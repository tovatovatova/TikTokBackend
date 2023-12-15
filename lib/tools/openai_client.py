import os
from enum import Enum

from openai import OpenAI
from openai.types.beta.threads import MessageContentText
_API_KEY = os.environ['OPENAI_KEY']
client = OpenAI(api_key=_API_KEY)

class Assistant(str, Enum):
    Video = 'asst_sMzgIiUd5HPVckcoLkEbJkLg'
    Text = 'asst_Y6C3JudOf1MqHnPXSsme3ac5'
    Transcript = 'asst_kEeVh4jGxkn8vw67CcgCcf0b'

def run_assistant(assistant: Assistant, data: str) -> str:
    thread = client.beta.threads.create()
    _message = client.beta.threads.messages.create(thread_id=thread.id, role='user', content=data)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant)

    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    # unpacking like this so it's will error in case there is multiple
    assist_message, = (message.content for message in messages.data if message.role == 'assistant')
    content, = assist_message
    # asserting that this is a message content (which has the text attr not like in image content for example..)
    assert isinstance(content, MessageContentText)
    return content.text.value


def speech_to_text_srt(file_path: str, lang: str):
    with open(file_path, 'rb') as file:
        # Open the uploaded file and pass it to the OpenAI client for
        # transcription
        transcript = client.audio.transcriptions.create(
            file=file,
            model='whisper-1',
            language=lang,
            response_format='srt',
        )
        return str(transcript)


def send_images(base64_frames: list[str], prompt: str, format: str = 'image/jpeg') -> str:
    prompt_messages = [
        {
            "role": "user",
            # TODO: Something fishy about the type and structure of prompt_messages. Need to review and possible correct.
            #  See https://platform.openai.com/docs/guides/vision/uploading-base-64-encoded-images
            "content": [
                {'type': 'text', 'data': prompt},
                *({"type": 'image_url', 'image_url': f'data:{format};base64,{frame}'} for frame in base64_frames),
            ],
        },
    ]

    result = client.chat.completions.create(
        model='gpt-4-vision-preview',
        messages=prompt_messages,  # type: ignore
        max_tokens=200 # TODO: check if this is the optimal number (price and performance)
    )

    assert result.choices[0].message.content is not None

    return result.choices[0].message.content


if __name__ == '__main__':
    res = run_assistant(Assistant.Text, """[
    {
        "idx": 1,
        "text": "HAMAS PRODUCTION",
        "score": null,
        "reason": null
    },
    {
        "idx": 2,
        "text": "Now.",
        "score": null,
        "reason": null
    },
    {
        "idx": 3,
        "text": "Gently open the vehicle door.",
        "score": null,
        "reason": null
    },
    {
        "idx": 4,
        "text": "DIRECTOR'S CUT CWITH A KNIFE)",
        "score": null,
        "reason": null
    },
    {
        "idx": 5,
        "text": "TAKE 4",
        "score": null,
        "reason": null
    },
    {
        "idx": 6,
        "text": "HOSTAGE",
        "score": null,
        "reason": null
    },
    {
        "idx": 7,
        "text": "RELEASE",
        "score": null,
        "reason": null
    },
    {
        "idx": 8,
        "text": "PRESENTS:",
        "score": null,
        "reason": null
    }
]""")
    print()