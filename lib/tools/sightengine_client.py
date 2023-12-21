from sightengine.client import SightengineClient

client = SightengineClient("741245411", "wJnGAF8RHgZxEaKfsp3JopUkyq")


def check_video(video_url: str) -> str:
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
        "https://storage.googleapis.com/tiktok-analyzer/This%20is%20your%20child%20-%20Vertical%20English.mp4"
    )
