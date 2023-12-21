from pathlib import Path

from lib.analyzers.base_analyzer import BaseAnalyzer
from lib.section import Section
from lib.tools.gcloud_client import upload_video_and_extract_in_video_text
from lib.tools.openai_client import Assistant
from lib.user_config import UserConfig


class TextAnalyzer(BaseAnalyzer):
    _AssistantType = Assistant.Text

    def _prepare_sections(self, file_path: Path) -> list[Section]:
        return upload_video_and_extract_in_video_text(file_path)


if __name__ == "__main__":
    analyzer = TextAnalyzer(UserConfig("en", "tiktok"))
    print(analyzer.analyze(Path("./frames/test-20.mp4")))
