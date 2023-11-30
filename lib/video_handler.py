# import os
# import cv2
# from lib.openai_client import client

# def video_to_frames(file_path: str, frames_interval: int = 10) -> list[str]:
#     # Create frames directory if it doesn't exist
#     if not os.path.exists('frames'):
#         os.makedirs('frames')

#     # Create a VideoCapture object
#     cap = cv2.VideoCapture(file_path)

#     # Check if video opened successfully
#     if (cap.isOpened()== False): 
#         print("Error opening video file")

#     # Read until video is completed
#     frame_count = 0
#     frames = []
#     while(cap.isOpened()):
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if ret == True:
#             # Save every frames_interval frame
#             if frame_count % frames_interval == 0:
#                 frame_file_path = f"frames/frame_{frame_count}.jpg"
#                 cv2.imwrite(frame_file_path, frame)
#                 print(f"Saved frame {frame_count} at {frame_file_path}")
#                 frames.append(frame_file_path)
#             frame_count += 1
#         # Break the loop if no more frames
#         else: 
#             break

#     # When everything done, release the video capture object
#     cap.release()

#     return frames

# ProblematicFrame = tuple[str, str] # frame path and the problem 
# def check_video_content(file_path: str) -> list[ProblematicFrame]:
#     ...