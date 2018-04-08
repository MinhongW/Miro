#!/usr/bin/env python

from __future__ import print_function
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import miro_msgs
from miro_msgs.msg import platform_config,platform_sensors,platform_state,platform_mics,platform_control,core_state,core_control,core_config,bridge_config,bridge_stream

class image_converter:	
	
	def __init__(self):
		self.image_pub = rospy.Publisher("image_topic",Image)
		self.control_pub = rospy.Publisher('miro/rob01/platform/control', platform_control, queue_size=0)
		self.fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/miro/rob01/platform/caml",Image,self.camera_callback)

		self.Control = platform_control()


	def camera_callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		

		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

		blur = cv2.GaussianBlur(gray,(5,5),5)

		fgmask = self.fgbg.apply(blur)
		ret,thresh1 = cv2.threshold(fgmask,10,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

		image,contours,heirarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		max_area = 0
		maxContIndex = 0
		for i in range(len(contours)):
			curCont=contours[i]
	    	area = cv2.contourArea(curCont)
	    	if(area>max_area):
        		max_area=area
        		maxContIndex=i	
		curCont = contours[maxContIndex]

		hull = cv2.convexHull(curCont)
		drawing = np.zeros(cv_image.shape,np.uint8)
		cv2.drawContours(thresh1,[curCont],0,(0,255,0),2)
		cv2.drawContours(thresh1,[hull],0,(0,0,255),2)
		
		# if someCondition != 0:
		# 	self.Control.tail = 0.5
		# else:
		# 	self.Control.tail = -1.0


		#self.control_pub.publish(self.Control)

		cv2.imshow("Image window", fgmask)
		cv2.waitKey(3)

		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		except CvBridgeError as e:
			print(e)
		

def main(args):
	ic = image_converter()
	
	rospy.init_node('image_converter', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)



img = cv2.imread('sachin.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
