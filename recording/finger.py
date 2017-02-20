#!/usr/bin/python
import time
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
from Tkinter import *
import rospy
from std_msgs.msg import Int16
from robot_body.msg import Emotion
import robot_tools.robot_tools as tools
import json
import numpy as np




R = dict()
L = dict()


emotions=['show text', 'normal', 'happy1', 'happy2', 'angry', 'play', 'robot', 'yellow']
show=Emotion()
for servo in range(1, 10):
    R[servo] = rospy.Publisher('servo/R' + str(servo), Int16, queue_size=10)
    L[servo] = rospy.Publisher('servo/L' + str(servo), Int16, queue_size=10)
HEAD_EMO = rospy.Publisher('poppy/face/emotion', Emotion, queue_size=10)
HEAD_TXT = rospy.Publisher('poppy/face/text', Emotion, queue_size=10)


def __init__(master, movement, motor, pub):
    master.geometry('915x855')
    master.title('SETTING THE HAND')
    title = Frame(master)
    title.grid(row=0, column=0, columnspan=3, sticky=W+E+N+S)
    info = Label(title, justify=LEFT, text='play the recorded sign using the slider in the blue section and set the hand configuration using \n'
                             'the sliders below than click "Set Pos" to record it, when you done all the hand sets click on \n'
                             '"Build & Play" to build the movement than save it. \n '
                             'you can also use "Delete before" and "Delete After" to delete unnecessary frames.')
    info.pack()
    lefthand = Frame(master, bg = "red")
    lefthand.grid(row=1, column=0)
    righthand = Frame(master, bg = "green")
    righthand.grid(row=1, column=2)
    medButt = Frame(master,bg = "blue")
    medButt.grid(row=1, column=1)
    buttfram = Frame(master, bg="blue")
    buttfram.grid(row=2, column=0, columnspan=3, sticky=W+E+N+S)
    master.closing = False
    master.movement = movement
    active_motors = master.movement['actors_NAME']
    dead_motors = [name for name in motor if name not in active_motors]
    print('Starting the ROBOT')
    goal_position = master.movement['position']['0']
    tools.go_to_pos(active_motors, motor, goal_position, pub)
    goal_position = {"Robot": [0 for name in dead_motors],
                     "Right_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100],
                     "Left_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100]}
    tools.go_to_pos(dead_motors, motor, goal_position, pub)
    print('Robot started')



#//////////////////////////////////////////////////////////////////////////LEFT  ARM////////////////////////////////////////////////////////////////////////
    def LgetValue1(event):
        tools.left_servo_set(1, master.Lwrist_V.get(), L)

    master.Lwrist_V = Scale(lefthand, label = "wrist_V N:1", from_=100, to =300, orient = HORIZONTAL, length = 300, command = LgetValue1)
    master.Lwrist_V.set(200)
    master.Lwrist_V.pack()

    def LgetValue2(event):
        tools.left_servo_set(2, master.Lwrist_H.get(), L)

    master.Lwrist_H = Scale(lefthand, label = "wrist_H N:2", from_=100, to =300, orient = HORIZONTAL, length = 300, command = LgetValue2)
    master.Lwrist_H.set(200)
    master.Lwrist_H.pack()

    def LgetValue3(event):
        tools.left_servo_set(3, master.Lthump_J.get(), L)

    master.Lthump_J = Scale(lefthand, label = "Thump_J N:3", from_=100, to =300, orient = HORIZONTAL, length = 300, command = LgetValue3)
    master.Lthump_J.set(100)
    master.Lthump_J.pack()

    def LgetValue4(event):
        tools.left_servo_set(4, master.Lthump.get(), L)

    master.Lthump = Scale(lefthand, label = "Thump N:4", from_=100, to =300, orient = HORIZONTAL, length = 300, command = LgetValue4)
    master.Lthump.set(100)
    master.Lthump.pack()

    def LgetValue5(event):
        tools.left_servo_set(5, master.LOpen.get(), L)

    master.LOpen = Scale(lefthand, label = "Open N:5", from_=100, to =300, orient = HORIZONTAL, length = 300, command = LgetValue5)
    master.LOpen.set(200)
    master.LOpen.pack()

    def LgetValue6(event):
        tools.left_servo_set(6, master.Lindex.get(), L)

    master.Lindex = Scale(lefthand, label = "Index N:6", from_=100, to =300, orient = HORIZONTAL, length = 300, command = LgetValue6)
    master.Lindex.set(100)
    master.Lindex.pack()

    def LgetValue7(event):
        tools.left_servo_set(7, master.Lmajor.get(), L)

    master.Lmajor = Scale(lefthand, label = "Major N:7", from_=100, to =300, orient = HORIZONTAL, length = 300, command = LgetValue7)
    master.Lmajor.set(100)
    master.Lmajor.pack()

    def LgetValue8(event):
        tools.left_servo_set(8, master.Lring.get(), L)

    master.Lring = Scale(lefthand, label = "Ring N:8", from_=100, to =300, orient = HORIZONTAL, length = 300, command = LgetValue8)
    master.Lring.set(100)
    master.Lring.pack()

    def LgetValue9(event):
        tools.left_servo_set(9, master.Lauri.get(), L)

    master.Lauri = Scale(lefthand, label = "Auriculaire N:9", from_=100, to =300, orient = HORIZONTAL, length = 300, command = LgetValue9)
    master.Lauri.set(100)
    master.Lauri.pack()
#//////////////////////////////////////////////////////////////////////////LEFT  ARM////////////////////////////////////////////////////////////////////////


#//////////////////////////////////////////////////////////////////////////RIGHT ARM////////////////////////////////////////////////////////////////////////
    def RgetValue1(event):
        tools.right_servo_set(1, master.Rwrist_V.get(), R)


    master.Rwrist_V = Scale(righthand, label="wrist_V N:1", from_=100, to =300, orient=HORIZONTAL, length=300,
                            command=RgetValue1)
    master.Rwrist_V.set(200)
    master.Rwrist_V.pack()


    def RgetValue2(event):
        tools.right_servo_set(2, master.Rwrist_H.get(), R)


    master.Rwrist_H = Scale(righthand, label="wrist_H N:2", from_=100, to =300, orient=HORIZONTAL, length=300,
                            command=RgetValue2)
    master.Rwrist_H.set(200)
    master.Rwrist_H.pack()


    def RgetValue3(event):
        tools.right_servo_set(3, master.Rthump_J.get(), R)


    master.Rthump_J = Scale(righthand, label="Thump_J N:3", from_=100, to =300, orient=HORIZONTAL, length=300,
                            command=RgetValue3)
    master.Rthump_J.set(100)
    master.Rthump_J.pack()


    def RgetValue4(event):
        tools.right_servo_set(4, master.Rthump.get(), R)


    master.Rthump = Scale(righthand, label="Thump N:4", from_=100, to =300, orient=HORIZONTAL, length=300, command=RgetValue4)
    master.Rthump.set(100)
    master.Rthump.pack()


    def RgetValue5(event):
        tools.right_servo_set(5, master.ROpen.get(), R)


    master.ROpen = Scale(righthand, label="Open N:5", from_=100, to =300, orient=HORIZONTAL, length=300, command=RgetValue5)
    master.ROpen.set(200)
    master.ROpen.pack()


    def RgetValue6(event):
        tools.right_servo_set(6, master.Rindex.get(), R)


    master.Rindex = Scale(righthand, label="Index N:6", from_=100, to =300, orient=HORIZONTAL, length=300, command=RgetValue6)
    master.Rindex.set(100)
    master.Rindex.pack()


    def RgetValue7(event):
        tools.right_servo_set(7, master.Rmajor.get(), R)


    master.Rmajor = Scale(righthand, label="Major N:7", from_=100, to =300, orient=HORIZONTAL, length=300, command=RgetValue7)
    master.Rmajor.set(100)
    master.Rmajor.pack()


    def RgetValue8(event):
        tools.right_servo_set(8, master.Rring.get(), R)


    master.Rring = Scale(righthand, label="Ring N:8", from_=100, to =300, orient=HORIZONTAL, length=300, command=RgetValue8)
    master.Rring.set(100)
    master.Rring.pack()


    def RgetValue9(event):
        tools.right_servo_set(9, master.Rauri.get(), R)


    master.Rauri = Scale(righthand, label="Auri N:9", from_=100, to =300, orient=HORIZONTAL, length=300, command=RgetValue9)
    master.Rauri.set(100)
    master.Rauri.pack()
#//////////////////////////////////////////////////////////////////////////RIGHT ARM////////////////////////////////////////////////////////////////////////


    def setframe(event):
        master.frm = master.recSlider.get()

        tools.do_seq(active_motors, 100, {'0':master.movement['position'][str(master.frm)]}, pub)

        if master.Lrec.get() == 0:
            tools.multi_servo_set(master.movement['position'][str(master.frm)]['Left_hand'], None, L)

        if master.Rrec.get() == 0:
            tools.multi_servo_set(None, master.movement['position'][str(master.frm)]['Right_hand'], None, R)


    def DelBefor():

        if tkMessageBox.askyesno(title='Warning', message='Warning: Do you want to delete the sequanses Befor the the frame ' + str(master.frm) + '?', parent=master):
            mov = {} #master.movement['position']

            newfrm=0
            for frm in range(master.frm, master.movement['frame_number'], 1):
                mov[str(newfrm)] = master.movement['position'][str(frm)]
                newfrm +=1
            master.movement.pop('position')
            master.movement['position'] = mov
            #master.movement['position'] = master.movement['position'][str(0):str(master.frm)]
            master.movement['frame_number']=newfrm
            master.recSlider.config(to=master.movement['frame_number'] - 1)
            master.recSlider.set(0)
            save.config(state=NORMAL)

    def DelAfter():

        if tkMessageBox.askyesno(title='Warning', message='Warning: Do you want to delete the sequanses After the the frame '+ str(master.frm) + '?', parent=master):
            for frm in range(master.frm, master.movement['frame_number'], 1):
                master.movement['position'].pop(str(frm))

            master.movement['frame_number'] = master.frm
            master.recSlider.config(to=master.movement['frame_number'] - 1)
            save.config(state=NORMAL)

    def closecall():
        if save['state']==NORMAL:
            decision = tkMessageBox.askyesnocancel('CLOSE', "Do you want to save sign: ", parent=master)
            if decision:
                savecall()
            elif decision is None:
                return
        print 'closing the robot'
        tools.multi_servo_set([200, 200, 100, 100, 200, 100, 100, 100, 100], [200, 200, 100, 100, 200, 100, 100, 100, 100], L, R)
        goal_position = {"Robot": [0 for name in dead_motors],
                         "Right_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100],
                         "Left_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100]}
        tools.go_to_pos(dead_motors, motor, goal_position, pub)
        goal_position = {"Robot": [0 for name in active_motors],
                         "Right_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100],
                         "Left_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100]}
        tools.go_to_pos(active_motors, motor, goal_position, pub)
        tools.releas(active_motors, pub, L, R)
        print 'Robot Closed'

        master.destroy()

    def savecall():
        print 'saving movement'
        saveFile = tkFileDialog.asksaveasfilename(defaultextension="json", initialdir="/home/odroid/catkin_ws/src/robot_body/recording/data_base", parent=master)
        if not saveFile:
            return None
        if list(master.emotion_list.curselection()):
            if master.emotion_list.get(master.emotion_list.curselection())=='show text':
                master.movement['text']=master.text.get()
            else:
                master.movement['emotion_name']=master.emotion_list.get(master.emotion_list.curselection())
            master.movement['emotion_time']=master.emotion_time.get()
        with open(saveFile, "w") as record:
            json.dump(master.movement, record)
        print 'saved'

    def setcall():
        print 'seting'
        master.lefthandpos = [master.Lwrist_V.get(), master.Lwrist_H.get(), master.Lthump_J.get(), master.Lthump.get(), master.LOpen.get(),
               master.Lindex.get(), master.Lmajor.get(), master.Lring.get(), master.Lauri.get()]
        master.righthandpos = [master.Rwrist_V.get(), master.Rwrist_H.get(), master.Rthump_J.get(), master.Rthump.get(), master.ROpen.get(),
                              master.Rindex.get(), master.Rmajor.get(), master.Rring.get(), master.Rauri.get()]
        master.movement['position'][str(master.frm)]['Left_hand'] = master.lefthandpos
        master.movement['position'][str(master.frm)]['Right_hand'] = master.righthandpos
        if master.frm not in master.setted_frame:
            master.setted_frame.append(master.frm)
            list(set(master.setted_frame))  # sort the list
        if ~master.needToBuild:
            master.needToBuild = True

        clear.config(state=NORMAL)
        print 'done'

    def find_smth_win():
        winSize = master.setted_frame[len(master.setted_frame)-1] - master.setted_frame[0]
        for i in range(len(master.setted_frame)-1):
            winSize = min(master.setted_frame[i+1]-master.setted_frame[i], winSize)
        return winSize;

    def buildPlay():
        if master.needToBuild:
            print 'building'
            #if master.setted_frame[0] != 0:
             #   master.setted_frame.insert(0, 0)
                #master.movement['position'][str(0)]['Left_hand'] = [200] * 9
                #master.movement['position'][str(0)]['Right_hand'] = [200] * 9
            if master.setted_frame[len(master.setted_frame) - 1] != master.movement['frame_number']:
                master.setted_frame.append(master.movement['frame_number'])
            index = 1
            while index < len(master.setted_frame):
                start = master.setted_frame[index - 1]
                stop = master.setted_frame[index]
                #        if (not master.movement['position'][str(0)]['Left_hand'])|(not master.movement['position'][str(0)]['Right_hand']):
                #            master.movement['position'][str(0)]['Left_hand'] = [200]*9
                #            master.movement['position'][str(0)]['Right_hand'] = [200]*9

                for frame in range(start + 1, stop, 1):
                    master.movement['position'][str(frame)]['Left_hand'] = master.movement['position'][str(start)]['Left_hand']
                    master.movement['position'][str(frame)]['Right_hand'] = master.movement['position'][str(start)]['Right_hand']
                index += 1
            print 'Done Building'

            print 'Smoothing the motion'

            win = find_smth_win()/int(2) if master.autoSmth.get() == 1 else master.smooth.get()
            for frame in range(master.movement['frame_number']):
                master.movement['position'][str(frame)]['Left_hand'] = np.mean([master.movement['position'][str(frame + i)]['Left_hand'] for i in range(min(master.movement['frame_number'] - frame-1, win)+1)], 0)
                master.movement['position'][str(frame)]['Right_hand'] = np.mean([master.movement['position'][str(frame + i)]['Right_hand'] for i in range(min(master.movement['frame_number'] - frame-1, win)+1)], 0)
                master.movement['position'][str(frame)]['Left_hand'] = list(np.int_(master.movement['position'][str(frame)]['Left_hand']))
                master.movement['position'][str(frame)]['Right_hand'] = list(np.int_(master.movement['position'][str(frame)]['Right_hand']))
            print 'Done Smoothing'
            master.needToBuild = False
            save.config(state=NORMAL)

        time.sleep(0.5)
        print 'Playing'
        goal_position = master.movement["position"]["0"]
        tools.go_to_pos(active_motors, motor, goal_position, pub, L, R)



        if list(master.emotion_list.curselection()):
            if master.emotion_list.get(master.emotion_list.curselection())=='show text':
                print 'text'
                HEAD_PUB = HEAD_TXT
                show.name = master.text.get()
            else:
                print 'emotion'
                HEAD_PUB = HEAD_EMO
                show.name = master.emotion_list.get(master.emotion_list.curselection())
            show.time = float(master.emotion_time.get())
            print show
        else:
            HEAD_PUB = None

        tools.do_seq(active_motors, master.movement["freq"], master.movement["position"],pub, L, R, HEAD_PUB, show)
        master.recSlider.set(master.movement["frame_number"])
        print 'Done'

    def clearcall():
        master.setted_frame = []
        master.needToBuild = False

    def setauto():
        master.smooth.config(state=NORMAL) if master.autoSmth.get() == 0 else master.smooth.config(state=DISABLED)

    def saveL():
        lefthandpos = [master.Lwrist_V.get(), master.Lwrist_H.get(), master.Lthump_J.get(), master.Lthump.get(),
                              master.LOpen.get(), master.Lindex.get(), master.Lmajor.get(), master.Lring.get(), master.Lauri.get()]
        name = tkSimpleDialog.askstring('Left Hand set name', 'Please enter the name of the Left hand set', parent=master)
        if name:
            handSetting["Left"][name] = lefthandpos
            L_handSets.insert(len(handSetting["Left"]), name)
        else:
            print "you Should enter the mane of the hand set"

        with open("/home/odroid/catkin_ws/src/robot_body/recording/handSetting.json", "w") as h:
            json.dump(handSetting, h)

    def saveR():
        righthandpos = [master.Rwrist_V.get(), master.Rwrist_H.get(), master.Rthump_J.get(), master.Rthump.get(),
                                master.ROpen.get(), master.Rindex.get(), master.Rmajor.get(), master.Rring.get(), master.Rauri.get()]
        name = tkSimpleDialog.askstring('Right Hand set name', 'Please enter the name of the Right hand set', parent=master)
        if name:
            handSetting["Right"][name] = righthandpos
            R_handSets.insert(len(handSetting["Right"]), name)
        else:
            print "you Should enter the mane of the hand set"

        with open("/home/odroid/catkin_ws/src/robot_body/recording/handSetting.json", "w") as h:
            json.dump(handSetting, h)

    def Lrel():
        tools.multi_servo_set([50] * 9, None, L)

    def Rrel():
        tools.multi_servo_set(None, [50] * 9, None, R)

    close = Button(buttfram, text='Close', width=10, command=closecall)
    close.grid(row=6, column=4, sticky=E)


    rel = Button(lefthand, text="Release",width = 10, command =  Lrel)
    rel.pack(side=LEFT)
    LSET = Button(lefthand, text=">>", width=10, command=saveL)
    LSET.pack(side=RIGHT)
    master.Lrec = IntVar(lefthand,value=0)
    recL = Checkbutton(lefthand, text='Record Mode', variable=master.Lrec)
    recL.pack()

    rer = Button(righthand, text="Release", width=10, command= Rrel)
    rer.pack(side=RIGHT)
    RSET = Button(righthand, text="<<", width=10, command=saveR)
    RSET.pack(side=LEFT)
    master.Rrec = IntVar(righthand, value=0)
    recR = Checkbutton(righthand, text='Record Mode', variable=master.Rrec)
    recR.pack()


    L_handSets = Listbox(medButt, height=33, width=15)
    L_handSets.grid(row=2, column=0, columnspan=2)
    R_handSets = Listbox(medButt, height=33, width=15)
    R_handSets.grid(row=2, column=2, columnspan=2)
    try:
        with open("/home/odroid/catkin_ws/src/robot_body/recording/handSetting.json", "r") as f:
            handSetting = json.load(f)

        for name, pos in handSetting["Left"].items():

            L_handSets.insert(END, (name))
        for name, pos in handSetting["Right"].items():

            R_handSets.insert(END, (name))
    except Exception, err:
        print err


    def setleft():
        if list(L_handSets.curselection()):
            left_values = handSetting["Left"][L_handSets.get(L_handSets.curselection())]
            tools.multi_servo_set(left_values, None, L)
            master.Lwrist_V.set(left_values[0])
            master.Lwrist_H.set(left_values[1])
            master.Lthump_J.set(left_values[2])
            master.Lthump.set(left_values[3])
            master.LOpen.set(left_values[4])
            master.Lindex.set(left_values[5])
            master.Lmajor.set(left_values[6])
            master.Lring.set(left_values[7])
            master.Lauri.set(left_values[8])
        else:
            print "No setting is selected"

    def setright():
        if list(R_handSets.curselection()):
            right_values = handSetting["Right"][R_handSets.get(R_handSets.curselection())]
            tools.multi_servo_set(None, right_values, None, R)
            master.Rwrist_V.set(right_values[0])
            master.Rwrist_H.set(right_values[1])
            master.Rthump_J.set(right_values[2])
            master.Rthump.set(right_values[3])
            master.ROpen.set(right_values[4])
            master.Rindex.set(right_values[5])
            master.Rmajor.set(right_values[6])
            master.Rring.set(right_values[7])
            master.Rauri.set(right_values[8])
        else:
            print "No setting is selected"


    def L_DEL():

        if list(L_handSets.curselection()):
            if tkMessageBox.askyesno(title='Warning', message='do you want to DELETE ' + L_handSets.get(L_handSets.curselection()) + ' ?', parent=master):
                with open("/home/odroid/catkin_ws/src/robot_body/recording/handSetting.json") as f:
                    handSetting = json.load(f)
                del handSetting["Left"][L_handSets.get(L_handSets.curselection())]
                L_handSets.delete(L_handSets.curselection())
                with open("/home/odroid/catkin_ws/src/robot_body/recording/handSetting.json", "w") as f:
                    json.dump(handSetting, f)
        else:
            print "No setting is selected"

    def R_DEL():

        if list(R_handSets.curselection()):
            if tkMessageBox.askyesno(title='Warning', message='do you want to DELETE ' + R_handSets.get(R_handSets.curselection()) + ' ?', parent=master):
                with open("/home/odroid/catkin_ws/src/robot_body/recording/handSetting.json", "r") as f:
                    handSetting = json.load(f)
                del handSetting["Right"][R_handSets.get(R_handSets.curselection())]
                R_handSets.delete(R_handSets.curselection())
                with open("/home/odroid/catkin_ws/src/robot_body/recording/handSetting.json", "w") as f:
                    json.dump(handSetting, f)
        else:
            print "No setting is selected"

    leftSet = Button(medButt, text="<<", width=5, command=setleft)
    leftSet.grid(row=3, column=0, sticky=E)
    LDEL = Button(medButt, text="DEL", width=5, command=L_DEL)
    LDEL.grid(row=3, column=1, sticky=W)

    rightSet = Button(medButt, text=">>", width=5, command=setright)
    rightSet.grid(row=3, column=3, sticky=W)
    RDEL = Button(medButt, text="DEL", width=5, command=R_DEL)
    RDEL.grid(row=3, column=2, sticky=E)
    master.steps = StringVar(master, value=1)
    master.frm = 0
    master.recSlider = Scale(buttfram, from_=0, to=master.movement['frame_number']-1, orient=HORIZONTAL, length=910, command=setframe)
    master.recSlider.set(0)
    master.recSlider.grid(row=0, column=0, columnspan=5)
    del_befor = Button(buttfram, text='Delete Before', width=10, command=DelBefor)
    del_befor.grid(row=1, column=0)
    del_after = Button(buttfram, text='Delete After', width=10, command=DelAfter)
    del_after.grid(row=1, column=4)
    master.autoSmth = IntVar(master, value=1)
    master.autoSmooth = Checkbutton(buttfram, text='Auto Smoothing', variable=master.autoSmth, command=setauto)
    master.autoSmooth.grid(row=2, column=0)
    master.smooth = Scale(buttfram, label = "Smoothing:", from_=0, to=master.movement['frame_number']-1, takefocus=1, orient=HORIZONTAL, length=250)
    master.smooth.set(min(30, master.movement['frame_number'] - 1))
    master.smooth.grid(row=2, column=1, columnspan=2, sticky=W)
    master.smooth.config(state=DISABLED)
    setpos = Button(buttfram, text='Set Pos', width=10, command=setcall)
    setpos.grid(row=3, column=0)
    build = Button(buttfram, text='Build & play', width=10, command=buildPlay)
    build.grid(row=4, column=0)
    save = Button(buttfram, text='Save', width=10, command=savecall)
    save.grid(row=5, column=0)
    save.config(state=DISABLED)
    clear = Button(buttfram, text='Clear', width=10, command=clearcall)
    clear.grid(row=6, column=0)
    clear.config(state=DISABLED)
    master.emotion_list = Listbox(buttfram, width=15, height=13)
    master.emotion_list.grid(row=2, column=2, rowspan=5, sticky=W)


    for name in emotions:
        master.emotion_list.insert(END, str(name))

    master.text = StringVar()
    master.textEntry = Entry(buttfram, width=15, textvariable=master.text)
    master.textEntry.grid(row=1, column=2, sticky=W)

    master.emotion_time = StringVar(value=2)
    master.emotion_timeEntry = Entry(buttfram, width=3, textvariable=master.emotion_time)
    master.emotion_timeEntry.grid(row=1, column=3, sticky=W)
    msg = Label(buttfram, height=8, justify=LEFT, text= '<----- Click here to record a hand set.\n\n'
                                                        '<----- Click here to build or play the recording.                    Add face emotion----->  \n\n'
                                                        '<----- Click here to save. \n\n'
                                                        '<----- Click here to clear all and start over')
    msg.grid(row=3, column=1, rowspan=4, sticky=W)
    master.needToBuild = False
    master.setted_frame = []
