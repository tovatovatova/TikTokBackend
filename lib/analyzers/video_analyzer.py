import base64
import json

import cv2

from lib.analyzers.base_analyzer import BaseAnalyzer
from lib.section import Section, SectionTypes
from lib.tools.openai_client import Assistant, send_images


def _video_to_frames(file_path: str, frames_interval: int = 60) -> list[str]:
    video = cv2.VideoCapture(file_path)

    base64_frames: list[str] = []
    frame_index = 0
    while video.isOpened():
        success, frame = video.read()

        if not success:
            break

        if frame_index % frames_interval == 0:
            _, buffer = cv2.imencode(".jpg", frame)
            base64_frames.append(base64.b64encode(buffer).decode("utf-8"))  # type: ignore
        frame_index += 1
    video.release()
    print(len(base64_frames), "frames read.")
    return base64_frames


def _gpt_vision_res_to_sections(gpt_res: str) -> list[Section]:
    """Getting from GPT-Vision the analyzed scenes and returning list of Sections

    Args:
        gpt_res (str): This will be a JSON array with this objects: [{ "info": "<scene description>", "start", <seconds>, "end": <seconds> }]

    Returns:
        list[Section]
    """

    # TODO: check if this is the required JSON from the GPT..

    gpt_res_list = json.loads(gpt_res)

    sections = [
        Section(
            info=obj["info"],
            start=obj["start"],
            end=obj["end"],
            type=SectionTypes.video,
        )
        for obj in gpt_res_list
    ]
    return sections


class VideoAnalyzer(BaseAnalyzer):
    _AssistantType = Assistant.Video

    def analyze(self) -> list[Section]:
        frames = _video_to_frames(self.path)
        prompt = """
            THE PROMPT FOR THE VIDEO
        """
        gpt_res = send_images(frames, prompt)
        self._sections = _gpt_vision_res_to_sections(gpt_res)
        self._process()
        return self._sections
