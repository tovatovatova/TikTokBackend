import re
from datetime import datetime

from lib.analyzers.base_analyzer import BaseAnalyzer
from lib.section import Section, SectionTypes
from lib.tools.openai_client import Assistant, speech_to_text_srt
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


class TranscriptAnalyzer(BaseAnalyzer):
    _AssistantType = Assistant.Transcript

    def analyze(self) -> list[Section]:
        transcription_srt = speech_to_text_srt(self.path, lang=self.user_config.lang)
        self._sections = _srt_to_sections(transcription_srt)
        self._process()
        return self._sections


if __name__ == "__main__":
    analyzer = TranscriptAnalyzer("./frames/test-20.mp4", UserConfig("en", "tiktok"))
    print(analyzer.analyze())
