import RPi.GPIO as GPIO
import time

# Pin configuration
TRIG = 23  # GPIO pin for Trigger
ECHO = 24  # GPIO pin for Echo

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Detection threshold in cm
THRESHOLD_DISTANCE = 50

def get_distance():
    # Send a short pulse to trigger the sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Timeout to avoid infinite loop
    timeout = time.time() + 0.1
    
    # Wait for the echo signal to start
    while GPIO.input(ECHO) == 0:
        if time.time() > timeout:
            return 999  # Return large value if no echo is received
    
    pulse_start = time.time()

    # Wait for the echo signal to stop
    timeout = time.time() + 0.1
    while GPIO.input(ECHO) == 1:
        if time.time() > timeout:
            return 999  # Return large value if echo never stops
    
    pulse_end = time.time()

    # Calculate the distance
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Speed of sound = 34300 cm/s

    return round(distance, 2)

try:
    print("Waiting for movement...")
    while True:
        distance = get_distance()
        if distance < THRESHOLD_DISTANCE:
            print("🚨 Someone is here! 🚨")
            time.sleep(1)  # Wait to avoid spamming
        else:
            print(f"Distance: {distance} cm")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopping...")
    GPIO.cleanup()
