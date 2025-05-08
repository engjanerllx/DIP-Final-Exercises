import cv2
import numpy as np

def process_video(input_filename, output_filename):
    """
    Converts a color video to grayscale and adjusts contrast over time.

    Args:
        input_filename (str): Path to the input video file.
        output_filename (str): Path to save the output video file.
    """

    cap = cv2.VideoCapture(input_filename)
    if not cap.isOpened():
        print(f"Error: Could not open video file: {input_filename}")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height), isColor=False)

    if not out.isOpened():
        print(f"Error: Could not create output video file: {output_filename}")
        return

    for i in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: Could not read frame {i}. Exiting loop.")
            break

        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Y = 0.299*R + 0.587*G + 0.114*B [cite: 33]

        progress = i / (total_frames - 1) if total_frames > 1 else 0 

        alpha = 0.8 + (1.5 - 0.8) * progress 
        mean = 128  
        adjusted_frame = np.clip(alpha * (gray_frame - mean) + mean, 0, 255).astype(np.uint8)  

        out.write(adjusted_frame)

    cap.release()
    out.release()
    print("Video processing complete.")

if __name__ == "__main__":
    input_filename = "my_test_video.mp4"  
    output_filename = "grayscale_conversion_exer1.mp4" 
    process_video(input_filename, output_filename)