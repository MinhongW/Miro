#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

import sys, select, termios, tty
import random
import thread
import time
import numpy as np

import miro_msgs
from miro_msgs.msg import platform_config,platform_sensors,platform_state,platform_mics,platform_control,core_state,core_control,core_config,bridge_config,bridge_stream

def publish():
    global Control
    #sensorSub = rospy.Subscriber('miro/rob01/platform/sensors',platform_sensors,test_callback)
    pub = rospy.Publisher('miro/rob01/platform/control', platform_control, queue_size=0)
    while True:
        pub.publish(Control)
        time.sleep(0.05)

testSensor = 0

def test_callback(data):
    global testSensor
    testSensor = data.touch_body

def getKey():
    	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

def spin():
    #print "spinning\n"
    Control.body_vel.angular.z = 1.7
    time.sleep(4)
    Control.body_vel.angular.z = 0
    time.sleep(2)
    
def nod():
    #print "nodding\n"
    Control.body_config[1] =  - 1.0
    time.sleep(2)
    Control.body_config[1] =  1.0
    time.sleep(2)
    Control.body_config[1] =   0
    time.sleep(2)


def shake():
    #print "shaking\n"
    Control.body_config[2] = - 1.0
    time.sleep(2)
    Control.body_config[2] =   1.0
    time.sleep(2)
    Control.body_config[2] =   0
    time.sleep(2)
    
def wag():
    #print "wagging\n"
    Control.tail = 1.0
    time.sleep(3)
    Control.tail = 0.0
    time.sleep(2)
    

def blink():
    #print "blinking\n"
    Control.blink_time = 2
    time.sleep(0.2)
    Control.blink_time = 0
    time.sleep(2)

def ears():
    #print "woofing\n"
    Control.ear_rotate = [1.0,1.0]
    time.sleep(3)
    Control.ear_rotate = [0.0,0.0]
    time.sleep(1)

def printControlStatus():
    print "currently:\tspeed %s    \tangular %s    \ttilt %s    \tlift %s    \tyaw %s    \tpitch %s\n" % (Control.body_vel.linear.x,Control.body_vel.angular.z,Control.body_config[0],Control.body_config[1],Control.body_config[2],Control.body_config[3])

if __name__=="__main__":
    
    global Control
    Control = platform_control()
    rospy.init_node('teleop_twist_keyboard')
    settings = termios.tcgetattr(sys.stdin)

    Control.body_config_speed = [-1.0, -1.0, -1.0, -1.0]
    quitGame = False
    playing = False
    availableMoves = [spin,blink,nod,shake,wag,ears]
    moves = []
    print "Welcome to Miro's Memory Game"
    mistakeMessage = "Uh oh, you made a mistake! Thanks for playing! "
    thread.start_new_thread(publish, ())
    while(quitGame == False):
        if (playing==False):
            print "Watch closely!\n"
            for move in moves:
                    print "I'm doing a move!"
                    move()
            randInt = random.randint(0,len(availableMoves)-1)
            nextMove = availableMoves[randInt]
            print "Doing a move!"
            nextMove()
            moves.append(nextMove)
            playing = True
            print "------------------------------------------------------"
        else:
            print "Your turn"
            for move in moves:
                print "Enter the next move in the sequence!\n"
                print "t to turn around, n to nod head, s to shake head,\n w to Wag tail, b to blink and e to rotate ears\n q to quit!"
                key = getKey()
                if key == 'q': 
                    quitGame=True
                    break
                
                elif key == "t":
                    if move == spin:
                        spin()
                    else:
                        print mistakeMessage + "You lasted "+ str(len(moves)-1)+" rounds!" 
                        quitGame=True
                        break
                
                elif key == "n":
                    if move == nod:
                        nod()
                    else:
                        print mistakeMessage + "You lasted "+ str(len(moves)-1)+" rounds!"
                        quitGame=True
                        break
                
                elif key == "s": 
                    if move == shake:
                        shake()
                    else:
                        print mistakeMessage + "You lasted "+ str(len(moves)-1)+" rounds!"
                        quitGame=True
                        break
                elif key == "w":
                    if move == wag:
                        wag()
                    else:
                        print mistakeMessage + "You lasted "+ str(len(moves)-1)+" rounds!"
                        quitGame=True
                        break
                elif key == 'e':
                    if move == ears:
                        ears()
                    else:
                        print mistakeMessage + "You lasted "+ str(len(moves)-1)+" rounds!"
                        quitGame=True
                        break
                elif key == "b":
                    if move == blink: 
                        blink()
                    else:
                        print mistakeMessage + "You lasted "+ str(len(moves)-1)+" rounds!"
                        quitGame=True
                        break
            playing = False

    
    # Memory Game
    # List of the moves he can do:
    #spins around - left arrow 
    #blinks - spacebar
    #nod - n
    #shake head - s
    #wag tail -