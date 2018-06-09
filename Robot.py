import RPi.GPIO as GPIO
import time


class Robot:

    # Static class members
    Stop = 0
    Go = 30
    Frequency = 20

    def __init__(self, light_sensor_pin, echo_pin, trigger_pin):

        # Pin vars
        motor_af = 10
        motor_ab = 9
        motor_bf = 8
        motor_bb = 7

        self._light_sensor_pin = light_sensor_pin
        self._echo_pin = echo_pin
        self._trigger_pin = trigger_pin

        # GPIO.setwarnings(False)
        GPIO.cleanup()

        # Setmode for pins
        GPIO.setmode(GPIO.BCM)

        # Setup pins
        GPIO.setup([motor_af, motor_ab, motor_bf, motor_bb, trigger_pin], GPIO.OUT)
        GPIO.setup([light_sensor_pin, echo_pin], GPIO.IN)

        # Setup PWM for pins
        self._pwm_AF = GPIO.PWM(motor_af, Robot.Frequency)
        self._pwm_AB = GPIO.PWM(motor_ab, Robot.Frequency)
        self._pwm_BF = GPIO.PWM(motor_bf, Robot.Frequency)
        self._pwm_BB = GPIO.PWM(motor_bb, Robot.Frequency)

        # Start duty cycle with none
        self._pwm_AF.start(Robot.Stop)
        self._pwm_AB.start(Robot.Stop)
        self._pwm_BF.start(Robot.Stop)
        self._pwm_BB.start(Robot.Stop)

        GPIO.output(trigger_pin, False)

    # ===============================================
    # Robot control section
    # ===============================================

    def stop(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Stop)
        self._pwm_AB.ChangeDutyCycle(Robot.Stop)
        self._pwm_BF.ChangeDutyCycle(Robot.Stop)
        self._pwm_BB.ChangeDutyCycle(Robot.Stop)

    def forward(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Go)
        self._pwm_AB.ChangeDutyCycle(Robot.Stop)
        self._pwm_BF.ChangeDutyCycle(Robot.Go)
        self._pwm_BB.ChangeDutyCycle(Robot.Stop)

    def back(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Stop)
        self._pwm_AB.ChangeDutyCycle(Robot.Go)
        self._pwm_BF.ChangeDutyCycle(Robot.Stop)
        self._pwm_BB.ChangeDutyCycle(Robot.Go)

    def left(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Stop)
        self._pwm_AB.ChangeDutyCycle(Robot.Go)
        self._pwm_BF.ChangeDutyCycle(Robot.Go)
        self._pwm_BB.ChangeDutyCycle(Robot.Stop)

    def right(self):
        self._pwm_AF.ChangeDutyCycle(Robot.Go)
        self._pwm_AB.ChangeDutyCycle(Robot.Stop)
        self._pwm_BF.ChangeDutyCycle(Robot.Stop)
        self._pwm_BB.ChangeDutyCycle(Robot.Go)

    # ===============================================
    # Sensor inputs
    # ===============================================

    def is_on_line(self):
        return not GPIO.input(self._light_sensor_pin)

    def trigger_echo(self):
        GPIO.output(self._trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self._trigger_pin, False)

    def get_distance(self):
        self.trigger_echo()
        start_time = time.time()

        while not GPIO.input(self._echo_pin):
            start_time = time.time()

        while GPIO.input(self._echo_pin):
            stop_time = time.time()

            # If the sensor is too close, it cannot detect it
            if stop_time - start_time >= 0.04:
                stop_time = start_time
                break

        # Speed of sound at 20 degrees celsius 3434.6 cm/s
        return (stop_time - start_time) * 3434.6 / 2

    # ===============================================
    # Close and destroy (Class needs to be reinitialized)
    # ===============================================

    def close(self):
        self._pwm_AF.stop()
        self._pwm_AB.stop()
        self._pwm_BF.stop()
        self._pwm_BB.stop()
        GPIO.cleanup()
