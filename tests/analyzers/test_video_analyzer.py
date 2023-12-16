import json

import pytest
from pytest_mock import MockerFixture

from lib.analyzers import VideoAnalyzer
from lib.user_config import UserConfig


@pytest.fixture
def mock_openai(mocker: MockerFixture) -> None:
    """Mock the openai_client so it won't really send requests to openai"""
    image_return_message = [
        {
            "info": "In This Scene the owner of a store yelling at a child to leave the store",
            "idx": 1,
        }
    ]
    mocker.patch(
        "lib.analyzers.video_analyzer.send_images",
        return_value=json.dumps(image_return_message),
    )
    assist_return_message = [
        {
            "info": image_return_message[0]["info"],
            "score": 6,
            "reason": "Yelling is bad..",
        }
    ]
    mocker.patch(
        "lib.analyzers.base_analyzer.run_assistant",
        return_value=json.dumps(assist_return_message),
    )


def test_analyze(mock_openai: None) -> None:
    path = "./frames/test-20.mp4"
    user_config = UserConfig(lang="en", platform="web")
    sections = VideoAnalyzer(path, user_config).analyze()
    for section in sections:
        assert section.processed
