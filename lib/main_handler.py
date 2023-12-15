from lib.analyzers import (
    quality_analyzer,
    text_analyzer,
    transcript_analyzer,
    video_analyzer,
)
from lib.section import Section
from lib.user_config import UserConfig


def get_final_results(file_path: str, user_config: UserConfig) -> list[Section]:
    final_results: list[Section] = []
    final_results += transcript_analyzer.analyze(file_path, user_config)
    final_results += text_analyzer.analyze(file_path, user_config)
    final_results += quality_analyzer.analyze(file_path, user_config)
    final_results += video_analyzer.analyze(file_path, user_config)
    return final_results
