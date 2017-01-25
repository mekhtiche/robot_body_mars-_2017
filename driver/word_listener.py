#!/usr/bin/env python
import sys,os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import json
import rospy
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
torso = ['abs_z', 'bust_y', 'bust_x']
right_hand_motors = ['r_shoulder_y', 'r_shoulder_x', 'r_arm_z', 'r_elbow_y', 'r_forearm_z']
left_hand_motors  = ['l_shoulder_y', 'l_shoulder_x', 'l_arm_z', 'l_elbow_y', 'l_forearm_z']
names = [x for x in list if x not in torso]
pub = dict()
motor = motorSet()
present_pos = {}
present_position = {'Robot': [], 'Right_hand': [], 'Left_hand': []}
buffer = []

def callback(data):
    buffer.append(data.data)

def get_motors(data):
    present_pos[data.name] = data

def do_sign(buffer):
    right_hand = [200, 200, 100, 100, 200, 100, 100, 100, 100]
    left_hand  = [200, 200, 100, 100, 200, 100, 100, 100, 100]
    old_motors = []
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
                    sign = movement["position"]
                    motor_to_release = [mtr for mtr in old_motors if (mtr not in names) & (mtr not in torso)]
                    if motor_to_release:
                        goal_position = {"Robot": sign['0']['Robot']+[0 for name in motor_to_release],
                            "Right_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100] if [mtr for mtr in motor_to_release if mtr in right_hand_motors]
                            else sign['0']['Right_hand'],
                            "Left_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100] if [mtr for mtr in motor_to_release if mtr in left_hand_motors]
                            else sign['0']['Left_hand']}
                    else:
                        goal_position = sign['0']
                    tools.go_to_pos(names+motor_to_release, present_pos, goal_position, pub, L, R, left_hand, right_hand)
                    tools.releas(motor_to_release, pub)
                    tools.do_seq(names, freq, sign, pub, L, R)
                    right_hand = sign[str(frames - 1)]["Right_hand"]
                    left_hand  = sign[str(frames - 1)]["Left_hand"]
                    old_motors = names
                    if not buffer:
                        goal_position = {'Robot': [0 for name in names],
                                         'Right_hand': [200, 200, 100, 100, 200, 100, 100, 100, 100],
                                         'Left_hand': [200, 200, 100, 100, 200, 100, 100, 100, 100]}
                        tools.go_to_pos(names, present_pos, goal_position, pub, L, R, left_hand, right_hand)
                        right_hand = [200, 200, 100, 100, 200, 100, 100, 100, 100]
                        left_hand = [200, 200, 100, 100, 200, 100, 100, 100, 100]
                        tools.releas(names, pub, L, R)
                        old_motors = []
            except Exception, err:
                print 'Robot can not start, error is '
                print  err



def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('Word', String, callback=callback)
    for name in list:
        pub[name] = rospy.Publisher('poppy/set/' + name, motorSet, queue_size=1)
        rospy.Subscriber('poppy/get/' + name, motorStat, callback=get_motors)
        present_pos[name]=motorStat
    print 'WORD_LISTENER publishers & subscribers successful Initial'
    rospy.spin()

if __name__ == '__main__':
    thread.start_new_thread(do_sign,(buffer,))
    listener()
