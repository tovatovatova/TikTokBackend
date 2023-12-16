import json
from abc import ABC, abstractmethod

from lib.section import Section
from lib.tools.openai_client import Assistant, run_assistant
from lib.user_config import UserConfig


class BaseAnalyzer(ABC):
    _AssistantType: Assistant | None = None

    def __init__(self, user_config: UserConfig) -> None:
        # TODO: Validate user config?
        self.user_config = user_config

    def analyze(self, file_path: str) -> list[Section]:
        sections = self._prepare_sections(file_path)
        # TODO: Validate sections structure?

        processed_sections = self.__process_sections(sections)
        final_sections = self._post_process_sections(processed_sections)
        return final_sections

    def __process_sections(self, sections: list[Section]) -> list[Section]:
        assert self._AssistantType is not None
        to_gpt = [section.to_gpt(i) for i, section in enumerate(sections)]
        assist_res = run_assistant(self._AssistantType, json.dumps(to_gpt))
        assist_res_list = json.loads(self._extract_json_str(assist_res))
        for assist_obj, section in zip(assist_res_list, sections):
            section.update_from_gpt(assist_obj)

        return sections

    @abstractmethod
    def _prepare_sections(self, file_path: str) -> list[Section]:
        ...

    def _post_process_sections(self, sections: list[Section]) -> list[Section]:
        return sections

    @staticmethod
    def _extract_json_str(string_response: str) -> str:
        return string_response.replace("```json", "").replace("```", "")
