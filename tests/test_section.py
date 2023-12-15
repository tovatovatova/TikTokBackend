import pytest

from lib.section import Section, SectionTypes


def test_section_initialization():
    section = Section(start=0.0, end=5.0, info="Example Info", type=SectionTypes.text)
    assert section.start == 0.0
    assert section.end == 5.0
    assert section.info == "Example Info"
    assert section.type == SectionTypes.text
    assert section.score is None
    assert section.reason is None
    assert section.processed == False


def test_section_to_gpt():
    section = Section(start=0.0, end=5.0, info="Example Info", type=SectionTypes.text)
    gpt_output = section.to_gpt(0)
    expected_output = {"info": "Example Info", "score": None, "reason": None, "idx": 0}
    assert gpt_output == expected_output


def test_section_update_from_gpt_valid():
    section = Section(start=0.0, end=5.0, info="Example Info", type=SectionTypes.text)
    gpt_response = {"score": 100, "reason": "Valid Reason"}
    section.update_from_gpt(gpt_response)

    assert section.score == 100
    assert section.reason == "Valid Reason"
    assert section.processed == True


def test_section_update_from_gpt_invalid():
    section = Section(start=0.0, end=5.0, info="Example Info", type=SectionTypes.text)
    gpt_response = {"score": "Invalid", "reason": 100}  # Invalid types

    with pytest.raises(AssertionError):
        section.update_from_gpt(gpt_response)
