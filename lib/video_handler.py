import os
import cv2
import base64
from lib.openai_client import client


def video_to_frames(file_path: str, frames_interval: int = 60):
    video = cv2.VideoCapture(file_path)

    base64Frames = []
    frame_index = 0
    while video.isOpened():
        success, frame = video.read()

        if not success:
            break

        if frame_index % frames_interval == 0:
            _, buffer = cv2.imencode(".jpg", frame)
            base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
        frame_index += 1
    video.release()
    print(len(base64Frames), "frames read.")
    return base64Frames


ProblematicFrame = tuple[str, str]  # frame path and the problem


def check_video_content(file_path: str):
    frames = video_to_frames(file_path)
    PROMPT_MESSAGES = [{
        "role": "user", "content": [
            # "These are frames from a video that I want to upload. Generate
            # a compelling description that I can upload along with the
            # video.",
            "Can tiktok approve that content?",
            *map(lambda x: {"image": x, "resize": 768}, frames), ],
    }, ]
    params = {
        "model": "gpt-4-vision-preview", "messages": PROMPT_MESSAGES,
        "max_tokens": 200,
    }

    result = client.chat.completions.create(**params)
    print(result.choices[0].message.content)


if __name__ == '__main__':
    check_video_content('C:/Users/ywiesel/Downloads/tovi-7.mp4')
