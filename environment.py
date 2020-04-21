import math, random

listOfAsteroids = []
mapHeight = 0
mapWidth = 0

def initEnv(mapDimensions=(400,400), numAsteroids=10):

    # need dimensions of map for random asteroid creation
    # need number of asteroids to be generated
    # just assume dimensions are 400 x 400

    global listOfAsteroids, mapHeight, mapWidth
    listOfAsteroids = []
    mapWidth = mapDimensions[0]
    mapHeight = mapDimensions[1]

    # generate x and y positions for asteroids and add them to list
    spawnAsteroids(numAsteroids)
    
    print("LOG: Environment Succesfully Initialized.")

    # rospy.init_node("Environment")

    # what should I publish to?
    # what am I publishing?
	# publisher = rospy.Publisher("???", PoseStamped, queue_size=10)
	# while publisher.get_num_connections() == 0:
	# 	rospy.sleep(1)

	# publisher.publish(msg)

# Call after init, while the game is still running if we are out of asteroids from the initial population
def spawnAsteroids(numAsteroids=10):
    global listOfAsteroids

    # generate x and y positions for asteroids and add them to list
    for i in range(0, numAsteroids):
        asteroidX = random.randint(0, mapWidth)
        asteroidY = random.randint(0, mapHeight)
        listOfAsteroids.append((asteroidX, asteroidY))
    
    print("LOG: Spawned Asteroids Succesfully")

def asteroidCollision():
    # hmmm
    pass

if __name__ == "__main__":
    initEnv()
    print(listOfAsteroids)

    