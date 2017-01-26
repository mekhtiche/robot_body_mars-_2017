#!/usr/bin/env python
import sys,os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import thread
import time
import rospy
from robot_body.msg import motorStat
from robot_body.msg import motorSet
from std_msgs.msg import String
import pypot.robot
import robot_tools.robot_tools as tools


print 'ROBOT succiful import'

activemotors = {'abs_z', 'bust_y', 'bust_x'}
robot = pypot.robot.from_config(pypot.robot.config.robot_config)
err_max = 10

pupStat = rospy.Publisher('Robot_status', String, queue_size=10)

pub = dict()




def Openning():
    print('Starting the ROBOT')
    try:
        right_hand = [200, 200, 100, 100, 200, 100, 100, 100, 100]
        left_hand = [200, 200, 100, 100, 200, 100, 100, 100, 100]
        present_position = {"Robot": [m.present_position for m in robot.torso], 'Right_hand': right_hand, 'Left_hand': left_hand}
        goal_position = {"Robot": [0 for m in robot.torso], 'Right_hand': right_hand, 'Left_hand': left_hand}
        max_err = max(map(abs,present_position["Robot"]))
        if max_err > err_max:
            preset = tools.build_seq(present_position, goal_position, int(max_err))
            for frame in range(len(preset)):
                id = 0
                for m in robot.torso:
                    m.compliant = False
                    m.goal_position = preset[str(frame)]['Robot'][id]
                    id+=1
                time.sleep(1/max_err)
        else:
            print 'robot in initial pos'
            for m in robot.torso:
                m.compliant = False

        robot_status = 'Ready'
        pupStat.publish(robot_status)
        print('Robot started Successful')
    except Exception, err:
        print 'Robot can not start, error is '
        print  err
        robot_status = err.message
        pupStat.publish(robot_status)


def Closing():
    try:
        print 'Closing the robot'
        for m in robot.motors:
            m.compliant = True
        robot.close()
        robot_status = 'Closed'
        pupStat.publish(robot_status)
        print 'Robot Closed'
    except Exception, err:
        print err


def callback(data, m):
    m.compliant = data.compliant
    m.goal_position = data.goal_position


def publisher():
    motor = motorStat()
    while not rospy.is_shutdown():

        for m in robot.motors:
            motor.id = m.id
            motor.name = m.name
            motor.present_position = m.present_position
            motor.goal = m.goal_position
            motor.present_error = m.goal_position - m.present_position
            motor.present_speed = m.present_speed
            motor.present_load = m.present_load
            motor.present_voltage = m.present_voltage
            motor.present_temperature = m.present_temperature
            motor.compliant = m.compliant
            motor.max_angle = m.angle_limit[0]
            motor.min_angle = m.angle_limit[1]
            motor.direction = m.direct
            motor.model = m.model
            motor.offset = m.offset
            motor.max_load = m.torque_limit
            pub[m.name].publish(motor)
            if (motor.present_temperature > 65):
                robot_status = motor.name + ' is OVERHEATED, Present Tempirature is ' + str(motor.present_temperature)
                pupStat.publish(robot_status)
                print robot_status
                Closing()
                return
        time.sleep(0.001)

if __name__ == '__main__':

    rospy.init_node('robot_node', anonymous=True)
    Openning()
    for m in robot.motors:
        pub[m.name] = rospy.Publisher('poppy/get/'+ m.name, motorStat, queue_size=1)
        rospy.Subscriber('poppy/set/'+ m.name, motorSet, callback=callback, callback_args=m)
    print 'ROBOT publishers & subscribers successful initial'
    thread.start_new_thread(publisher, ())
    rospy.spin()
    Closing()


