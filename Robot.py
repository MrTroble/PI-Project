import RPi.GPIO as GPIO
import time


# @singleton
class Robot:

    # Static class members
    # Thees values shouldn't change
    # (There are some circumstances)
    Go = 30
    Frequency = 20
    Stop = 0

    # Initializes a new instance
    #
    # Setup all pins needed for
    # the robotic edukit from camjam
    #
    # Initializes PWM for the motors
    #
    # Param:
    #    light_sensor_pin:
    #       Pin ID of black sensor
    #    echo_pin:
    #       Pin ID of echo pin
    #    trigger_pin:
    #       Pin ID to trigger echo
    def __init__(self,
                 light_sensor_pin,
                 echo_pin,
                 trigger_pin):

        # Initialize values
        self._light_sensor_pin = light_sensor_pin
        self._echo_pin = echo_pin
        self._trigger_pin = trigger_pin

        # Pin constants
        motor_af = 10
        motor_ab = 9
        motor_bf = 8
        motor_bb = 7

        # Setmode for pins and disable warnings
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)

        # Setup pins
        GPIO.setup([motor_af,
                    motor_ab,
                    motor_bf,
                    motor_bb,
                    trigger_pin], GPIO.OUT)
        GPIO.setup([light_sensor_pin, echo_pin], GPIO.IN)

        # Initialize PWM for pins
        self._pwm_AF = GPIO.PWM(motor_af, Robot.Frequency)
        self._pwm_AB = GPIO.PWM(motor_ab, Robot.Frequency)
        self._pwm_BF = GPIO.PWM(motor_bf, Robot.Frequency)
        self._pwm_BB = GPIO.PWM(motor_bb, Robot.Frequency)

        # Start duty cycle with zero
        self._pwm_AF.start(Robot.Stop)
        self._pwm_AB.start(Robot.Stop)
        self._pwm_BF.start(Robot.Stop)
        self._pwm_BB.start(Robot.Stop)

        # Disable output for trigger
        GPIO.output(trigger_pin, False)

    # ===================================================
    # Robot control section
    # ===================================================

    # Stops the duty cycles of all motors
    def stop(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Stop)
        self._pwm_AB.ChangeDutyCycle(Robot.Stop)
        self._pwm_BF.ChangeDutyCycle(Robot.Stop)
        self._pwm_BB.ChangeDutyCycle(Robot.Stop)

    # Starts the duty cycle for Forward A and B
    # Stops all others
    def forward(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Go)
        self._pwm_AB.ChangeDutyCycle(Robot.Stop)
        self._pwm_BF.ChangeDutyCycle(Robot.Go)
        self._pwm_BB.ChangeDutyCycle(Robot.Stop)

    # Starts the duty cycle for Backwards A and B
    # Stops all others
    def back(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Stop)
        self._pwm_AB.ChangeDutyCycle(Robot.Go)
        self._pwm_BF.ChangeDutyCycle(Robot.Stop)
        self._pwm_BB.ChangeDutyCycle(Robot.Go)

    # Starts the duty cycle for
    # Backwards A,
    # Forwards B
    #
    # Stops all others
    def left(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Stop)
        self._pwm_AB.ChangeDutyCycle(Robot.Go)
        self._pwm_BF.ChangeDutyCycle(Robot.Go)
        self._pwm_BB.ChangeDutyCycle(Robot.Stop)

    # Starts the duty cycle for
    # Forwards A,
    # Backwards B
    #
    # Stops all others
    def right(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Go)
        self._pwm_AB.ChangeDutyCycle(Robot.Stop)
        self._pwm_BF.ChangeDutyCycle(Robot.Stop)
        self._pwm_BB.ChangeDutyCycle(Robot.Go)

    # ===================================================
    # Sensor input section
    # ===================================================

    # Checks the light sensor
    #
    # return: bool
    #    true if it sees black, false other wise
    def is_on_line(self):
        return not GPIO.input(self._light_sensor_pin)

    # Triggers an echo of the echo sensor
    # Calculates the time need by the echo
    # Calculates the distance with the time
    #
    # return: float
    #    the distance in cm (at 20 degrees celsius)
    def get_distance(self):
        # Trigger echo
        GPIO.output(self._trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self._trigger_pin, False)

        # Save start time and idle
        start_time = time.time()
        while not GPIO.input(self._echo_pin):
            start_time = time.time()

        print("Pass start loop")

        # Save stop time and idle
        stop_time = time.time()
        while GPIO.input(self._echo_pin):
            stop_time = time.time()
            # If the sensor is too close,
            # it cannot detect distance
            if stop_time - start_time >= 0.04:
                return 0

        # Speed of sound at 20 degrees celsius:
        # 3434.6 cm/s
        return (stop_time - start_time) * 3434.6 / 2

    # ===================================================
    # End section
    # ===================================================

    # This stops all PWM's and
    # cleans all GPIO stuff.
    #
    # The class should be reinitialized after calling it
    def close(self):
        self._pwm_AF.stop()
        self._pwm_AB.stop()
        self._pwm_BF.stop()
        self._pwm_BB.stop()
        GPIO.cleanup()
