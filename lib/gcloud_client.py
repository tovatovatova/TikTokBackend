from google.cloud import storage
from google.cloud import videointelligence

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def analyze_video_gcs(gcs_uri: str):
    """Analyze a video stored in Google Cloud Storage for shot changes, labels, and explicit content."""
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [
        videointelligence.Feature.TEXT_DETECTION, 
    ]
    operation = client.annotate_video(request={"features": features, "input_uri": gcs_uri})
    print("\nProcessing video for annotations:")
    result = operation.result(timeout=100)
    assert result
    print("\nFinished processing.\n")
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print(f"Video label description: {segment_label.entity.description}")
        for category_entity in segment_label.category_entities:
            print(f"\tCategory: {category_entity.description}")


if __name__ == '__main__':
    # Replace with your bucket name, local video file, and desired blob name
    bucket_name = "tiktok-analyzer"
    local_video_file = r"C:\Users\ywiesel\Downloads\test.mp4"
    blob_name = "your-video.mp4"

    # Upload local video file to Google Cloud Storage
    upload_blob(bucket_name, local_video_file, blob_name)

    # Analyze the uploaded video with the Video Intelligence API
    gcs_uri = f"gs://{bucket_name}/{blob_name}"
    analyze_video_gcs(gcs_uri)
