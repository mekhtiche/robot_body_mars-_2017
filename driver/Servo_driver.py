#!/usr/bin/env python
import sys,os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import rospy
import time
from robot_body.msg import servoSet
import serial
import struct
# from servo.Adafruit_PWM_Servo_Driver import PWM
print "SERVO_DRIVER successful import"
hand = ['Right', 'Left']

srl = serial.Serial('/dev/ttySAC0', 115200)


def doIt(Rcmd, Lcmd):
    # print srl
    if Rcmd is not None:
        srl.write(struct.pack('cBBBBBBBBB', "R", Rcmd[0] - 50, Rcmd[1] - 50, Rcmd[2] - 50,
                              Rcmd[3] - 50, Rcmd[4] - 50, Rcmd[5] - 50,
                              Rcmd[6] - 50, Rcmd[7] - 50, Rcmd[8] - 50))
#    if Rcmd is not None:
#        for i in range(9):
#            srl.write(struct.pack('cBB', "r", i + 1, Rcmd[i] - 50))

    time.sleep(0.01)

    if Lcmd is not None:
        srl.write(struct.pack('cBBBBBBBBB', "L", Lcmd[0] - 50, Lcmd[1] - 50, Lcmd[2] - 50,
                              Lcmd[3] - 50, Lcmd[4] - 50, Lcmd[5] - 50,
                              Lcmd[6] - 50, Lcmd[7] - 50, Lcmd[8] - 50))

#    if Lcmd is not None:
#        for i in range(9):
#            srl.write(struct.pack('cBB', "l", i + 1, Lcmd[i] - 50))
    


def callback(data):

    doIt(data.right_cmd, data.left_cmd)





if __name__ == '__main__':

    rospy.init_node('Fingers_driver', anonymous=True)
    rospy.Subscriber('servo/cmd', servoSet, callback=callback)
    print 'SERVO_DRIVER publishers & subscribers successful Initial'
    rospy.spin()
    print 'Closing the serial port'
    
