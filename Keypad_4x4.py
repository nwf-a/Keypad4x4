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

        # Set column as outputs and set them to LOW
        for col in self.COLS:
            GPIO.setup(col, GPIO.OUT, initial=GPIO.LOW)

        # Set up row as inputs with pull-down resistors to avoid floating
        for row in self.ROWS:
            GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_keypad(self):
        for col_idx, col in enumerate(self.COLS):
            GPIO.output(col, GPIO.HIGH)  # set output to HIGH, one at a time
            for row_idx, row in enumerate(self.ROWS):
                if GPIO.input(row) == GPIO.HIGH:  # Check if the key is pressed
                    sleep(0.2) #Debounce time
                    key = self.KEYPAD[row_idx][col_idx]
                    while GPIO.input(row) == GPIO.HIGH:
                        pass
                    GPIO.output(row, GPIO.LOW)  # Deactivate output after the key pressed
                    return key
            GPIO.output(col, GPIO.LOW)  # Deactivate the output after scan the input
        return None

    def print_keypad(self):
        key = self.read_keypad()
        if key:
            print(f"Key Pressed: {key}")

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
