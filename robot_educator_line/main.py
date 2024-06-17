#!/usr/bin/env pybricks-micropython


from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait
from pybricks.robotics import DriveBase

# Constantes
DRIVE_SPEED = 150

# Inicializar motores
motor_left = Motor(Port.A)
motor_right = Motor(Port.B)
robot = DriveBase(motor_left, motor_right, wheel_diameter=62.4, axle_track=104)

# Inicializar sensores de cor
sensor_left = ColorSensor(Port.S3)
sensor_right = ColorSensor(Port.S1)

left_prev = Color.WHITE
right_prev = Color.WHITE

while True:
    left_color = sensor_left.color()
    right_color = sensor_right.color()

    if (left_color == Color.WHITE and right_color == Color.WHITE):
        robot.drive(DRIVE_SPEED, 0)
        print('[linha] reto')
    elif (left_color == Color.WHITE and right_color == Color.BLACK):
        robot.drive(DRIVE_SPEED//2, -100)
        print('[linha] ajustar direita')
    elif (right_color == Color.WHITE and left_color == Color.BLACK):
        robot.drive(DRIVE_SPEED//2, 100)
        print('[linha] ajustar esquerda')
    elif (right_color == Color.GREEN and left_color == Color.WHITE and right_prev != Color.BLACK):
        print('[cruzamento] virar direita')
        robot.drive(DRIVE_SPEED//2, -100)
        wait(500)
    elif (left_color == Color.GREEN and right_color == Color.WHITE and left_prev != Color.BLACK):
        print('[cruzamento] virar esquerda')
        robot.drive(DRIVE_SPEED//2, 100)
        wait(500)
    elif (left_color == Color.GREEN and right_color == Color.GREEN and left_prev != Color.BLACK and right_prev != Color.BLACK):
        print('[cruzamento] virar 180')
        robot.drive(DRIVE_SPEED//2, 100)
        wait(1000)
    else:
        print('sei la man - to confuso')
    
    left_prev = left_color
    right_prev = right_color