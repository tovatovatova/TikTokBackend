from lib.analyzers.quality_analyzer import analyze as analyze_quality
from lib.analyzers.text_analyzer import analyze as analyze_text
from lib.analyzers.transcript_analyzer import analyze as analyze_transcript
from lib.analyzers.video_analyzer import analyze as analyze_video
from lib.section import Section
from lib.user_config import UserConfig


def get_final_results(file_path: str, user_config: UserConfig) -> list[Section]:
    final_results: list[Section] = []
    final_results += analyze_quality(file_path, user_config)
    final_results += analyze_text(file_path, user_config)
    final_results += analyze_transcript(file_path, user_config)
    final_results += analyze_video(file_path, user_config)
    return final_results
