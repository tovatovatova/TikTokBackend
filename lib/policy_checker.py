import json
from .openai_client import client
from .policy_from_tiktok import POLICY


def check_policy(text_to_check: str, policy: str = POLICY):

    PROMPT_MESSAGES = [{
        "role": "user", "content": ["""
                                    You are an expert in analyzing video transcriptions and assessing their fit for being posted on different social medias. You have access to a policy file, describing in details the all the policies.
                                    The user's msg will be the entire video transcription text. Please go over the transcritopn and assess it against the policy files you have. The result should be a json with two keys, one being the "score" of the entire transcript (1 to 10) and the other being an "details" array with, each element neing a "word" and "reason" pair. Here is an example - { "score": 7, "details": [{ "word": "Kill", "reason": "Killing is a bad action" }]}. Of course, the reason should be taken from the policy file.
                                    Trust the use that his msg is exactly the video transcription text and head right away to analyze it.""",
            policy[:5000], text_to_check],
    }, ]
    params = {
        "model": "gpt-4-vision-preview", "messages": PROMPT_MESSAGES,
        "max_tokens": 200,
    }

    result = client.chat.completions.create(**params)
    return json.loads(result.choices[0].message.content)