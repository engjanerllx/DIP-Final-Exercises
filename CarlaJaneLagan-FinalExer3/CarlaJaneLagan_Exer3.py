import cv2
import numpy as np
import os.path

def rotate_video(input_filename, output_filename):
    """
    Rotates a video gradually around its center.

    Args:
        input_filename (str): Path to the input video file.
        output_filename (str): Path to save the output video file.
    """

    if not os.path.exists(input_filename):
        print(f"Error: Input video file not found at: {input_filename}")
        return

    cap = cv2.VideoCapture(input_filename)
    if not cap.isOpened():
        print("Error opening video")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))

    if not out.isOpened():
        print(f"Error: Could not create output video file: {output_filename}")
        return

    final_angle = 90 

    center = (frame_width / 2, frame_height / 2)

    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        current_angle = final_angle * (i / (total_frames - 1)) if total_frames > 1 else 0

        rotation_matrix = cv2.getRotationMatrix2D(center, current_angle, 1)

        rotated_frame = cv2.warpAffine(frame, rotation_matrix, (frame_width, frame_height))

        out.write(rotated_frame)

    cap.release()
    out.release()
    print(f"Video processing complete. Output saved as: {output_filename}")


if __name__ == "__main__":
    input_filename = "my_test_video.mp4" 
    output_filename = "gradually_rotation_exer3.mp4"
    rotate_video(input_filename, output_filename)