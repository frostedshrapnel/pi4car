"""
Remote start via Pi.

Keyless signal detection on pin 7
Power for key module on pin 11
Brake switch is on pin 13
Start switch is on pin 15
Detection of car power status on pin 29
"""
import time
import RPi.GPIO as GPIO


class Car():

    """Remote starting and everything involved."""

    trigger = 0
    wait_time = 4

    def watch_signal(self):
        """Watch for voltage on keyless or door lock."""
        while True:
            if not GPIO.input(29):
                # If the car power is off
                if GPIO.input(7):
                    # If it detects a keyless/door lock press
                    time.sleep(.2)
                    timeout = time.time() + self.wait_time
                    while timeout > time.time():
                        # Watch for input for set amount of time.
                        if GPIO.input(7):
                            self.trigger += 1
                            time.sleep(.2)
                        if self.trigger == 2:
                            self.trigger = 0
                            self.start_car()
                        time.sleep(.1)

    def toggle_key(self, state):
        """Toggle the key fob."""
        GPIO.output(11, state)

    def toggle_brake(self, state):
        """Toggle the brake switch."""
        GPIO.output(13, state)

    def toggle_start(self, state):
        """Toggle the start button."""
        GPIO.output(15, state)

    def start_car(self):
        """Sequence for starting the car."""
        self.toggle_key('GPIO.HIGH')
        self.toggle_brake('GPIO.HIGH')
        self.toggle_start('GPIO.HIGH')
        time.sleep(3)
        # Release all buttons
        self.toggle_start('GPIO.LOW')
        self.toggle_brake('GPIO.LOW')
        self.toggle_key('GPIO.LOW')


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(29, GPIO.IN)
    mycar = Car()
    mycar.watch_signal()
    GPIO.cleanup()
