import google.cloud.storage as gc_storage
import google.cloud.videointelligence as gc_video


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = gc_storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


InVideoTextType = dict[str, str | float]

def extract_in_video_text(gcs_uri: str) -> list[InVideoTextType]:
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
    detected_texts = []

    for text_annotation in text_annotations:
        text = text_annotation.text
        if len(text_annotation.segments) > 1:
            print('TODO: same text on multiple segments - think how to show the timestamp..')
            
        for segment in text_annotation.segments:
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.microseconds / 1e6)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.microseconds / 1e6)

            # Append the result to the array
            detected_texts.append({
                "text": text,
                "start_time": start_time,
                "end_time": end_time
            })

    return detected_texts



if __name__ == '__main__':
    # Replace with your bucket name, local video file, and desired blob name
    bucket_name = "tiktok-analyzer"
    local_video_file = './frames/test-20.mp4'
    blob_name = "your-video.mp4"

    # Upload local video file to Google Cloud Storage
    upload_blob(bucket_name, local_video_file, blob_name)

    # Analyze the uploaded video with the Video Intelligence API
    gcs_uri = f"gs://{bucket_name}/{blob_name}"
    res = extract_in_video_text(gcs_uri)
    print(res)