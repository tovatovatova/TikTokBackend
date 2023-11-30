from lib.openai_client import client
from policy_from_tiktok import POLICY


def check_policy(text_to_check: str, policy: str = POLICY):

    PROMPT_MESSAGES = [{
        "role": "user", "content": [
            "The following request has 2 parameters. The first parameter is "
            "all statements in a policy's full detail. The second parameter "
            "is all the sentences in the context that we want to check "
            "according to the policy. You need to rate this with a number "
            "that represents how well the sentences in the context meet the "
            "policy on a scale of 1-10. When the sentence completely "
            "violates the policy, you must respond 1, when the sentences "
            "comply with the policy , you must respond 10, when it is an "
            "ambiguous number in the range. Don't ever answer with anything "
            "else but the number in the first line of your answer. The "
            "second answer should contain only the words from the second "
            "parameter that decreased the value, if there are any.",
            policy[:5000], text_to_check],
    }, ]
    params = {
        "model": "gpt-4-vision-preview", "messages": PROMPT_MESSAGES,
        "max_tokens": 200,
    }

    result = client.chat.completions.create(**params)
    return result.choices[0].message.content

# x = check_policy(
#     "Israel should be able to defend itself, and to kill terrorists"
# )
# print(x)
