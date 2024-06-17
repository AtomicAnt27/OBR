#!/usr/bin/env pybricks-micropython


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color, Direction, Stop
from pybricks.tools import wait

# Inicializar o EV3
ev3 = EV3Brick()

# Inicializar motores
motor_left = Motor(Port.A, Direction.CLOCKWISE)
motor_right = Motor(Port.B, Direction.CLOCKWISE)

# Inicializar sensores de cor
color_sensor_left = ColorSensor(Port.S3)
color_sensor_right = ColorSensor(Port.S1)

# Constantes
BLACK = 10  # Limiar para a cor preta (ajuste conforme necessário)
WHITE = 90  # Limiar para a cor branca (ajuste conforme necessário)
GREEN = 50  # Limiar para a cor verde (ajuste conforme necessário)
THRESHOLD = (BLACK + WHITE) / 2

# Função para seguir linha
def follow_line():
    while True:
        left_reflection = color_sensor_left.reflection()
        right_reflection = color_sensor_right.reflection()
        
        if left_reflection < THRESHOLD and right_reflection > THRESHOLD:
            # Corrigir para a direita
            motor_left.run(150)
            motor_right.run(50)
        elif left_reflection > THRESHOLD and right_reflection < THRESHOLD:
            # Corrigir para a esquerda
            motor_left.run(50)
            motor_right.run(150)
        else:
            # Ir em frente
            motor_left.run(100)
            motor_right.run(100)
        
        direction = detect_green()
        if direction:
            handle_crossing(direction)
            break

# Função para detectar quadrados verdes
def detect_green():
    left_color = color_sensor_left.color()
    right_color = color_sensor_right.color()
    
    if left_color == Color.GREEN and right_color == Color.GREEN:
        # Quadrados verdes em ambos os lados
        return 'BOTH'
    elif left_color == Color.GREEN:
        # Quadrado verde à esquerda
        return 'LEFT'
    elif right_color == Color.GREEN:
        # Quadrado verde à direita
        return 'RIGHT'
    else:
        return None

# Função para tomar decisão no cruzamento
def handle_crossing(direction):
    if direction == 'LEFT':
        # Virar à esquerda
        motor_left.run_angle(150, 360, then=Stop.HOLD, wait=True)
        motor_right.run_angle(150, -360, then=Stop.HOLD, wait=True)
    elif direction == 'RIGHT':
        # Virar à direita
        motor_left.run_angle(150, -360, then=Stop.HOLD, wait=True)
        motor_right.run_angle(150, 360, then=Stop.HOLD, wait=True)
    elif direction == 'BOTH':
        # Virar 180 graus
        motor_left.run_angle(150, 720, then=Stop.HOLD, wait=True)
        motor_right.run_angle(150, -720, then=Stop.HOLD, wait=True)
    
    # Retomar seguimento de linha após cruzamento
    follow_line()

# Loop principal
while True:
    follow_line()
    wait(100)
