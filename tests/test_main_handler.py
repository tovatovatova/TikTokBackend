from unittest.mock import Mock, create_autospec

import pytest
from pytest_mock import MockerFixture

from lib.analyzers import AllAnalyzers
from lib.main_handler import get_final_results
from lib.section import Section
from lib.user_config import UserConfig


@pytest.fixture
def mock_analyzers(mocker: MockerFixture):
    # Mock each analyzer class and its analyze method
    for Analyzer in AllAnalyzers:
        mock_analyzer = create_autospec(Analyzer, instance=True)
        mock_analyzer.analyze.return_value = [Mock(spec=Section)]
        mocker.patch.object(Analyzer, "__init__", return_value=None)
        mocker.patch.object(Analyzer, "analyze", mock_analyzer.analyze)


def test_get_final_results(mock_analyzers: None) -> None:
    user_config = UserConfig(lang="en", platform="web")
    file_path = "path/to/file"

    results = get_final_results(file_path, user_config)

    # Check that the result is a list of Section objects
    for section in results:
        assert isinstance(section, Section)
    # Additional checks can include the length of the results list,
    # the contents of the Section objects, etc.
