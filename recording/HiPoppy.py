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

    def pos_nextCall(self):
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
            tkMessageBox.showerror(title='Warning', message='You need to select at least ONE Actor!')
            return None
        if tkMessageBox.askyesno(title='Warning',
                                 message='Warning: You selected folowing actors: ' + str(
                                     selected) + 'the rest of robot will be in mode "freeze" do you want to continue?'):
            pos_rec_fram = Toplevel()
            pos_rec_fram.grab_set()
            pos_rec_fram.transient(self.master)
            # self.master.wait_window(RECD)
            myPosRec = RECORDING_2(pos_rec_fram, mtrs)

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

        self.Next = Button(master, text="Manual Recording", width=20, command=self.nextCall)
        self.Next.pack(anchor=NW)
        self.PosByPos = Button(master, text="POS_BY_POS Recording", width=20, command=self.pos_nextCall)
        self.PosByPos.pack(anchor=NW)
        self.option2 = Radiobutton(self.master, text="Edit old Sign", variable=self.Var, value = 2, command=self.method)
        self.option2.pack(anchor=NW)
        self.option2.deselect()

        self.loadFile = Button(self.master, text="Load File", width=10, command=self.editSign)
        self.loadFile.pack(anchor=NW)
        self.loadFile.config(state=DISABLED)

        self.Cancel = Button(master, text="Cancel", width=10, command=self.cancelCall)
        self.Cancel.pack(anchor=E)




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
                            'emotion_name':'',
                            'text': '',
                            'emotion_time': [],
                            'position':self.pos
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
        goal_position = self.movement['position']['0']
        tools.go_to_pos(self.movement['actors_NAME'], motor, goal_position, pub)
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
        goal_position = {"Robot": [0 for name in self.motorsName],
                            "Right_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100],
                            "Left_hand" : [200, 200, 100, 100, 200, 100, 100, 100, 100]}
        tools.go_to_pos(self.motorsName, motor, goal_position, pub)
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
        self.StpTm = StringVar(self.master, value='5')
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
        goal_position = {"Robot": [0 for name in self.deadmotors],
                            "Right_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100],
                            "Left_hand" : [200, 200, 100, 100, 200, 100, 100, 100, 100]}
        tools.go_to_pos(self.deadmotors, motor, goal_position, pub)
        tools.releas(self.motorsName, pub)
        print('Robot started')


class RECORDING_2():

    def setcall(self):
        self.settings["SET" + str(self.sets.size() + 1)] = [motor[name].present_position
                                                            for name in self.motorsName]
        self.sets.insert(END, "SET" + str(self.sets.size() + 1))
        self.play.config(state=DISABLED)
        self.save.config(state=DISABLED)
        self.set_hand.config(state=DISABLED)
        self.edit.config(state=NORMAL)
        self.delete.config(state=NORMAL)
        if self.sets.size() > 1:
            self.build.config(state=NORMAL)
        self.info.set("Done setting")
    def build(self):
        self.sign={"position":{}}
        i=0
        if len(self.settings) < 2:
            print "error: you need at least TWO SETTINGS"
            return
        elif len(self.settings) < 3:
            method="Smooth"
        else:
            method="Smooth"   # "Linear"
        for SET in range(len(self.settings)-1):
            max_err = max([abs(self.settings["SET"+str(SET+1)][ndx] - self.settings["SET"+str(SET+1+1)][ndx])
                           for ndx in range(len(self.settings["SET"+str(SET+1+1)]))])
            self.sign["position"].update(tools.build_sign(self.settings["SET"+str(SET+1)], self.settings["SET"+str(SET+1+1)], i, int(max_err), method))
            i=len(self.sign["position"])
        self.sign["actors_NAME"]=self.motorsName
        self.sign["frame_number"]=i
        self.play.config(state=NORMAL)
        self.save.config(state=NORMAL)
        self.set_hand.config(state=NORMAL)
        self.info.set("Done building")

    def play(self):
        self.info.set("Playing")
        goal_position = self.sign["position"]["0"]
        tools.go_to_pos(self.motorsName, motor, goal_position,pub)
        for frame in range(len(self.sign["position"])):
            id=0
            for name in self.sign["actors_NAME"]:
                MOTOR.compliant=False
                MOTOR.goal_position=self.sign["position"][str(frame)]["Robot"][id]
                id+=1
                pub[name].publish(MOTOR)
            time.sleep(float(self.time.get()) / float(self.sign["frame_number"]))
        self.info.set("Done")

    def save(self):
        self.info.set("Saving sign ...")
        saveFile = tkFileDialog.asksaveasfilename(defaultextension="json",
                                                  initialdir="/home/odroid/catkin_ws/src/robot_body/recording/data_base",
                                                  parent=self.master)
        if not saveFile:
            return None

        self.sign["freq"]=float(self.sign["frame_number"])/float(self.time.get())
        self.sign["emotion_name"]=''
        self.sign["text"] = ''
        self.sign["emotion_time"]=[]
        with open(saveFile, "w") as record:
            json.dump(self.sign, record)
        self.info.set("Saved")

    def close(self):
        self.info.set("Closing the Robot")
        goal_position = {"Robot": [0 for name in self.motorsName],
                         "Right_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100],
                         "Left_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100]}
        tools.go_to_pos(self.motorsName, motor, goal_position, pub)
        tools.releas(self.motorsName, pub)
        self.info.set("Robot Closed")
        self.master.destroy()

    def edit(self):
        if self.sets.curselection():
            curs = int(self.sets.curselection()[0])
            self.settings["SET" + str(curs + 1)] = [motor[name].present_position for name in self.motorsName]
            self.play.config(state=DISABLED)
            self.save.config(state=DISABLED)
            self.set_hand.config(state=DISABLED)
            self.info.set("Set"+str(curs+1)+" edited")

    def delete(self):
        if self.sets.curselection():
            curs = int(self.sets.curselection()[0])
            for ndx in range(curs, self.sets.size() - 1):
                self.settings["SET" + str(ndx + 1)] = self.settings["SET" + str(ndx + 1 + 1)]
                self.sets.delete(ndx)
                self.sets.insert(ndx, "SET" + str(ndx + 1))
            del self.settings["SET" + str(len(self.settings))]
            self.sets.delete(END)
            self.play.config(state=DISABLED)
            self.save.config(state=DISABLED)
            self.set_hand.config(state=DISABLED)
            if self.sets.size() < 1:
                self.edit.config(state=DISABLED)
                self.delete.config(state=DISABLED)
            elif self.sets.size() < 2:
                self.build.config(state=DISABLED)
            self.info.set("Set"+str(curs+1)+" deleted")

    def selection(self, evn):
        if list(self.activemotors.curselection()):
            selected = [self.activemotors.get(ndx) for ndx in list(self.activemotors.curselection())]
            unselected = [self.activemotors.get(ndx) for ndx in range(self.activemotors.size())
                          if ndx not in list(self.activemotors.curselection())]
        else:
            selected=[]
            unselected=self.activemotors.get(0, END)
        for name in self.motorsName:
            if name in selected:
                MOTOR.compliant = False
                MOTOR.goal_position = motor[name].present_position
            else:
                MOTOR.compliant = True
            pub[name].publish(MOTOR)

    def Handset(self):
        edit_fram = Toplevel()
        edit_fram.grab_set()
        edit_fram.transient(self.master)
        self.sign["freq"]=float(self.sign["frame_number"])/float(self.time.get())
        handsSet = finger.__init__(edit_fram, self.sign, motor, pub)

    def __init__(self, master, motors):
        self.motorsName = motors
        self.deadmotors = [x for x in motor_names if x not in self.motorsName]
        self.master = master
        self.master.geometry('250x200')
        self.master.title('POS_BY_POS RECORDING')
        self.tl = Label(master, text="Time:")
        self.tl.grid(row=0, column=0)
        self.time = StringVar(value=1)
        self.timeEntry = Entry(master, width=3, textvariable=self.time)
        self.timeEntry.grid(row=0, column=1)
        self.setpos = Button(master, text="Set pos", width=5, command=self.setcall)
        self.setpos.grid(row=1, column=0, columnspan=2)
        self.build = Button(master, text="Build", width=5, command=self.build)
        self.build.grid(row=2, column=0, columnspan=2)
        self.build.config(state=DISABLED)
        self.play = Button(master, text="Play", width=5, command=self.play)
        self.play.grid(row=3, column=0, columnspan=2)
        self.play.config(state=DISABLED)
        self.save = Button(master, text="Save", width=5, command=self.save)
        self.save.grid(row=4, column=0, columnspan=2)
        self.save.config(state=DISABLED)
        self.info = StringVar()
        self.show = Label(master,textvariable=self.info)
        self.show.grid(row=5, column=0, columnspan=4)
        self.set_hand = Button(master, text="Config fingers", width=8, command=self.Handset)
        self.set_hand.grid(row=5, column=4)
        self.set_hand.config(state=DISABLED)
        self.close = Button(master, text="Close", width=8, command=self.close)
        self.close.grid(row=6, column=4)
        self.sl = Label(master, text="Settings")
        self.sl.grid(row=0, column=2, columnspan=2)
        self.sets = Listbox(master, height=5, width=8)
        self.sets.grid(row=1, column=2, rowspan= 3,columnspan=2)
        self.mtr_l = Label(master, text="Motors to block")
        self.mtr_l.grid(row=0, column=4)
        self.activemotors = Listbox(master, height=7, width=12, selectmode=MULTIPLE)
        self.activemotors.grid(row=1, column=4, rowspan=4)
        self.activemotors.bind('<<ListboxSelect>>', self.selection)
        self.edit = Button(master, text="Edit", width=1, command=self.edit)
        self.edit.grid(row=4, column=2)
        self.edit.config(state=DISABLED)
        self.delete = Button(master, text="Del", width=1, command=self.delete)
        self.delete.grid(row=4, column=3)
        self.delete.config(state=DISABLED)
        #print self.motorsName
        #print self.deadmotors
        for name in self.motorsName:
            self.activemotors.insert(END, str(name))
        self.settings = {}
        self.sign = {}




        print('Starting the ROBOT')
        goal_position = {"Robot": [0 for name in self.deadmotors],
                         "Right_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100],
                         "Left_hand": [200, 200, 100, 100, 200, 100, 100, 100, 100]}
        tools.go_to_pos(self.deadmotors, motor, goal_position, pub)
        tools.releas(self.motorsName, pub)
        print('Robot started')
        self.info.set("Robot is Ready")





pub = dict()
motor = dict()
MOTOR = motorSet()


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

