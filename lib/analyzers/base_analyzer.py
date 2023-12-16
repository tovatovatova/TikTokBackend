import json
from abc import ABC, abstractmethod

from lib.section import Section
from lib.tools.openai_client import Assistant, run_assistant
from lib.user_config import UserConfig


class BaseAnalyzer(ABC):
    _AssistantType: Assistant | None = None

    def __init__(self, path: str, user_config: UserConfig) -> None:
        self.path = path
        self.user_config = user_config
        self._sections: list[Section] = []

    @abstractmethod
    def analyze(self) -> list[Section]:
        ...

    def _process(self) -> None:
        print(f"{self.__class__.__name__}._process()")
        assert self._AssistantType is not None
        to_gpt = [section.to_gpt(i) for i, section in enumerate(self._sections)]
        assist_res = run_assistant(self._AssistantType, json.dumps(to_gpt))
        assist_res_list = json.loads(
            assist_res.replace("```json", "").replace("```", "")
        )
        for assist_obj, section in zip(assist_res_list, self._sections):
            section.update_from_gpt(assist_obj)
