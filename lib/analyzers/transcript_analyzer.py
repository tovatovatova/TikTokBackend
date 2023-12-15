import json
import re
from datetime import datetime

from lib.section import Section, SectionTypes
from lib.tools.openai_client import Assistant, run_assistant, speech_to_text_srt
from lib.user_config import UserConfig


def _srt_ts_to_seconds(ts: str) -> float:
    td = datetime.strptime(ts, "%H:%M:%S,%f") - datetime(1900, 1, 1)
    return td.total_seconds()


def _srt_to_sections(srt_text: str) -> list[Section]:
    # Splitting the text into blocks
    blocks = re.split(r"\n\n", srt_text.strip())

    # Parse each block
    sections: list[Section] = []
    for block in blocks:
        assert isinstance(block, str)
        lines = block.split("\n")
        _idx, times, *text = lines
        start, end = times.split(" --> ")
        sections.append(
            Section(
                info=" ".join(text),
                start=_srt_ts_to_seconds(start),
                end=_srt_ts_to_seconds(end),
                type=SectionTypes.transcript,
            )
        )
    return sections


def analyze(path: str, user_config: UserConfig) -> list[Section]:
    transcription_srt = speech_to_text_srt(path, lang=user_config.lang)
    sections = _srt_to_sections(transcription_srt)
    to_gpt = [section.to_gpt(i) for i, section in enumerate(sections)]
    assist_res = run_assistant(Assistant.Transcript, json.dumps(to_gpt))
    assist_res_list = json.loads(assist_res.replace("```json", "").replace("```", ""))
    for assist_obj, section in zip(assist_res_list, sections):
        section.update_from_gpt(assist_obj)
    return sections


if __name__ == "__main__":
    print(analyze("./frames/test-20.mp4", UserConfig("en", "tiktok")))
