import base64
import json
from pathlib import Path

import cv2

from lib.analyzers.base_analyzer import BaseAnalyzer
from lib.section import Section, SectionTypes
from lib.tools.openai_client import Assistant, send_images
from lib.user_config import UserConfig


def _video_to_frames(file_path: Path, sampling_interval_sec: float) -> list[str]:
    video = cv2.VideoCapture(str(file_path))

    # TODO: Handle correctly with exceptions and converting to response
    assert video.isOpened(), f"Video file {file_path} not found."

    # Extract fps and convert sampling_interval_sec to frames_interval
    frame_rate = video.get(cv2.CAP_PROP_FPS)
    frames_interval = int(sampling_interval_sec * frame_rate)

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


def _gpt_vision_res_to_sections(
    gpt_res: str, sampling_interval_sec: float
) -> list[Section]:
    """Getting from GPT-Vision the analyzed scenes and returning list of Sections

    Args:
        gpt_res (str): This will be a JSON array with this objects: [{ "info": "<scene description>", "idx": <index> }]
        sampling_interval_sec (float): The sampling time interval between consecutive frames
    Returns:
        list[Section]
    """

    # TODO: check if this is the required JSON from the GPT..

    gpt_res_list = json.loads(gpt_res)

    sections: list[Section] = []
    for obj in gpt_res_list:
        start = obj["idx"] * sampling_interval_sec
        end = start + sampling_interval_sec
        sections.append(
            Section(
                info=obj["info"],
                start=start,
                end=end,
                type=SectionTypes.video,
            )
        )
    return sections


class VideoAnalyzer(BaseAnalyzer):
    _AssistantType = Assistant.Video
    SectionType = SectionTypes.video
    PROMPT = """
        I am sharing with you multiple images. I need you to give me extensive details on everything
        you see in each one of the images so I could share with a blind person who cannot see them by himself.

        You will be asked to log the details/information you extract, for every image separately (there is no
        relation between the images).

        It is important for me to get information about possible misbehavior/violence or anything that might be
        disturbing in the images (violence, weapons, drugs, protestors). Do not avoid sharing this information with
        me. If images dont contain such information, you dont need to mention that they dont, just share what you
        see!

        Please reply with a JSON of this format (fill in the details in the "info" values instead of null) -
        [
            {
                "idx": 0,
                "info": null,
            },
            {
                "idx": 1,
                "info": null,
            }
        ]

        RULES:
        1. Ignore any text you see inside the frames. I do not need this information. Dont let it block you!
        2. ALLWAYS reply with a JSON of this format (length equal to the number of images) and nothing
        more (and nothing less!), one array element for each image! User is expecting for the response
        to be a valid JSON of this format.
        3. If you cant reply on specific images, just return "I can't comment on this image" for those ONLY.
        4. Do your best effort to give some details on as many images as you can!
        5. Consider each image as a "Stand alone" image. Meaning, DO NOT relate to the other images

        You response mush bt ONLY the JSON formatted reply!
    """

    def _prepare_sections(self, file_path: Path) -> list[Section]:
        # Sample frames from the video
        sample_rate_sec = 2.0
        frames = _video_to_frames(file_path, sample_rate_sec)

        # Get GPT-Vision's help to understand the frames
        gpt_res = send_images(frames, self.PROMPT)

        sections = _gpt_vision_res_to_sections(
            self._extract_json_str(gpt_res), sample_rate_sec
        )
        return sections


if __name__ == "__main__":
    analyzer = VideoAnalyzer(UserConfig("", ""))
    analyzer.analyze(Path("./frames/test-20.mp4"))
