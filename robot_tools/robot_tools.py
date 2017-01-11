#!/usr/bin/python
# -*- coding: UTF-8 -*-  # this is to add arabic coding to python

import time
from robot_body.msg import motorSet
motor = motorSet()

def releas(names,pub, L=None, R=None):
    for name in names:
        motor.compliant = True
        pub[name].publish(motor)
    if (L is not None) & (R is not None):
        multi_servo_set([0]*9, [0]*9, L, R)


def do_seq(names, freq, seq, pub, L=None, R=None):

    for frame in range(len(seq)):
        id = 0
        for name in names:
            motor.compliant = False
            motor.goal_position = seq[str(frame)]['Robot'][id]
            pub[name].publish(motor)
            id += 1
        if (L is not None) & (R is not None):
            multi_servo_set(seq[str(frame)]['Left_hand'], seq[str(frame)]['Right_hand'], L, R)
        time.sleep(1 / float(freq))

def build_seq(curent_pos, pos, max_err):
    pre_sign = {}
    frames = [float(x) / max_err for x in range(max_err + 1)]
    i = 0
    for frame in frames:
        pre_sign[str(i)] = {
            'Robot': [curent_pos[ndx] + frame * frame * (3 - 2 * frame) * (pos[ndx] - curent_pos[ndx])
                      for ndx in range(len(pos))],
            'Right_hand': [200, 200, 100, 100, 200, 100, 100, 100, 100],
            'Left_hand': [200, 200, 100, 100, 200, 100, 100, 100, 100]}
        i += 1
    return pre_sign


def go_to_pos(motors, present_position, goal_position, pub, L=None, R=None):
    err_max = 5
    try:
        max_err = 0
        for id in range(len(goal_position)):
            max_err = max([abs(goal_position[id] - present_position[id]), max_err])
        if max_err > err_max:
            print 'Going to pos'
            preset = build_seq(present_position, goal_position, int(max_err))
            do_seq(motors, max_err, preset, pub, L, R)
        else:
            print 'robot in pos'
            pos = {'0':{'Robot':goal_position}}
            do_seq(motors, 100, pos, pub, L, R)
    except Exception, err:
        print 'Robot can go, error is '
        print  err




def multi_servo_set(Lcommand=None, Rcommand=None, L=None, R=None):

    if Lcommand is not None:
        for servo in range(1,10):
            L[servo].publish(Lcommand[servo - 1])
    if Rcommand is not None:
        for servo in range(1,10):
            R[servo].publish(Rcommand[servo - 1])

def right_servo_set(servo, cmd, R):
    R[servo].publish(cmd)

def left_servo_set(servo, cmd, L):
    L[servo].publish(cmd)