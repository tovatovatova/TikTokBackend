import os

import google.cloud.storage as gc_storage
import google.cloud.videointelligence as gc_video

from lib.section import Section, SectionTypes


def upload_blob(bucket_name: str, source_file_name: str, destination_blob_name: str) -> None:
    """Uploads a file to the bucket."""
    storage_client = gc_storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


def extract_in_video_text(gcs_uri: str) -> list[Section]:
    """Analyze a video stored in Google Cloud Storage for text detection."""
    client = gc_video.VideoIntelligenceServiceClient()
    features = [gc_video.Feature.TEXT_DETECTION]

    operation = client.annotate_video(request={"features": features, "input_uri": gcs_uri})
    print("\nProcessing video for text detection:")
    result = operation.result(timeout=300)  # Increased timeout for potentially long processing
    assert result
    print("\nFinished processing.\n")

    text_annotations = result.annotation_results[0].text_annotations

    # Array to hold the results
    detected_texts: list[Section] = []

    for text_annotation in text_annotations:
        text = text_annotation.text
        assert isinstance(text, str)
        if len(text_annotation.segments) > 1:
            print('TODO: same text on multiple segments - think how to show the timestamp..')

        for segment in text_annotation.segments:
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.microseconds / 1e6)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.microseconds / 1e6)
            assert isinstance(start_time, float)
            assert isinstance(end_time, float)

            # Append the result to the array
            detected_texts.append(Section(start=start_time, end=end_time, type=SectionTypes.text, info=text))

    return detected_texts

def upload_video_and_extract_in_video_text(local_path: str) -> list[Section]:
    # Upload local video file to Google Cloud Storage
    bucket_name = "tiktok-analyzer"
    blob_name = os.path.basename(local_path)
    upload_blob(bucket_name, local_path, blob_name)

    # Analyze the uploaded video with the Video Intelligence API
    gcs_uri = f"gs://{bucket_name}/{blob_name}"
    res = extract_in_video_text(gcs_uri)
    return res

if __name__ == '__main__':
    upload_video_and_extract_in_video_text('./frames/test-20.mp4')
