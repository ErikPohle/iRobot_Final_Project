#!/usr/bin/env python
# used ROS tutorials talker file as template
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('/lab0', String, queue_size=10)
    rospy.init_node('Pohle', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "test world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
