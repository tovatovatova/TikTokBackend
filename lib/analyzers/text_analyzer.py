from lib.analyzers.base_analyzer import BaseAnalyzer
from lib.section import Section
from lib.tools.gcloud_client import upload_video_and_extract_in_video_text
from lib.tools.openai_client import Assistant
from lib.user_config import UserConfig


class TextAnalyzer(BaseAnalyzer):
    _AssistantType = Assistant.Text

    def analyze(self) -> list[Section]:
        self._sections = upload_video_and_extract_in_video_text(self.path)
        self._process()
        return self._sections


if __name__ == "__main__":
    analyzer = TextAnalyzer("./frames/test-20.mp4", UserConfig("en", "tiktok"))
    print(analyzer.analyze())
