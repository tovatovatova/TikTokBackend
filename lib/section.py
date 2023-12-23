from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class SectionTypes(str, Enum):
    video = "video"
    transcript = "transcript"
    text = "text"
    quality = "quality"


class Status(str, Enum):
    error = "error"
    success = "success"
    processing = "processing"
    created = "created"


@dataclass
class Section:
    start: float
    end: float
    info: str
    type: SectionTypes
    score: int | None = None
    reason: str | None = None
    status: Status = Status.created
    error: Exception | None = None

    def to_gpt(self, index: int) -> dict[str, Any]:
        assert (
            self.reason is None and self.score is None and self.status == Status.created
        )
        self.status = Status.processing
        return {
            "idx": index,
            "info": self.info,
            "score": self.score,
            "reason": self.reason,
        }

    def update_from_gpt(self, gpt_response: dict[str, Any]) -> None:
        try:
            # TODO: Parsing Error handling
            assert isinstance(
                gpt_response["score"], int
            ), f'expected gpt_response["score"] to be type int but got `{type(gpt_response["score"])}`'
            assert isinstance(
                gpt_response["reason"], str
            ), f'expected gpt_response["reason"] to be type int but got `{type(gpt_response["reason"])}`'
            self.score = gpt_response["score"]
            self.reason = gpt_response["reason"]
            self.status = Status.success
        except Exception as e:
            self.status = Status.error
            self.error = e

    def get_error_str(self) -> str | None:
        if self.error is None:
            return None
        return f"error-type: {type(self.error)} args: {self.error.args}"

    def to_jsonable(self) -> dict[str, Any]:
        self_dict = asdict(self)
        self_dict["error"] = self.get_error_str()
        return self_dict


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
