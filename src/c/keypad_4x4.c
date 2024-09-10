#include <stdio.h>
#include <pigpio.h>
#include <unistd.h>
#include <signal.h>

#define ROWS 4
#define COLS 4
#define STEADY_TIME 50000 // 50,000 microseconds (50 milliseconds)
#define ACTIVE_TIME 500000 // 500,000 microseconds (500 milliseconds)
#define DEBOUNCE_TIME 30000 // 30,000 microseconds (30 milliseconds)
#define POLL_TIME 10000 // 10,000 microseconds (10 milliseconds)

// GPIO pins for rows and columns
const int rowPins[ROWS] = {18, 23, 24, 25};
const int colPins[COLS] = {4, 17, 27, 22};

// Matrix representation of keypad
const char keys[ROWS][COLS] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}
};

// Function prototypes
void setup();
char readKeypad();
void cleanup();
void signalHandler(int signal);

// initialize GPIO pins
void setup() {
    // Initialize pigpio
    if (gpioInitialise() < 0) {
        fprintf(stderr, "Pigpio initialization failed.\n");
        exit(1);
    }

    // Set rows as input with internal pull-down resistors
    for (int i = 0; i < ROWS; i++) {
        gpioSetMode(rowPins[i], PI_INPUT);
        gpioSetPullUpDown(rowPins[i], PI_PUD_DOWN);
        gpioNoiseFilter(rowPins[i], STEADY_TIME, ACTIVE_TIME);
    }

    // Set columns as output with initial state LOW
    for (int i = 0; i < COLS; i++) {
        gpioSetMode(colPins[i], PI_OUTPUT);
        gpioWrite(colPins[i], PI_LOW);
    }
}

// Function to read keypad input
char readKeypad() {
    // Scan columns in a loop
    for (int col = 0; col < COLS; col++) {
        // Set column to HIGH one at a time
        gpioWrite(colPins[col], PI_HIGH);

        // Scan rows for a key press
        for (int row = 0; row < ROWS; row++) {
            // Check if the key is pressed
            if (gpioRead(rowPins[row]) == PI_HIGH) {
                while (gpioRead(rowPins[row]) == PI_HIGH)
                {
                    // Wait for key release    
                }

                gpioWrite(colPins[col], PI_LOW); // Deactivate output after the key pressed
                return keys[row][col]; // Return the key that was pressed
            }
        }

        gpioWrite(colPins[col], PI_LOW); // Deactivate the output after scan the input
    }
    return '\0'; // No key was pressed
}

// Function to cleanup GPIO pins
void cleanup() {
    gpioTerminate();
}

// Signal handler function (Ctrl + C)
void signalHandler(int signal) {
    if (signal == SIGINT)
    {
        printf("\nSignal SIGINT received. Cleaning up and exiting...\n");
        cleanup();
        exit(0);
    }
    
}

int main() {
    // Register signal handler
    signal(SIGINT, signalHandler);

    // Set up GPIO pins
    setup();

    printf("Press keys on the keypad...\n");

    // Main loop to read keypad input
    while (1) {
        char key = readKeypad();
        if (key != '\0') {
            printf("Key pressed: %c\n", key);
            usleep(DEBOUNCE_TIME); // Debounce
        }
        usleep(POLL_TIME); // Polling interval
    }

    // Clean up GPIO pins
    cleanup();
    printf("Application stopped!\n");
    return 0;
}
