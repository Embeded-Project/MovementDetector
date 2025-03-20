from picamera2 import Picamera2
import time

# Function to start recording from the Raspberry Pi camera
def start_camera():
    # Initialize the camera
    picam2 = Picamera2()
    picam2.start_preview()  # Start the camera preview
    time.sleep(2)  # Wait for the camera to initialize
    
    # Set the filename to save the video
    filename = "output.h264"
    
    # Start recording
    print("Recording started...")
    picam2.start_recording(filename)
    
    try:
        while True:
            time.sleep(1)  # Let the recording continue for as long as needed
    except KeyboardInterrupt:
        pass  # Stop recording if the user interrupts the process (Ctrl + C)
    
    # Stop recording and close the camera
    picam2.stop_recording()
    picam2.close()
    print("Recording stopped.")

# Main function to handle user input and start recording
def main():
    input("Press Enter to start recording...")
    
    # Start the camera when user presses Enter
    start_camera()

# Run the script
if __name__ == "__main__":
    main()
