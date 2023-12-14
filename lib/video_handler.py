import base64
from typing import Optional

import cv2

from lib.openai_client import client


def video_to_frames(file_path: str, frames_interval: int = 60) -> list[str]:
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


def check_video_content(file_path: str) -> Optional[str]:
    frames = video_to_frames(file_path)
    prompt_messages = [
        {
            "role": "user",
            "content": [
                # "These are frames from a video that I want to upload. Generate
                # a compelling description that I can upload along with the
                # video.",
                "Can tiktok approve that content?",
                *map(lambda x: {"image": x, "resize": 768}, frames),
            ],
        },
    ]

    # TODO: Something fishy about the type and structure of prompt_messages. Need to review and possible correct.
    #  See https://platform.openai.com/docs/guides/vision/uploading-base-64-encoded-images
    result = client.chat.completions.create(
        model='gpt-4-vision-preview',
        messages=prompt_messages,  # type: ignore
        max_tokens=200
    )
    return result.choices[0].message.content


if __name__ == '__main__':
    print(check_video_content('../frames/test-20.mp4'))
