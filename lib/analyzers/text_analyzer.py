import json

from lib.section import Section
from lib.tools.gcloud_client import upload_video_and_extract_in_video_text
from lib.tools.openai_client import Assistant, run_assistant
from lib.user_config import UserConfig


def analyze(path: str, user_config : UserConfig) -> list[Section]:
    sections = upload_video_and_extract_in_video_text(path)
    to_gpt = [section.to_gpt() for section in sections]
    assist_res = run_assistant(Assistant.Text, json.dumps(to_gpt))
    assist_res_list = json.loads(assist_res)
    for assist_obj, section in zip(assist_res_list, sections):
        section.update_from_gpt(assist_obj)
    return sections
