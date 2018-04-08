#!/usr/bin/env python

from __future__ import print_function
import sys
import rospy
import time
import numpy as np
from std_msgs.msg import String

import miro_msgs
from miro_msgs.msg import platform_config,platform_sensors,platform_state,platform_mics,platform_control,core_state,core_control,core_config,bridge_config,bridge_stream

class sound_recognition:

    def __init__(self):
        self.control_pub = rospy.Publisher('miro/rob01/platform/control', platform_control, queue_size=0)
        self.mic_sub = rospy.Subscriber("/miro/rob01/platform/mics",platform_mics,self.mic_callback)
        self.Control = platform_control()


    def mic_callback(self,data):
        samples = data.data
        absoluteValues = [abs(x) for x in samples]
        maxAmplitude = max(absoluteValues)
        limit = 400
        print(maxAmplitude)
        if maxAmplitude > limit:
            self.Control.tail = 1.0
        else:
            self.Control.tail = -1.0

        self.control_pub.publish(self.Control)

def main(args):
    sound_recognition()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)