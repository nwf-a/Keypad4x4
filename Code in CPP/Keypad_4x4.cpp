#include <iostream>
#include <wiringPi.h>
#include <signal.h>
#include <chrono>

class Keypad {
private:
    // GPIO pin configuration (using wiringPi pin numbers)
    int ROWS[4] = {1, 4, 5, 6};    // wPi pin numbers for rows
    int COLS[4] = {7, 0, 2, 3};    // wPi pin numbers for columns

    // Keypad configuration (4x4)
    char KEYPAD[4][4] = {
        {'1', '2', '3', 'A'},
        {'4', '5', '6', 'B'},
        {'7', '8', '9', 'C'},
        {'*', '0', '#', 'D'}
    };

    // Debounce time in milliseconds
    const int DEBOUNCE_TIME = 50; // Adjust as needed

    // Last key state
    char lastKey = '\0';
    std::chrono::steady_clock::time_point lastPressTime;

    void cleanup() {
        // Set all pins to input with internal pull-down resistors
        for (int i = 0; i < 4; i++) {
            pinMode(ROWS[i], INPUT);
            pullUpDnControl(ROWS[i], PUD_DOWN); // Set as pull-down resistor
            pinMode(COLS[i], INPUT);
            pullUpDnControl(COLS[i], PUD_DOWN); // Set as pull-down resistor
        }
    }

public:
    Keypad() {
        wiringPiSetup(); // Initialize WiringPi

        // Configure row pins as input with internal pull-down resistors
        for (int i = 0; i < 4; i++) {
            pinMode(ROWS[i], INPUT);
            pullUpDnControl(ROWS[i], PUD_DOWN);
        }

        // Configure column pins as output and LOW
        for (int i = 0; i < 4; i++) {
            pinMode(COLS[i], OUTPUT);
            digitalWrite(COLS[i], LOW);
        }

        // Setup signal handler for ctrl+c
        signal(SIGINT, [](int sig) {
            Keypad::instance()->cleanup();
            exit(0);
        });

        lastKey = '\0';
        lastPressTime = std::chrono::steady_clock::now();
    }

    static Keypad* instance() {
        static Keypad instance;
        return &instance;
    }

    char getKey() {
        char key = '\0';
        for (int col = 0; col < 4; col++) {
            // Set current column to HIGH
            digitalWrite(COLS[col], HIGH);

            for (int row = 0; row < 4; row++) {
                // If the button at the selected row and column is pressed
                if (digitalRead(ROWS[row]) == HIGH) {
                    key = KEYPAD[row][col];
                    break;
                }
            }

            // Set column back to LOW after scanning
            digitalWrite(COLS[col], LOW);
            if (key != '\0') break;
        }

        // Handle debounce and key press duration
        auto now = std::chrono::steady_clock::now();
        auto elapsedTime = std::chrono::duration_cast<std::chrono::milliseconds>(now - lastPressTime).count();

        if (key != lastKey) {
            lastKey = key;
            lastPressTime = now;
        } else if (key != '\0' && elapsedTime > DEBOUNCE_TIME) {
            lastPressTime = now; // Reset debounce timer
        }

        return key;
    }

    void scan() {
        while (true) {
            char key = getKey();
            if (key != '\0') {
                std::cout << "Key Pressed: " << key << std::endl;
            }
            delay(10); // Small delay for CPU efficiency
        }
    }
};

int main() {
    Keypad* keypad = Keypad::instance();
    keypad->scan();
    return 0;
}
