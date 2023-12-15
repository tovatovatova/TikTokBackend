import json
import pytest
from pytest_mock import MockerFixture
from lib.analyzers import transcript_analyzer

from lib.user_config import UserConfig

@pytest.fixture
def mock_openai(mocker: MockerFixture) -> None:
    mocker.patch('lib.analyzers.transcript_analyzer.speech_to_text_srt', return_value="1\n00:00:01,000 --> 00:00:02,000\nHello World")
    mocker.patch('lib.analyzers.transcript_analyzer.run_assistant', return_value=json.dumps([{"info": "Hello World", "score": 5, "reason": "Good"}]))


def test_analyze(mock_openai: None) -> None:
    path = 'path/to/audio'
    user_config = UserConfig(lang="en", platform="web")
    sections = transcript_analyzer.analyze(path, user_config)

    # Assertions to validate the behavior of analyze function
    assert len(sections) == 1
    assert sections[0].score == 5
    assert sections[0].reason == "Good"