import re
from datetime import datetime
from pathlib import Path

from moviepy.editor import VideoFileClip

from lib.analyzers.base_analyzer import BaseAnalyzer
from lib.section import Section, SectionTypes
from lib.tools.openai_client import Assistant, speech_to_text_srt
from lib.user_config import UserConfig


def _extract_and_save_audio(video_path: Path) -> Path:
    video = VideoFileClip(str(video_path))
    assert video.audio is not None
    audio_filename = video_path.name.split(".")[0] + "-audio.mp3"
    audio_path = video_path.parent / audio_filename
    video.audio.write_audiofile(audio_path)
    return audio_path


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
    SectionType = SectionTypes.transcript

    def _prepare_sections(self, file_path: Path) -> list[Section]:
        audio_path = _extract_and_save_audio(file_path)
        transcription_srt = speech_to_text_srt(audio_path, lang=self.user_config.lang)
        sections = _srt_to_sections(transcription_srt)
        return sections


if __name__ == "__main__":
    analyzer = TranscriptAnalyzer(UserConfig("en", "tiktok"))
    print(analyzer.analyze(Path("./frames/test-20.mp4")))
