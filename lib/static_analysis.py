import cv2
import numpy as np


def get_video_quality(video_file):
    # Open the video file using cv2.VideoCapture()
    cap = cv2.VideoCapture(video_file)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print('Error opening video file:', video_file)
        return None

    # Get the video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate the video bitrate
    bitrate = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate the entropy of the grayscale frame
        entropy = np.mean(-np.log2(np.unique(gray_frame)))

        # Calculate the bitrate based on the entropy
        bitrate += entropy * width * height * fps

    # Calculate the PSNR (Peak Signal-to-Noise Ratio)
    psnr = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Calculate the PSNR for the current frame
        psnr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        psnr += cv2.PSNR(psnr_frame, gray_frame)

    # Calculate the average PSNR
    psnr /= cap.get(cv2.CAP_PROP_FRAME_COUNT)

    # Close the video file
    cap.release()

    # Calculate the overall video quality using a combination of bitrate and PSNR
    quality = bitrate * psnr

    return quality

# Example usage
video_file = 'video.mp4'
quality = get_video_quality(video_file)
print('Video quality:', quality)
