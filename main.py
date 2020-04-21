import rospy
import numpy as numpy
import argparse
from geometry_msgs.msg import PoseStamped


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Lab7")
	#using default values from previous step
	parser.add_argument('-x','--x',nargs=1,default=-2.0,help='Starting x location')
	parser.add_argument('-y','--y',nargs=1,default=-0.5,help='Starting y location')
	parser.add_argument('-t','--theta',nargs=1,default= 0.0,help='Starting theta', dest="t")
	args = parser.parse_args()

	print(args)

	startX = args.x
	startY = args.y
	startT = args.t

	if not isinstance(startX, float):
		startX = float(args.x[0])
	if not isinstance(startY, float):
		startY = float(args.y[0])
	if not isinstance(startT, float):
		startT = float(args.t[0])

	msg = PoseStamped()
	msg.header.frame_id = "map"
	msg.pose.position.x = startX
	msg.pose.position.y = startY
	msg.pose.orientation.w = startT

	rospy.init_node("lab7_script")

	publisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=10)
	while publisher.get_num_connections() == 0:
		rospy.sleep(1)

	publisher.publish(msg)