import Robot as Robot
import time

print("Initialize robot API")
# Initialize Robot.py API
robot = Robot.Robot(4, 24, 22)
print("Finished initializing")

# Test logic
try:
    print("Start loop")
    while True:
        time.sleep(0.1)

        print("Send echo")
        distance = robot.get_distance()
        print(distance)
        if robot.is_on_line() and distance >= 10:
            robot.forward()
        else:
            robot.stop()

except KeyboardInterrupt:
    robot.close()
