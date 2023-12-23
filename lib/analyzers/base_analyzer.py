import json
import re
from abc import ABC, abstractmethod
from pathlib import Path

from lib.section import Section, SectionTypes, Status
from lib.tools.openai_client import Assistant, run_assistant
from lib.user_config import UserConfig


class BaseAnalyzer(ABC):
    _AssistantType: Assistant | None = None
    SectionType: SectionTypes | None = None

    def __init__(self, user_config: UserConfig) -> None:
        # TODO: Validate user config?
        self.user_config = user_config

    def analyze(self, file_path: Path) -> list[Section]:
        assert self.SectionType is not None
        try:
            sections = self._prepare_sections(file_path)
        except Exception as e:
            return self._analyzer_failure_err("prepare sections failed", e)

        # TODO: Validate sections structure?

        try:
            processed_sections = self.__process_sections(sections)
        except Exception as e:
            return self._analyzer_failure_err("process sections failed", e)

        try:
            final_sections = self._post_process_sections(processed_sections)
        except Exception as e:
            return self._analyzer_failure_err("post sections failed", e)

        return final_sections

    def _analyzer_failure_err(self, description: str, e: Exception) -> list[Section]:
        assert self.SectionType is not None
        return [
            Section(0, 0, description, self.SectionType, status=Status.error, error=e)
        ]

    def __process_sections(self, sections: list[Section]) -> list[Section]:
        assert self._AssistantType is not None
        to_gpt = [section.to_gpt(i) for i, section in enumerate(sections)]
        assist_res = run_assistant(self._AssistantType, json.dumps(to_gpt))
        assist_res_list = json.loads(self._extract_json_str(assist_res))
        for assist_obj, section in zip(assist_res_list, sections):
            section.update_from_gpt(assist_obj)

        return sections

    @abstractmethod
    def _prepare_sections(self, file_path: Path) -> list[Section]:
        ...

    def _post_process_sections(self, sections: list[Section]) -> list[Section]:
        return sections

    @staticmethod
    def _extract_json_str(string_response: str) -> str:
        ret = string_response
        ret = re.sub(r".*```json", "", ret, re.DOTALL)
        ret = re.sub(r"```.*", "", ret, re.DOTALL)
        return ret
