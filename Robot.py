import RPi.GPIO as GPIO


class Robot:

    # static class members
    Stop = 0
    Go = 30
    Frequency = 20

    def __init__(self):

        # Pin vars
        motor_af = 10
        motor_ab = 9
        motor_bf = 8
        motor_bb = 7

        # Setmode for pins
        GPIO.setmode(GPIO.BCM)

        GPIO.cleanup()

        # Setup pins
        GPIO.setup([motor_af, motor_ab, motor_bf, motor_bb], GPIO.OUT)

        # Setup PWM for pins
        self.pwm_AF = GPIO.PWM(motor_af, Robot.Frequency)
        self.pwm_AB = GPIO.PWM(motor_ab, Robot.Frequency)
        self.pwm_BF = GPIO.PWM(motor_bf, Robot.Frequency)
        self.pwm_BB = GPIO.PWM(motor_bb, Robot.Frequency)

        # Start duty cycle with none
        self.pwm_AF.start(Robot.Stop)
        self.pwm_AB.start(Robot.Stop)
        self.pwm_BF.start(Robot.Stop)
        self.pwm_BB.start(Robot.Stop)

    # ===============================================
    # Robot control section
    # ===============================================

    def stop(self):
        self.pwm_AF.ChangeDutyCycle(Robot.Stop)
        self.pwm_AB.ChangeDutyCycle(Robot.Stop)
        self.pwm_BF.ChangeDutyCycle(Robot.Stop)
        self.pwm_BB.ChangeDutyCycle(Robot.Stop)

    def forward(self):
        self.pwm_AF.ChangeDutyCycle(Robot.Go)
        self.pwm_AB.ChangeDutyCycle(Robot.Stop)
        self.pwm_BF.ChangeDutyCycle(Robot.Go)
        self.pwm_BB.ChangeDutyCycle(Robot.Stop)

    def back(self):
        self.pwm_AF.ChangeDutyCycle(Robot.Stop)
        self.pwm_AB.ChangeDutyCycle(Robot.Go)
        self.pwm_BF.ChangeDutyCycle(Robot.Stop)
        self.pwm_BB.ChangeDutyCycle(Robot.Go)

    def left(self):
        self.pwm_AF.ChangeDutyCycle(Robot.Stop)
        self.pwm_AB.ChangeDutyCycle(Robot.Go)
        self.pwm_BF.ChangeDutyCycle(Robot.Go)
        self.pwm_BB.ChangeDutyCycle(Robot.Stop)

    def right(self):
        self.pwm_AF.ChangeDutyCycle(Robot.Go)
        self.pwm_AB.ChangeDutyCycle(Robot.Stop)
        self.pwm_BF.ChangeDutyCycle(Robot.Stop)
        self.pwm_BB.ChangeDutyCycle(Robot.Go)

    def close(self):
        self.pwm_AF.stop()
        self.pwm_AB.stop()
        self.pwm_BF.stop()
        self.pwm_BB.stop()
        GPIO.cleanup()
