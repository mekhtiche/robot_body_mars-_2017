# robot
The system is tested on ubuntu Xenial armhf
Image avalaible on MEGA Cloud https://mega.nz/#!oIFhUZLa decryption Key: !K1EM5aygbKRRNzjF8cbqpAs_myevqVCU3P7QGwaH8RE
this package need : 

                    ROS Kinetic 

                    I2C tools 
                    
                    pyserial
                    
                    enum
                    
                    python-tk
                    
Installation:

  ROS:
  
    install ROS Kinetic wiki.ros.org/kinetic/Installation/Ubuntu
    
  I2C:


      $ sudo apt-get update
      $ sudo apt-get install python-smbus
      $ sudo apt-get install i2c-tools

    
  
  Python packages:
  
      $ sudo apt-get install python-pip

      $ sudo pip install pyserial

      $ sudo pip install enum

      $ sudo apt-get install python-tk

  now use git clone to download the package:

      $ cd catkin_ws/src

      $ git clone https://github.com/mekhtiche/robot_new.git

      $ cd ..

      $ catkin_make
  
  source the work space
  
      $ sudo nano .bashrc
    
    in the end of the file add "source ~/catkin_ws/devel/setup.bash"
    
    
  To launch the robot:

      $ roslaunch robot Robot_start.launch

  To record sign:

      $ roslaunch robot Recording.launch


  if you have permission denied error you need to change the permission of Servo_driver.py and finger.py

      $ cd catkin_ws/src/robot/driver

      $ chmod 775 Servo_driver.py 

      $ cd catkin_ws/src/robot/recording

      $ chmod 775 finger.py 
