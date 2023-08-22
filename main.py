# Created by Arad Maleki
# This is a simplified version of the game "Traffic Racer", a car racing game for mobile phones
# My goal is to create a simple version of this game using Python CLI, and might add GUI later
# This is intended to be used as a playground for training an RL agent to play this game.
import time
import os
import keyboard
import random

NO_CAR_PROB = 0.9
CAR_PROB = 0.05
BUS_PROB = 0.05


def initialize_lanes(lane_count=4, rows_num=10):
    lanes = [[' ' for _ in range(lane_count)] for _ in range(rows_num)]
    lanes[-1][-1] = 'U'
    return lanes


def show_game_state(game_state, step):
    border = '\u2503'
    split = '|'
    middle = '\u2502'
    lane_count = len(game_state[0])
    print(f'Step: {step}')
    for row in game_state:
        print(f'{border}{split.join(row[:lane_count//2])}{middle}{split.join(row[lane_count//2:])}{border}')


def move_left(game_state):
    crashed = False
    index = game_state[-1].index('U')
    if index == 0:
        return game_state, crashed
    if game_state[-1][index-1] == ' ':
        game_state[-1][index-1] = 'U'
        game_state[-1][index] = ' '
    else:
        crashed = True
    return game_state, crashed


def move_right(game_state):
    crashed = False
    index = game_state[-1].index('U')
    if index == len(game_state[-1]) - 1:
        return game_state, crashed
    if game_state[-1][index + 1] == ' ':
        game_state[-1][index + 1] = 'U'
        game_state[-1][index] = ' '
    else:
        crashed = True
    return game_state, crashed


def get_next_step(game_state):
    bus_below = 'B'
    bus_above = 'b'
    car = 'C'
    index = game_state[-1].index('U')
    if game_state[-2][index] != ' ':
        return game_state, True
    for i in range(len(game_state)-1, 0, -1):
        game_state[i] = game_state[i-1].copy()
    game_state[-1][index] = 'U'
    for i in range(len(game_state[0])):
        if game_state[1][i] == bus_below:
            game_state[0][i] = bus_above
            continue
        num = random.random()
        if num < NO_CAR_PROB:
            game_state[0][i] = ' '
        elif num < NO_CAR_PROB + CAR_PROB:
            game_state[0][i] = car
        else:
            game_state[0][i] = bus_below
    if game_state[0][0] != ' ' and game_state[0][1] != ' ' and game_state[0][2] != ' ' and game_state[0][3] != ' ':
        game_state[0][3] = ' '
    return game_state, False


if __name__ == '__main__':
    game_state = initialize_lanes()
    last_step = time.time()
    last_action_time = time.time()
    step = 0
    while True:
        crashed = False
        if time.time() - last_step > 0.3:
            step += 1
            game_state, crash_step = get_next_step(game_state)
            os.system('cls')
            show_game_state(game_state, step)
            last_step = time.time()
            crashed |= crash_step

        if (keyboard.is_pressed('a') or keyboard.is_pressed('left')) and time.time() - last_action_time > 0.2:
            game_state, crash_step = move_left(game_state)
            last_action_time = time.time()
            os.system('cls')
            show_game_state(game_state, step)
            crashed |= crash_step

        if (keyboard.is_pressed('d') or keyboard.is_pressed('right')) and time.time() - last_action_time > 0.2:
            game_state, crash_step = move_right(game_state)
            last_action_time = time.time()
            os.system('cls')
            show_game_state(game_state, step)
            crashed |= crash_step

        if crashed:
            print('You crashed!')
            crashed = True
            break




