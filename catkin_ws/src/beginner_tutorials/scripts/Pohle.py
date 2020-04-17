#!/usr/bin/env python
#import rospy
#from std_msgs.msg import String


import rospy
from std_msgs.msg import String
import numpy as np

pub = rospy.Publisher('/lab0', String, queue_size=10)

def lab_zero(data):
	rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

def one_node_to_rule_them_all():
	
	# initialize node and set subscriber to /lab0
	rospy.init_node('Pohle', anonymous=True)
	rospy.Subscriber('/lab0', String, lab_zero)

	# while ros is running
	while not rospy.is_shutdown():
	
		# get data
		hello_str = "test world %s" % rospy.get_time()
		rospy.loginfo(hello_str)
		pub.publish(hello_str)

		# sleep for one sec
		rospy.sleep(1)

if __name__ == '__main__':
	print "Node Now Running"
	one_node_to_rule_them_all()

