import Robot as Robot
import time

# Initialize Robot.py API
robot = Robot.Robot(4, 23, 22)

# Test logic
try:

    _id = input("Start id?: ")

    if _id == "0":
        while True:
            time.sleep(0.5)

            distance = robot.get_distance()
            if robot.is_on_line() and distance >= 10:
                robot.forward()
            else:
                robot.stop()
    else:
        while True:
            time.sleep(0.5)

            distance = robot.get_distance()
            if distance >= 10:
                robot.forward()
            else:
                robot.stop()

except KeyboardInterrupt:
    robot.close()
