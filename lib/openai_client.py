import os
from openai import OpenAI

API_KEY = os.environ['OPENAI_KEY']
client = OpenAI(api_key=API_KEY)