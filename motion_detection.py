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
AVERAGE_COUNT = 5  # Number of readings to average

def get_distance():
    # Send a short pulse to trigger the sensor
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for the echo signal to start
    timeout_start = time.time()
    while GPIO.input(ECHO) == 0:
        if time.time() - timeout_start > 0.1:  # Timeout if no echo after 100ms
            return 999  # Return large value if no echo is received

    pulse_start = time.time()

    # Wait for the echo signal to stop
    timeout_start = time.time()
    while GPIO.input(ECHO) == 1:
        if time.time() - timeout_start > 0.1:  # Timeout if no echo after 100ms
            return 999  # Return large value if echo never stops

    pulse_end = time.time()

    # Calculate the distance
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Speed of sound = 34300 cm/s

    return round(distance, 2)

def get_average_distance():
    distances = []
    for _ in range(AVERAGE_COUNT):
        distance = get_distance()
        distances.append(distance)
        time.sleep(0.1)  # Small delay between readings
    return round(sum(distances) / len(distances), 2)

try:
    print("Waiting for movement...")
    while True:
        distance = get_average_distance()
        print(f"Average Distance: {distance} cm")  # Displaying the average distance
        if distance < THRESHOLD_DISTANCE:
            print("🚨 Someone is here! 🚨")
            time.sleep(1)  # Wait to avoid spamming
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopping...")
    GPIO.cleanup()
