import pigpio
import time
import signal
import sys

# Constants
ROWS = 4
COLS = 4
STEADY_TIME = 50000  # 50 milliseconds
ACTIVE_TIME = 500000   # 500 milliseconds
DEBOUNCE_TIME = 30000  # 30 milliseconds
POLL_TIME = 10000    # 10 milliseconds

# GPIO pins for rows and columns
rowPins = [18, 23, 24, 25]
colPins = [4, 17, 27, 22]

# Matrix representation of keypad
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

class Keypad:
    def __init__(self):
        self.pi = pigpio.pi()  # Connect to local pigpio daemon
        if not self.pi.connected:
            print("Failed to connect to pigpio daemon.")
            sys.exit(1)
        self.setup()
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def setup(self):
        # Set rows as input with internal pull-down resistors
        for pin in rowPins:
            self.pi.set_mode(pin, pigpio.INPUT)
            self.pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
            self.pi.set_noise_filter(pin, int(STEADY_TIME), int(ACTIVE_TIME))

        # Set columns as output with initial state LOW
        for pin in colPins:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.write(pin, LOW)
    
    def read_keypad(self):
        # Scan columns in a loop
        for col in range(COLS):
            # Set column to HIGH one at a time
            self.pi.write(colPins[col], HIGH)
            
            # Scan rows for a key press
            for row in range(ROWS):
                # Check if the key is pressed
                if self.pi.read(rowPins[row]) == HIGH:
                    while self.pi.read(rowPins[row]) == HIGH:
                        # Wait for key release
                        pass
                    
                    self.pi.write(colPins[col], LOW)  # Deactivate output after the key pressed
                    return keys[row][col]  # Return the key that was pressed
            
            self.pi.write(colPins[col], LOW)  # Deactivate the output after scanning the input
        
        return None  # No key was pressed
    
    def cleanup(self):
        self.pi.stop()
    
    def signal_handler(self, signal, frame):
        print("\nSignal SIGINT received. Cleaning up and exiting...")
        self.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    keypad = Keypad()
    
    print("Press keys on the keypad...")
    
    # Main loop to read keypad input
    try:
        while True:
            key = keypad.read_keypad()
            if key is not None:
                print(f"Key pressed: {key}")
                time.sleep(DEBOUNCE_TIME)  # Debounce
            time.sleep(POLL_TIME)  # Polling interval
    except KeyboardInterrupt:
        keypad.cleanup()
        print("Application stopped!")
