import math, random, asteroid

class Environment():

    def __init__(self, mapDimensions, numAsteroids):

        # need dimensions of map for random asteroid creation
        # need number of asteroids to be generated
        # just assume dimensions are 400 x 400

        self.listOfAsteroids = []
        self.mapLength = mapDimensions[0]
        self.mapWidth = mapDimensions[1]
        self.mapHeight = mapDimensions[2]
        self.numAsteroids = numAsteroids
        self.asteroidSpeed = 5
        self.gameOver = False
        
        print("LOG: Environment Succesfully Initialized.")

        # rospy.init_node("Environment")

        # what should I publish to?
        # what am I publishing?
        # publisher = rospy.Publisher("???", PoseStamped, queue_size=10)
        # while publisher.get_num_connections() == 0:
        # 	rospy.sleep(1)

        # publisher.publish(msg)

    # Call after init, while the game is still running if we are out of asteroids from the initial population
    def spawnAsteroids(self):

        # generate x and y positions for asteroids and add them to list
        for i in range(0, self.numAsteroids):
            asteroidX = random.randint(0, self.mapLength)
            asteroidY = random.randint(0, self.mapWidth)
            asteroidZ = random.randint(50, self.mapHeight)
            ast = asteroid.Asteroid(asteroidX, asteroidY, asteroidZ)
            self.listOfAsteroids.append(ast)
        
        print("LOG: Spawned Asteroids Succesfully")

    def asteroidCollision(self):
        # hmmm
        # need Publisher/Subscriber for health (if asteroid hits player) and points (if player destroys asteroid)

        for i in self.listOfAsteroids:
            pos = i.getPos()
            
            # check if z pos is hitting the ground
            if pos[2] <= 25:
                self.gameOver = True
                return
    
    def updateAsteroids(self):
        for i in self.listOfAsteroids:
            pos = i.getPos()
            i.updatePos(pos[0], pos[1], pos[2] - self.asteroidSpeed)
            

if __name__ == "__main__":
    initEnv()
    print(listOfAsteroids)

    