import rospy
import numpy as np 
from geometry_msgs.msg import PoseStamped, Pose
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import GoalStatusArray
import tf
import main

#publishers
pub_move = None
pub_shooter = None

#subscribers
sub_odom = None
sub_move_status = None

#globals
bot_pos = [0, 0, 0] # [X, Y, Z]
bot_ori = [0, 0, 0, 1] # [X, Y, Z, W]

cur_dest = [-50, -50, 1] #[X, Y, T] like from setDest()
dest_queue = []

asteroids = {}
last_asteroids = {}

#booleans
moving = False
shooting = False

def init_node_and_such():
	#simply initializes the node, publishers, and subscribers in rospy
	global pub_move, pub_shooter
	global sub_odom, sub_move_status
	rospy.init_node("brain")
	pub_move = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=10)
	pub_shooter = rospy.Publisher("/laser", Pose, queue_size=10)

	sub_odom = rospy.Subscriber("/odom", Odometry, setOdomCallback)
	sub_move_status = rospy.Subscriber("/move_base/status", GoalStatusArray, moveStatusCallback)

def setDict(ast_dict):
	global asteroids
	asteroids = ast_dict

def setDest(X, Y, D, radian=False):
	#takes in an X,Y,Degree/Radian and sends a message to rospy to move bot
	# also updates cur_dest to reflect this new destination
	global cur_dest
	msg = PoseStamped()
	msg.header.frame_id = "map"
	msg.pose.position.x = X
	msg.pose.position.y = Y

	if not radian:
		quat = degreeToQuaternion(D)
	else:
		quat = eulerToQuaternion(0, 0, D)

	msg.pose.orientation.x = quat[0]
	msg.pose.orientation.y = quat[1]
	msg.pose.orientation.z = quat[2]
	msg.pose.orientation.w = quat[3]

	cur_dest[0] = X
	cur_dest[1] = Y
	cur_dest[2] = D
	print("set dest to: ", cur_dest)

	while pub_move.get_num_connections() == 0:
		rospy.sleep(1)

	pub_move.publish(msg)

def setOdomCallback(msg):
	#set odom to match the message on callback
	# also handles some logic about when to move etc to avoid
	# having to use threads :P I can do it!
	global bot_pos, bot_ori

	bot_pos[0] = msg.pose.pose.position.x
	bot_pos[1] = msg.pose.pose.position.y
	bot_pos[2] = msg.pose.pose.position.z
	# bot_pos = msg.pose.pose.position

	bot_ori[0] = msg.pose.pose.orientation.x
	bot_ori[1] = msg.pose.pose.orientation.y
	bot_ori[2] = msg.pose.pose.orientation.z
	bot_ori[3] = msg.pose.pose.orientation.w

	#checks asteroids and updates dest_queue according to cost function
	learn_asteroids()
	# if goal is reached, shoot, then move to the next goal in dest_queue
	# else, pass and wait for bot to finish current move_goal
	mn_status_code = moveNext()

def moveStatusCallback(msg):
	#sets moving to false if the destination has been reached
	global moving
	if moving:
		if msg.status_list[-1].status == 3:
			moving = False

def moveNext(aim_for_next = True):
	global moving
	#if robot is not currently moving or shooting,
	# will set cur_dest to the next dest in queue
	#  two options for orientation_at_goal, explained below
	if moving or shooting:
		return -1
	elif not moving:
		blast()
		if len(dest_queue) == 0:
			return -2 #no destinations queued

		if aim_for_next:
			#degrees from cur_target to next_target so it's pre-lined up
			try:
				D = np.arctan2((dest_queue[1][1]-dest_queue[0][1]),(dest_queue[1][0]-dest_queue[0][0]))
			except IndexError:
				#we're aiming for the last target
				D = 0 #arbitrary
		else:
			#so as to not slow things down, line it up how it should've already been moving roughly
			# D = np.arctan((dest_queue[0][1]-cur_dest[1])/(dest_queue[0][0]-cur_dest[0]))
			D = 0 #arbitrary

		newDest = dest_queue.pop(0)

		setDest(newDest[0], newDest[1], D, radian=True)
		moving = True
		return 0

def queueDest(X, Y):
	#adds a destination to Robot's queue of destinations
	dest_queue.append([X, Y])

def degreeToQuaternion(deg):
	#assumes we only care about yaw bc 2d rotation of bot
	# takes degrees, passes on rads
	rad = (deg/180.0)*np.pi
	quaternion = eulerToQuaternion(0,0,rad)
	return quaternion

def eulerToQuaternion(roll, pitch, yaw):
	#roll, pitch, yaw all in radians at this point
	q = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
	#quat[0,1,2,3] = pose.orientation.x, .y, .z, .w
	return q

def quaternionToEuler(quaternion):
	# quaternion must be like:
	# quaternion = (
	# 	pose.orientation.x
	# 	pose.orientation.y
	# 	pose.orientation.z
	# 	pose.orientation.w )
	euler = tf.transformations.euler_from_quaternion(quaternion)
	roll = euler[0]
	pitch = euler[1]
	yaw = euler[2]

	return roll, pitch, yaw

def blast(x = 0, y = 0, z = 100):
	#x,y,z is the force vector, position vector given by robot location
	msg = Pose()
	msg.position.x = bot_pos[0]
	msg.position.y = bot_pos[1]
	msg.position.z = 0.3
	msg.orientation.x = x
	msg.orientation.y = y
	msg.orientation.z = z

	pub_shooter.publish(msg)


def learn_asteroids():
	global last_asteroids
	#updates the asteroid dict to current one in environment.
	# if there was a change, calls the queue_asteroids() fxn to change approach
	if asteroids != last_asteroids:
		last_asteroids = asteroids
		queue_asteroids()
		return 1
	else: #asteroids hasn't changed
		return 0

def queue_asteroids():
	global dest_queue
	#uses the dictionary of asteroids to calculate a cost for each
	# and then queues the locations of each depending on cost
	kQueue = []
	for astKey in asteroids:
		curAst = asteroids[astKey]
		#if an asteroid is about to hit the ground, it needs priority
		# high urgency corresponds to an asteroid near ground
		urgency = height_to_urgency(curAst.z)
		#nice to hit nearby asteroids on the way
		# high distance means asteroid is far out of way (tuned, not linear)
		distance = tuned_distance(curAst)
		#overall priority is a balancing act between these two
		# high priority comes first 
		priority = urgency - distance
		kQueue.append((astKey, priority))
	kQueue.sort(key=lambda tup: tup[1]) #sorts based on priority values
	#clear queue
	dest_queue = []
	for key, priority in kQueue:
		queueDest(asteroids[key].x, asteroids[key].y)

def height_to_urgency(height):
	#higher number the lower the asteroid is
	return 100-height

def tuned_distance(ast):
	ast_x = ast.x
	ast_y = ast.y
	bot_x = bot_pos[0]
	bot_y = bot_pos[1]

	dist = np.sqrt((ast_y - bot_y)**2+(ast_x - bot_x)**2)
	#less than 6 always, and urgency is like 0-200, so scale
	return dist * 10