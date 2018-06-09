import Robot as Robot
import time

robot = Robot.Robot(4, 24, 23)

try:
    while True:
        time.sleep(0.2)

        distance = robot.get_distance()
        if robot.is_on_line() and distance >= 10:
            robot.forward()
        else:
            robot.stop()

except KeyboardInterrupt:
    robot.close()