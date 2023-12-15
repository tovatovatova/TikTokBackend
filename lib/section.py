from dataclasses import dataclass
from enum import Enum
from typing import Any


class SectionTypes(str, Enum):
    video = "video"
    transcript = "transcript"
    text = "text"
    quality = "quality"


@dataclass
class Section:
    start: float
    end: float
    info: str
    type: SectionTypes
    score: int | None = None
    reason: str | None = None
    processed: bool = False

    def to_gpt(self, index: int) -> dict[str, Any]:
        assert self.reason is None and self.score is None and self.processed == False
        return {
            "idx": index,
            "info": self.info,
            "score": self.score,
            "reason": self.reason,
        }

    def update_from_gpt(self, gpt_response: dict[str, Any]) -> None:
        # TODO: Parsing Error handling
        assert isinstance(gpt_response["score"], int)
        assert isinstance(gpt_response["reason"], str)
        self.score = gpt_response["score"]
        self.reason = gpt_response["reason"]
        self.processed = True


# @dataclass
# class Results:
#     sections: dict[int, Section]
#     errors: list[Exception]

#     def update_from_gpt(self, gpt_response: str) -> bool:
#         error = None
#         try:
#             gpt_response_list = json.loads(gpt_response)
#         except json.JSONDecodeError as e:
#             error = e
#         except pydantic.errors.PydanticUserError as e:
#             error = e
#         else:
#             for

#         if error:
#             self.errors.append(error)

#         return error is None

#     def to_json(self) -> str:
#         return json.dumps(self)
