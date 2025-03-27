import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# Set GPIO Pins
GPIO_TRIGGER = 23  # Trigger pin
GPIO_ECHO = 24     # Echo pin

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    """
    Calculate the distance to the nearest object using ultrasonic sensor
    Returns the distance in centimeters
    """
    # Set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # Time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2 (go and return)
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def main():
    try:
        print("Ultrasonic Motion Detection Started")
        
        while True:
            # Measure distance
            dist = distance()
            
            # Detect motion (adjust threshold as needed)
            # Here, we'll consider anything closer than 50 cm as motion detected
            if dist < 50:
                print("Someone is here!")
                # Optional: Add a small delay to prevent multiple rapid detections
                time.sleep(2)
            
            # Small delay to prevent CPU overload
            time.sleep(0.5)
 
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
