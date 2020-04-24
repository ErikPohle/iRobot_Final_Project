import rospy
import numpy as np 
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry

pub_move = None
sub_odom = None

def init_node_and_such():
	global pub_move
	rospy.init_node("brain")
	pub_move = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=10)
	sub_odom = rospy.Subscriber("/odom", Odometry, setOdomCallback)

def moveTo(X, Y, T):
	msg = PoseStamped()
	msg.header.frame_id = "map"
	msg.pose.position.x = X
	msg.pose.position.y = Y
	msg.pose.orientation.w = T

	while pub_move.get_num_connections() == 0:
		rospy.sleep(1)

	pub_move.publish(msg)

def setOdomCallback(msg):
	#set odom to match the message
	pass