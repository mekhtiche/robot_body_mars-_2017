#!/usr/bin/env python
import sys,os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import json
import rospy
import time
import thread
from std_msgs.msg import String
from robot_body.msg import motorSet
from robot_body.msg import motorStat
import robot_tools.robot_tools as tools
from std_msgs.msg import Int16



R = dict()
L = dict()

for servo in range(1, 10):
    R[servo] = rospy.Publisher('servo/R' + str(servo), Int16, queue_size=1)
    L[servo] = rospy.Publisher('servo/L' + str(servo), Int16, queue_size=1)


print "WORD_LISTENNER successful import"
list = ['abs_z', 'bust_y', 'bust_x', 'head_z', 'head_y', 'l_shoulder_y', 'l_shoulder_x', 'l_arm_z', 'l_elbow_y',
            'l_forearm_z', 'r_shoulder_y', 'r_shoulder_x', 'r_arm_z', 'r_elbow_y', 'r_forearm_z']
activemotors = ['abs_z', 'bust_y', 'bust_x']
names = [x for x in list if x not in activemotors]
err_max = 5
pub = dict()
motor = motorSet()
present_pos = {}
present_position = {'Robot': [], 'Right_hand': [], 'Left_hand': []}
buffer = []


def callback(data):
    buffer.append(data.data)

def get_motors(data):
    present_pos[data.name] = data.present_position

def do_sign(buffer):
    right_hand = [200, 200, 100, 100, 200, 100, 100, 100, 100]
    left_hand  = [200, 200, 100, 100, 200, 100, 100, 100, 100]
    while True:
        if buffer:
            try:
                SIGN = buffer.pop(0)
                print 'Doing sign: ' + SIGN
                with open("/home/odroid/catkin_ws/src/robot_body/recording/data_base/" + SIGN + ".json", "r") as sign:
                    movement = json.load(sign)
                    names = movement["actors_NAME"]
                    frames = movement["frame_number"]
                    freq = float(movement["freq"])
                    print freq
                    sign = movement["position"]
                    id = 0
                    max_err = 0
                    for name in names:
                        max_err = max([abs(sign['0']['Robot'][id]-present_pos[name]), max_err])
                        id +=1
                if max_err > err_max:
                    present_position = {'Robot': [present_pos[name] for name in names], 'Right_hand': right_hand, 'Left_hand': left_hand}
                    goal_position = sign['0']
                    pre_sign = tools.build_seq(present_position, goal_position, int(max_err))
                    tools.do_seq(names, max_err, pre_sign, pub, L, R)
                tools.do_seq(names, freq, sign, pub, L, R)
                right_hand = sign[str(frames - 1)]["Right_hand"]
                left_hand  = sign[str(frames - 1)]["Left_hand"]
                if not buffer:
                    present_position = {'Robot': [present_pos[name] for name in names], 'Right_hand': right_hand, 'Left_hand': left_hand}
                    right_hand = [200, 200, 100, 100, 200, 100, 100, 100, 100]
                    left_hand = [200, 200, 100, 100, 200, 100, 100, 100, 100]
                    goal_position = {'Robot': [0 for name in names], 'Right_hand': right_hand, 'Left_hand': left_hand}
                    max_err = max(map(abs, present_position["Robot"]))
                    if max_err > err_max:
                        post_sign = tools.build_seq(present_position, goal_position, int(max_err))
                        tools.do_seq(names, max_err, post_sign, pub, L, R)
                    tools.releas(names, pub, L, R)
            except Exception, err:
                print 'Robot can not start, error is '
                print  err



def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('Word', String, callback=callback)
    list = ['abs_z', 'bust_y', 'bust_x', 'head_z', 'head_y', 'l_shoulder_y', 'l_shoulder_x', 'l_arm_z', 'l_elbow_y',
            'l_forearm_z', 'r_shoulder_y', 'r_shoulder_x', 'r_arm_z', 'r_elbow_y', 'r_forearm_z']
    for name in list:
        pub[name] = rospy.Publisher('poppy/set/' + name, motorSet, queue_size=1)
        rospy.Subscriber('poppy/get/' + name, motorStat, callback=get_motors)
        present_pos[name]=[]
    print 'WORD_LISTENER publishers & subscribers successful Initial'
    rospy.spin()

if __name__ == '__main__':
    thread.start_new_thread(do_sign,(buffer,))
    listener()
