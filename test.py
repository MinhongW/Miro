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
    pub = rospy.Publisher('miro/sim01/platform/control', platform_control, queue_size=0)
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
    Control.body_vel.angular.z = Control.body_vel.angular.z + 1
    time.sleep(3)
    Control.body_vel.angular.z = 0
    
def nod():
    #print "nodding\n"
    Control.body_config[1] =  - 1.0
    time.sleep(3)
    Control.body_config[1] =  1.0
    time.sleep(2)
    Control.body_config[1] =   0
    time.sleep(3)


def shake():
    #print "shaking\n"
    Control.body_config[2] = - 1.0
    time.sleep(3)
    Control.body_config[2] =   1.0
    time.sleep(2)
    Control.body_config[2] =   0
    time.sleep(3)
    
def wag():
    #print "wagging\n"
    Control.tail = 1.0
    time.sleep(3)
    Control.tail = 0.0
    

def blink():
    #print "blinking\n"
    Control.blink_time = 2
    time.sleep(0.2)
    Control.blink_time = 0

def woof():
    #print "woofing\n"
    Control.sound_index_P2 = 2
    time.sleep(1)
    Control.sound_index_P2 = 24

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
    availableMoves = [spin,blink,nod,shake,wag]
    moves = []
    print "Welcome to Miro's Memory Game"
    thread.start_new_thread(publish, ())
    while(quitGame == False):
        if (playing==False):
            print "Watch closely!\n"
            for move in moves:
                    move()
            randInt = random.randint(0,len(availableMoves)-1)
            nextMove = availableMoves[randInt]
            nextMove()
            moves.append(nextMove)
            playing = True
        else:
            for move in moves:
                print "Enter the next move in the sequence!\n"
                print "S to spin around, Y to nod head, N to shake head,\n W to Wag tail,B to blink"
                #print move.func_name
                key = getKey()
                if key == 'q': 
                    quitGame=True
                    break
                
                elif key == "s":
                    if move == spin:
                        spin()
                    else:
                        print "YOU WERE WRONG"
                        quitGame=True
                        break
                
                elif key == "y":
                    if move == nod:
                        nod()
                    else:
                        print "YOU WERE WRONG"
                        quitGame=True
                        break
                
                elif key == "n": 
                    if move == shake:
                        shake()
                    else:
                        print "YOU WERE WRONG"
                        quitGame=True
                        break
                elif key == "w":
                    if move == wag:
                        wag()
                    else:
                        print "YOU WERE WRONG"
                        quitGame=True
                        break
                
                elif key == "b":
                    if move == blink: 
                        blink()
                    else:
                        break
            playing = False

    
    # Memory Game
    # List of the moves he can do:
    #spins around - left arrow 
    #blinks - spacebar
    #nod - n
    #shake head - s
    #wag tail -