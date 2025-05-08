import cv2
import numpy as np

def night_vision_effect(input_filename, output_filename):
    """
    Applies a simple night vision effect to a video:
    1. Converts to grayscale.
    2. Applies a green tint.
    3. Optionally adjusts brightness/contrast.
    4. Optionally adds noise.

    Args:
        input_filename (str): Path to the input video file.
        output_filename (str): Path to save the output video file.
    """

    cap = cv2.VideoCapture(input_filename)  # Open the video file
    if not cap.isOpened():
        print(f"Error: Could not open video file: {input_filename}")
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

    for i in range(total_frames):
        ret, frame = cap.read()  # Read a frame from the video
        if not ret:
            print(f"Warning: Could not read frame {i}. Exiting loop.")
            break

       
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        output_frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)  # Create black frame

        output_frame[:, :, 1] = gray_frame  # Copy grayscale to green channel

        alpha = 1.2  # Contrast control (1.0 = no change)
        beta = 10    # Brightness control (0 = no change)
        output_frame[:, :, 1] = cv2.convertScaleAbs(output_frame[:, :, 1], alpha=alpha, beta=beta)


      
        noise = np.random.normal(0, 20, output_frame[:, :, 1].shape).astype(np.int8)  # Adjust noise level (20)
        noisy_green_channel = np.clip(output_frame[:, :, 1] + noise, 0, 255).astype(np.uint8)
        output_frame[:, :, 1] = noisy_green_channel

        out.write(output_frame)

    cap.release()
    out.release()
    print(f"Night vision effect applied. Output video saved as: {output_filename}")


if __name__ == "__main__":
    input_filename = "my_test_video.mp4"  
    output_filename = "night_vision_exer4.mp4"
    night_vision_effect(input_filename, output_filename)