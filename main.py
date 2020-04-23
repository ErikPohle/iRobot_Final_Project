import rospy
import numpy as numpy
import argparse
from geometry_msgs.msg import PoseStamped
import environment
import time

def runSim(env):
	for i in env.listOfAsteroids:
		print(i.getPos()),
	
	
	env.updateAsteroids()
	env.asteroidCollision()
	
	if env.gameOver == True:
		print("Game Over")
		return -1

	for i in env.listOfAsteroids:
		print(i.getPos()),



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Lab7")
	parser.add_argument('-m','--m',nargs=1,default=[400, 400, 400],help='Map Size')
	parser.add_argument('-na','--na',nargs=1,default=10,help='Number of Initial Asteroids')
	args = parser.parse_args()
	lastFrameTime = 0

	env = environment.Environment(args.m, args.na)
	env.spawnAsteroids()

	x = runSim(env)
	numIterations = 1

	while x != -1:
		print(numIterations)
		numIterations += 1
		x = runSim(env)

	"""
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
	"""