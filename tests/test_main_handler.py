import pytest
from pytest_mock import MockerFixture

from lib.main_handler import Section, UserConfig, get_final_results
from lib.section import SectionTypes


@pytest.fixture
def mock_analyzers(mocker: MockerFixture) -> None:
    # Mock each analyze function to return a predefined list of Section objects
    mocker.patch('lib.main_handler.quality_analyzer.analyze', return_value=[Section(0, 0, '', SectionTypes.quality)])
    mocker.patch('lib.main_handler.text_analyzer.analyze', return_value=[Section(0, 0, '', SectionTypes.quality)])
    mocker.patch('lib.main_handler.transcript_analyzer.analyze', return_value=[Section(0, 0, '', SectionTypes.quality)])
    mocker.patch('lib.main_handler.video_analyzer.analyze', return_value=[Section(0, 0, '', SectionTypes.quality)])

def test_get_final_results(mock_analyzers: None) -> None:
    user_config = UserConfig(lang="en", platform="web")
    file_path = "path/to/file"

    results = get_final_results(file_path, user_config)

    # Check that the result is a list of Section objects
    for section in results:
        assert isinstance(section, Section)
    # Additional checks can include the length of the results list,
    # the contents of the Section objects, etc.
