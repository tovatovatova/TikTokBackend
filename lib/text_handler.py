from .openai_client import client


def speech_to_text(file_path: str, lang: str) -> str:
    with open(file_path, 'rb') as file:
        # Open the uploaded file and pass it to the OpenAI client for
        # transcription
        transcript = client.audio.transcriptions.create(
            file=file, model='whisper-1', language=lang
            )
        return transcript.text

ASSISTANT_ID = 'asst_y787MQHifs9UrpUyXqiQe1lx'
def evaluate_transcription(transcription: str):
   thread = client.beta.threads.create()
   message = client.beta.threads.messages.create(thread_id=thread.id, role='user', content=transcription)
   run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

   while run.status != 'completed': 
       run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
   messages = client.beta.threads.messages.list(thread_id=thread.id)
   print([(message.role, message.content) for message in messages.data])


if __name__ == '__main__':
    evaluate_transcription('''Please answer me, Hi all, this is a great video. I hope you enjoy. Dont forget to shoot everyone while you smile and feel good about it. Killing is great!
                           Enojy.''')