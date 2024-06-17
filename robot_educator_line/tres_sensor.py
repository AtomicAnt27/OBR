#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Educator Color Sensor Down Program
----------------------------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#robot
"""

from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

# Initialize the color sensors.
left_sensor = ColorSensor(Port.S3)
middle_sensor = ColorSensor(Port.S2)
right_sensor = ColorSensor(Port.S1)

# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=62.4, axle_track=104)

# Calculate the light threshold. Choose values based on your measurements.
BLACK = 7
WHITE = 85
threshold = (BLACK + WHITE) / 2

# Set the drive speed at 100 millimeters per second.
DRIVE_SPEED = 100

# Set the gain of the proportional line controller. This means that for every
# percentage point of light deviating from the threshold, we set the turn
# rate of the drivebase to 1.2 degrees per second.
PROPORTIONAL_GAIN = 2.2

# Weights for the sensors
LEFT_WEIGHT = -2
MIDDLE_WEIGHT = 0
RIGHT_WEIGHT = 2

prev_status = ""
status = "iniciado"
prev_left = Color.WHITE
prev_middle = Color.WHITE
prev_right = Color.WHITE

# Start following the line endlessly.
while True:
    # Calculate the deviation from the threshold for each sensor.
    left_deviation = left_sensor.reflection() - threshold
    middle_deviation = middle_sensor.reflection() - threshold
    right_deviation = right_sensor.reflection() - threshold

    # Combine deviations using the weights.
    combined_deviation = (LEFT_WEIGHT * left_deviation +
                          MIDDLE_WEIGHT * middle_deviation +
                          RIGHT_WEIGHT * right_deviation)

    # Calculate the turn rate.
    turn_rate = PROPORTIONAL_GAIN * combined_deviation
    
    # Set the drive base speed and turn rate.
    #if (left_sensor.color() == Color.GREEN and prev_left != Color.BLACK):
    #    robot.drive(DRIVE_SPEED, -100)
    #    print("[GREEN] virar esquerda")
    #    wait(50)
    #elif (right_sensor.color() == Color.GREEN and prev_right != Color.BLACK):
    #    robot.drive(DRIVE_SPEED, 100)
    #    print("[GREEN] virar direita")
    #    wait(50)
    if (left_sensor.reflection() > WHITE and middle_sensor.reflection() > WHITE and right_sensor.reflection() > WHITE):
        status = "indo na fé"
        robot.drive(DRIVE_SPEED, 0)
    elif (abs(turn_rate) < 100):
        robot.drive(DRIVE_SPEED, turn_rate)
        status = "indo normal"
    else:
        robot.drive(50, turn_rate)
        status = "baixa veloc"
    # You can wait for a short time or do other things in this loop.

    if (left_sensor.reflection() < BLACK and middle_sensor.reflection() < BLACK and right_sensor.reflection() < BLACK):
        # robot.drive(0, 0)
        robot.drive(-200, 0)
        wait(200)
        robot.drive(0, 0)
        left_color = left_sensor.color()
        right_color = right_sensor.color()
        print(left_color)
        print(right_color)
        if (left_color == Color.GREEN and right_color == Color.GREEN):
            print("RETO")
            robot.drive(100, 0)
            wait(200)
        elif (left_color == Color.GREEN):
            print("ESQUERDA")
            robot.drive(100, 150)
            wait(800)
        elif (right_color == Color.GREEN):
            print("DIREITA")
            robot.drive(100, -150)
            wait(800)
        else:
            print("NADA")
            robot.drive(100, 0)
            wait(200)

    if (status != prev_status):
        print(status)

    prev_status = status
    #prev_left = left_sensor.color()
    #prev_middle = middle_sensor.color()
    #prev_right = right_sensor.color()
    wait(10)
