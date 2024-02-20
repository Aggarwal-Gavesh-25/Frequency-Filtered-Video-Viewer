import cv2  # For computer vision tasks
import numpy as np  # For numerical operations
from scipy import signal as sig # For signal processing

# Function to filter out frequencies outside the specified range
def filter_frequency(signal_data, freq_range, fps):     # Takes a signal, frequency range & frames per second
    nyquist_freq = fps / 2      # 
    cutoff_freq = freq_range[1] / nyquist_freq
    b, a = sig.butter(4, cutoff_freq, 'low', analog=False)
    filtered_signal = sig.filtfilt(b, a, signal_data)
    return filtered_signal

# Open the video file
cap = cv2.VideoCapture('/Users/gavesh_aggarwal/Desktop/Frequency-Filtered-Video-Viewer/video.mp4')

# Get the frames per second (fps) of the video
fps = cap.get(cv2.CAP_PROP_FPS)

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret == True:
        # Filter the frequency components (0 to 1 Hz)
        filtered_frame = np.zeros_like(frame)
        for i in range(3):  # Iterate over color channels (assuming BGR)
            filtered_channel = filter_frequency(frame[:,:,i].flatten(), (0, 1), fps)
            filtered_channel = filtered_channel.reshape(frame[:,:,i].shape)
            filtered_frame[:,:,i] = filtered_channel

        # Normalize the filtered image to 0-255 range
        filtered_frame = cv2.normalize(filtered_frame, None, 0, 255, cv2.NORM_MINMAX)

        # Convert to uint8
        filtered_frame = np.uint8(filtered_frame)

        # Display the original and filtered frames
        cv2.imshow('Original', frame)
        cv2.imshow('Filtered (0-1 Hz)', filtered_frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
           break
    else:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
