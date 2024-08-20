import RPi.GPIO as GPIO
from time import sleep

class Keypad:
    def __init__(self):
        # GPIO pin configuration
        self.ROWS = [18, 23, 24, 25]    # GPIO pins for rows
        self.COLS = [4, 17, 27, 22]      # GPIO pins for columns

        # Keypad configuration (4x4)
        self.KEYPAD = [
            [1, 2, 3, 'A'],
            [4, 5, 6, 'B'],
            [7, 8, 9, 'C'],
            ['*', 0, '#', 'D']
        ]

        # Setup GPIO
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # Set up rows as outputs and set them to high
        for row in self.ROWS:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, GPIO.HIGH)

        # Set up columns as inputs with pull-down resistors
        for col in self.COLS:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_keypad(self):
        for row_idx, row in enumerate(self.ROWS):
            GPIO.output(row, GPIO.LOW)  # Activate the current row
            for col_idx, col in enumerate(self.COLS):
                if GPIO.input(col) == GPIO.HIGH:  # Check if the key is pressed
                    key = self.KEYPAD[row_idx][col_idx]
                    GPIO.output(row, GPIO.HIGH)  # Deactivate the row
                    return key
            GPIO.output(row, GPIO.HIGH)  # Deactivate the row
            sleep(0.1)
        return None

    def print_keypad(self):
        key = self.read_keypad()
        if key:
            print(f"Key Pressed: {key}")
            sleep(0.1)  # Debounce time to avoid repeated prints

    def cleanup(self):
        GPIO.cleanup()  # Clean up GPIO

if __name__ == "__main__":
    # Initialize the Keypad
    keypad = Keypad()

    try:
        while True:
            keypad.print_keypad()
    except KeyboardInterrupt:
        keypad.cleanup()  # Clean up GPIO on CTRL+C exit