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

        # Set column as outputs and set them to high
        for col in self.COLS:
            GPIO.setup(col, GPIO.OUT)
            GPIO.output(col, GPIO.HIGH)

        # Set up row as inputs with pull-up resistors
        for row in self.ROWS:
            GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_keypad(self):
        for col_idx, col in enumerate(self.COLS):
            GPIO.output(col, GPIO.LOW)  # set output to low, one at a time
            for row_idx, row in enumerate(self.ROWS):
                if GPIO.input(row) == GPIO.LOW:  # Check if the key is pressed
                    key = self.KEYPAD[row_idx][col_idx]
                    while GPIO.input(row) == GPIO.LOW:
                        pass
                    GPIO.output(row, GPIO.HIGH)  # Deactivate output after the key pressed
                    sleep(0.1)
                    return key
            GPIO.output(col, GPIO.HIGH)  # Deactivate the output after scan
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
        print("\nApplication stopped!")
