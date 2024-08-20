# Keypad 4x4

![Keypad](Images/Keypad_4x4.jpg)

A 4x4 keypad consists of 16 buttons arranged in a grid with 4 rows and 4 columns. Each button connects a specific row and column. When a button is pressed, it connects a specific row to a column, allowing you to detect which key was pressed by checking which row and column were connected.

## Wiring

The 4x4 keypad has 8 pins: 4 for the rows and 4 for the columns. Connect these pins to the GPIO pins on the Raspberry Pi.

- Keypad Pins: The first 4 pins correspond to the rows, and the next 4 correspond to the columns

| Keypad Pinout | Keypad Arrangement |
|---------------|--------------------|
|![Keypad Pinout](Images/Keypad_pinout.jpg) | ![Keypad Arrangement](Images/keypad_arrangement.jpg) |

- Raspberry Pi GPIO Pins: Connect the keypad to any GPIO pins, but for this example, use the following configuration:

![RPi GPIO Pinout](Images/Raspberry-Pi-3B+-GPIO-Pinout-Diagram.png)

![GPIO Mapping](Images/GPIO.png)

| **Keypad Pins** | **Raspberry Pi GPIO Pins** |
|-------------|------------------------|
| Column 1 | GPIO4 |
| Column 2 | GPIO17 |
| Column 3 | GPIO27 |
| Column 4 | GPIO22 |
| Row 1 | GPIO18 |
| Row 2 | GPIO23 |
| Row 3 | GPIO24 |
| Row 4 | GPIO25 |

## Python Code to Interface the 4x4 Keypad

Create a Python script to read the keypad input:

```python
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

```
