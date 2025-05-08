import cv2
import numpy as np
import os.path

def apply_moving_blur(input_filename, output_filename):
    """
    Applies a moving blur effect to a video.

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
        print("Error creating output video file")
        return

    kernel_size = 21  # Adjust for blur intensity
    blur_region_width = 100  # Adjust for the width of the blur band

    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: Could not read frame {i}. Breaking loop.")
            break

        
        cx = (frame_width / total_frames) * i

        output_frame = frame.copy()

        blurred_frame = cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)
        # You could also try a simple box blur:
        # blurred_frame = cv2.blur(frame, (kernel_size, kernel_size))

        x_start = max(0, int(cx - blur_region_width / 2))
        x_end = min(frame_width, int(cx + blur_region_width / 2))

        output_frame[:, x_start:x_end] = blurred_frame[:, x_start:x_end]

        out.write(output_frame)

    cap.release()
    out.release()
    print("Video processing complete.")


if __name__ == "__main__":
    input_filename = "my_test_video.mp4"  
    output_filename = "moving_filter_exer2.mp4"  
    apply_moving_blur(input_filename, output_filename)