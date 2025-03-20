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
    # Send pulse to trigger the sensor
    GPIO.output(TRIG, False)
    time.sleep(2)  # Wait for sensor to stabilize

    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # Send pulse
    GPIO.output(TRIG, False)

    # Wait for the echo to start and end
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    pulse_end = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Calculate distance in cm
    return round(distance, 2)

try:
    print("Waiting for movement...")
    while True:
        distance = get_distance()
        print(f"Distance: {distance} cm")
        if distance < THRESHOLD_DISTANCE:
            print("🚨 Someone is here! 🚨 ichy")
            time.sleep(1)  # Wait before checking again to avoid spamming
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopping...")
    GPIO.cleanup()
