import os
from pathlib import Path

from sightengine.client import SightengineClient

client = SightengineClient(
    api_secret=os.environ["SIGHTENGINE_SECRET"], api_user=os.environ["SIGHTENGINE_USER"]
)


def check_video(video_url: Path) -> str:
    output = client.check(
        "nudity-2.0",
        "wad",
        "properties",
        "celebrities",
        "gore",
        "faces",
        "face-attributes",
        "text",
        "qr-content",
        "text-content",
        "offensive",
        "tobacco",
        "money",
        "gambling",
    ).video_sync(video_url)
    return output


if __name__ == "__main__":
    check_video(
        Path(
            "https://storage.googleapis.com/tiktok-analyzer/This%20is%20your%20child%20-%20Vertical%20English.mp4"
        )
    )
