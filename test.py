import Robot as Robot
import time

# Initialize Robot.py API
robot = Robot.Robot(4, 23, 22)

# Test logic
try:
    while True:
        time.sleep(0.5)

        distance = robot.get_distance()
        print(distance)
        if robot.is_on_line() and distance >= 1:
            robot.forward()
        else:
            robot.stop()

except KeyboardInterrupt:
    robot.close()
