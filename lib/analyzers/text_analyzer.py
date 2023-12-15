import json

from lib.section import Section
from lib.tools.gcloud_client import upload_video_and_extract_in_video_text
from lib.tools.openai_client import Assistant, run_assistant
from lib.user_config import UserConfig


def analyze(path: str, user_config : UserConfig) -> list[Section]:
    sections = upload_video_and_extract_in_video_text(path)
    to_gpt = [section.to_gpt(i) for i, section in enumerate(sections)]
    assist_res = run_assistant(Assistant.Text, json.dumps(to_gpt))
    assist_res_list = json.loads(assist_res.replace('```json', '').replace('```', ''))
    for assist_obj, section in zip(assist_res_list, sections):
        section.update_from_gpt(assist_obj)
    return sections

if __name__ == '__main__':
    print(analyze('./frames/test-20.mp4', UserConfig('en', 'tiktok')))
