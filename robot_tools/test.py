import time
import pypot.robot

print 'ROBOT succiful import'


robot = pypot.robot.from_config(pypot.robot.config.test_config)


print "robot started"


while True:
    for m in robot.motors:
        print m.present_position