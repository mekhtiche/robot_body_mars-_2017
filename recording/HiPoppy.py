#!/usr/bin/python
# -*- coding: UTF-8 -*-  # this is to add arabic coding to python
import sys,os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import rospy
from robot_body.msg import motorSet
from robot_body.msg import motorStat
import thread
import json
import time
import tkFileDialog
import tkMessageBox
from Tkinter import *
from timeit import default_timer
from pypot.robot import config
import robot_tools.robot_tools as tools
import finger


class REC():

    # SELECT OR DESELECT THE CHILD OF THE CHECKBUTTON CLICKED
    def selUsel(self, etat, list):
        for i in list:
            if etat == 1:
                self.chkb['Var_%02d' % i].select()
            else:
                self.chkb['Var_%02d' % i].deselect()
        i = 0
        for var, value in sorted(self.cb.items()):
            self.stat[i] = value.get()
            i += 1

    # CHECK THE CHECKBUTTON ON CLICK
    def check(self, name, stt):

        if name == 'Poppy':
            self.selUsel(stt, range(0, len(self.lcb)))
            return
        if name not in self.alias:
            return
        for key in self.alias[name]:
            if key in self.alias:
                self.selUsel(stt, [self.lcb.index(key)])
                self.check(key,stt)
            else:
                self.selUsel(stt, [self.lcb.index(key)])




    def child(self):
        self.stat
        i = 0
        chng = []
        for var, value in sorted(self.cb.items()):
            if self.stat[i] != value.get():
                chng = i
                stt = value.get()
            self.stat[i] = value.get()
            i += 1
        self.check(self.lcb[chng], stt)

        return self.stat

    def _motor_extractor(self, alias, name, space):
        l = []
        self.ndx += 1
        self.lcb.append(name)
        self.cb['Var_%02d' % self.ndx] = IntVar()
        self.chkb['Var_%02d' % self.ndx] = Checkbutton(self.master, text=space + name, variable=self.cb['Var_%02d' % self.ndx], command=self.child)
        self.chkb['Var_%02d' % self.ndx].pack(anchor=NW)
        space = '        ' + space
        if name not in alias:
            return [name]
        for key in alias[name]:
            if key in alias:
                l += self._motor_extractor(alias, key, space)
            else:
                l += [key]
                self.ndx += 1
                self.lcb.append(key)
                self.cb['Var_%02d' % self.ndx] = IntVar()
                self.chkb['Var_%02d' % self.ndx] = Checkbutton(self.master, text=space + key, variable=self.cb['Var_%02d' % self.ndx],
                                                     command=self.child)
                self.chkb['Var_%02d' % self.ndx].pack(anchor=NW)

        return l


    def cancelCall(self):

        self.master.destroy()


    def nextCall(self):
        selected = ''
        i = 0
        mtrs = []
        nonActive = []
        for var, value in sorted(self.cb.items()):
            if self.lcb[i] in self.motor_names:
                if value.get():
                    selected += self.lcb[i]
                    selected += ' '
                    mtrs.append(self.lcb[i])
                else:
                    nonActive.append(self.lcb[i])
            i += 1
#        print mtrs
#        print nonActive
        if selected == '':
          #  tkMessageBox.ERROR
            tkMessageBox.showerror(title= 'Warning', message='You need to select at least ONE Actor!')
            return None
        if tkMessageBox.askyesno(title='Warning',
                              message='Warning: You selected folowing actors: ' + str(selected) + 'the rest of robot will be in mode "freeze" do you want to continue?'):


            rec_fram = Toplevel()
            rec_fram.grab_set()
            rec_fram.transient(self.master)
            # self.master.wait_window(RECD)
            myRec = RECORDING_1(rec_fram, mtrs)

    def method(self):
        if self.Var.get() == 1:
            for key, value in self.chkb.items():
                value.config(state = NORMAL)

            self.Next.config(state=NORMAL)
            self.loadFile.config(state=DISABLED)
        else:

            for key, value in self.chkb.items():
                value.config(state=DISABLED)

            self.Next.config(state=DISABLED)
            self.loadFile.config(state=NORMAL)

    def editSign(self):
        recFile = tkFileDialog.askopenfilename(initialdir="/home/odroid/catkin_ws/src/robot_body/recording/data_base")
        if not recFile:
            return None
        print 'Openning the file: ' + recFile
        with open(recFile, "r") as sign:
            self.movement = json.load(sign)
        edit_fram = Toplevel()
        edit_fram.grab_set()
        edit_fram.transient(self.master)
        handsSet = finger.__init__(edit_fram, self.movement, motor, pub)

    def __init__(self, master):
        self.master = master
        self.master.geometry('480x720')
        self.master.title('Hi Poppy ;)')
        self.label1 = Label(self.master, text='Hi Poppy', font="Helvetica 48 bold italic").pack(anchor=N)
        self.label2 = Label(self.master, justify=LEFT, text='To record new sing choose "Record new Sign" than select the actors, \n'
                                                            'or choose "Edit old Sign" and select the file to edit it.').pack(anchor=NW)
        self.Var = IntVar(master, value=1)
        self.option1 = Radiobutton(self.master, text="Record new Sign", variable = self.Var, value = 1, command=self.method)
        self.option1.pack(anchor=NW)
        self.option1.select()
        self.cb = dict()
        self.chkb = dict()
        self.config = config.robot_config
        self.alias = self.config['motorgroups']
        self.lcb = ['Poppy']
        self.ndx = 0
        self.cb['Var_%02d' % self.ndx] = IntVar()
        self.chkb['Var_%02d' % self.ndx] = Checkbutton(master, text="_Poppy", variable=self.cb['Var_%02d' % self.ndx], command=self.child)
        self.chkb['Var_%02d' % self.ndx].pack(anchor=NW)
        space = "      |____ "
        for c_name, c_params in self.config['controllers'].items():
            self.motor_names = sum([self._motor_extractor(self.alias, name, space)
                               for name in c_params['attached_motors']], [])
        self.stat = [0] * len(self.cb)

        self.Next = Button(master, text="Next", width=10, command=self.nextCall)
        self.Next.pack(anchor=N)

        self.option2 = Radiobutton(self.master, text="Edit old Sign", variable=self.Var, value = 2, command=self.method)
        self.option2.pack(anchor=NW)
        self.option2.deselect()

        self.loadFile = Button(self.master, text="Load File", width=10, command=self.editSign)
        self.loadFile.pack(anchor=N)
        self.loadFile.config(state=DISABLED)

        self.Cancel = Button(master, text="Cancel", width=10, command=self.cancelCall)
        self.Cancel.pack(anchor=W)




class RECORDING_1():
    def timeToStop(self):
        self.stopTime.config(state = NORMAL) if self.STP.get() == 1 else self.stopTime.config(state = DISABLED)

    def STARTREC(self):
        self.STOP = 0
        self.sleeping = 1 / float(self.Frq.get())
        present_position = [motor[name].present_position for name in self.deadmotors]
        IDs = [motor[name].id for name in self.motorsName]
        self.pos = {}
        tools.releas(self.motorsName, pub)
        for sec in range(int(self.StrTm.get())):
            self.info.config(text=str(sec))
            time.sleep(1)
        print 'Starting record'
        i = 0
        start = default_timer()
        while self.STOP == 0:
            self.pos[str(i)] = {'Robot': [motor[name].present_position for name in self.motorsName], 'Right_hand': [200, 200, 100, 100, 200, 100, 100, 100, 100], 'Left_hand': [200, 200, 100, 100, 200, 100, 100, 100, 100]}
            i+=1

            time.sleep(self.sleeping)
            if self.STP.get() == 1 & (default_timer()-start > float(self.StpTm.get())):
                self.STOP = 1
                print 'Stop Recording'

        self.frames = i
        self.movement = {'actors_ID':IDs,
                       'actors_NAME':self.motorsName,
                       'freq': self.Frq.get(),
                       'frame_number':self.frames,
                       'position':
                           self.pos
                       }
        self.save.config(state=NORMAL)
        self.play.config(state=NORMAL)
        self.handset.config(state=NORMAL)

        self.varInfo.set('Done Recording, now you can play the recorded movement\n'
                         'if it is OK you can save it or go to hand setting\n\n'
                         '<------ Click here to play the recording\n\n'
                         '<------ Click here to save the recording\n\n'
                         '<------ Click here to go to Hand Setting')
        self.info.config(justify=LEFT)


    def STOPREC(self):
        self.STOP = 1

    def PLAY(self):

        print 'Playing'
        present_position = [motor[name].present_position for name in self.motorsName]
        goal_position = self.movement['position']['0']['Robot']
        tools.go_to_pos(self.movement['actors_NAME'], present_position, goal_position, pub)
        tools.do_seq(self.movement['actors_NAME'], self.movement['freq'], self.movement['position'], pub)
        print 'Done'

    def SAVE(self):
        print 'saving movement without hand motion '
        saveFile = tkFileDialog.asksaveasfilename()
        if not saveFile:
            return None
        with open(saveFile, "w") as record:
            json.dump(self.movement, record)
        print 'saved'

    def CLOSE(self):
        print 'closing the robot'
        present_position = [motor[name].present_position for name in self.motorsName]
        goal_position = [0 for name in self.motorsName]
        tools.go_to_pos(self.motorsName, present_position, goal_position, pub)
        tools.releas(self.motorsName, pub)
        print 'Robot Closed'
        self.master.destroy()

    def Handset(self):
        edit_fram = Toplevel()
        edit_fram.grab_set()
        edit_fram.transient(self.master)
        handsSet = finger.__init__(edit_fram, self.movement, motor, pub)

    def __init__(self, master, motors):
        self.motorsName = motors
        self.deadmotors = [x for x in motor_names if x not in self.motorsName]
        self.master = master
        self.master.geometry('540x220')
        self.master.title('AUTO RECORDING')
        self.freqLb = Label(master, text = "freq").grid(row=0, column=0)
        self.Frq = StringVar(self.master, value='50')
        self.freq = Entry(master, width = 10, textvariable = self.Frq).grid(row=0, column=1)
        self.strTm = Label(master, text="Time to start").grid(row=1, column=1)
        self.StrTm = StringVar(self.master, value='2')
        self.startTime = Entry(master, width=10, textvariable=self.StrTm).grid(row=1, column=2, sticky=W)
        self.stpTm = Label(master, text="Time to stop").grid(row=2, column=1)
        self.STP = IntVar(self.master, value=1)
        self.stop = Checkbutton(master, variable = self.STP, command = self.timeToStop).grid(row=2, column=0)
        self.StpTm = StringVar(self.master, value='10')
        self.stopTime = Entry(self.master, width=10, textvariable=self.StpTm)
        self.stopTime.grid(row=2, column=2, sticky=W)
        self.startRec = Button(self.master, text = 'Start Recording', width = 10, command = self.STARTREC)
        self.startRec.grid(row=5, column=1, sticky=NW)
        self.play = Button(self.master, text='Play', width=10, command=self.PLAY)
        self.play.grid(row=6, column=1, sticky=NW)
        self.play.config(state=DISABLED)
        self.save = Button(self.master, text='Save', width=10, command=self.SAVE)
        self.save.grid(row=7, column=1, sticky=NW)
        self.save.config(state=DISABLED)
        self.varInfo = StringVar(self.master, value="<------ Click here to start recording \n\n\n\n"
                                                    "First you need to set the friquance of recording, \n"
                                                    "time to start and the recording time \n"
                                                    "than click on Start Recording Button to start the recording.")
        self.info = Label(self.master, justify=LEFT, width=50, height=8, textvariable = self.varInfo)
        self.info.grid(row=5, column=2, rowspan=4, sticky=W)
        self.close = Button(self.master, text='Close', width=6, command=self.CLOSE)
        self.close.grid(row=9, column=2, sticky=E)

        self.handset = Button(self.master, text='Hand set', width=10, command=self.Handset)
        self.handset.grid(row=8, column=1)
        self.handset.config(state=DISABLED)
        self.STOP = 0

        print('Starting the ROBOT')
        present_position = [motor[name].present_position for name in self.deadmotors]
        goal_position = [0 for name in self.deadmotors]
        tools.go_to_pos(self.deadmotors, present_position, goal_position, pub)
        tools.releas(self.motorsName, pub)
        print('Robot started')



pub = dict()
motor = dict()



def get_motors(data):
    motor[data.name] = data


def start_topics(list):


    for name in list:
        pub[name] = rospy.Publisher('poppy/set/' + name, motorSet, queue_size=10)
        rospy.Subscriber('poppy/get/' + name, motorStat, callback=get_motors)
        motor[name]=motorStat
    print 'WORD_LISTENER publishers & subscribers successful Initial'
    rospy.spin()




def main():
    root = Tk()
    hi_poppy = REC(root)
    root.mainloop()

motor_names = config.get_motor_list(config.robot_config)


if __name__ == '__main__':
    rospy.init_node('Recorder', anonymous=True)
    thread.start_new_thread(start_topics, (motor_names,))
    main()

