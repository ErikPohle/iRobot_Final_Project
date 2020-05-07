import math, random, asteroid, bullet
from geometry_msgs.msg import PoseStamped, Pose

class Environment():

    def __init__(self, mapDimensions, numAsteroids):

        # need dimensions of map for random asteroid creation
        # need number of asteroids to be generated
        # just assume dimensions are 400 x 400

        self.dictOfAsteroids = {}
        self.mapLength = mapDimensions[0]
        self.mapWidth = mapDimensions[1]
        self.mapHeight = 200
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

    def spawnAsteroids2(self):

        # generate x and y positions for asteroids and add them to list
        asteroidX = random.randint(-2, 2)
        asteroidY = random.randint(-2, 2)
        asteroidZ = 200
        ast = asteroid.Asteroid(asteroidX, asteroidY, asteroidZ)

        # very hacky but it works...lol
        x = "astr" + str(random.randint(0, 100000))
        while x in self.dictOfAsteroids:
            x = "astr" + str(random.randint(0, 100000))
        self.dictOfAsteroids[x] = ast

        print("LOG: Spawned Asteroids Succesfully")

    # Call after init, while the game is still running if we are out of asteroids from the initial population
    def spawnAsteroids(self):

        # generate x and y positions for asteroids and add them to list
        for i in range(0, self.numAsteroids):
            asteroidX = random.randint(0, self.mapLength)
            asteroidY = random.randint(0, self.mapWidth)
            asteroidZ = random.randint(0, 200)
            ast = asteroid.Asteroid(asteroidX, asteroidY, asteroidZ)

            # very hacky but it works...lol
            x = "astr" + str(random.randint(0, 100000))
            while x in self.dictOfAsteroids:
                x = "astr" + str(random.randint(0, 100000))
            self.dictOfAsteroids[x] = ast
        
        print("LOG: Spawned Asteroids Succesfully")

    def asteroidCollision(self):
        # hmmm
        # need Publisher/Subscriber for health (if asteroid hits player) and points (if player destroys asteroid)

        # position (x,y)
        #sub_particle = rospy.Subscriber("/particle_shooter", Pose, setBulletPos)

        #rospy.Subscriber("/particle_shooter", geometry_msgs/Pose, self.initBullet())

        for i in self.dictOfAsteroids:
            pos = self.dictOfAsteroids[i].getPos()
            
            # check if z pos is hitting the ground
            if pos[2] <= 25:
                self.gameOver = True
                return


            # x and y of bullet and asteroid match - bullet shot at asteroid - hit if within 50 units
            #if (abs(pos[0] - bulletPos[0]) <= 50) and (abs(pos[1] - bulletPos[1]) <= 50):
                #self.dictOfAsteroids[i].isHit = True

            
            # if pos[0] == bulletLoc[0] and pos[1] == bulletLoc[1] and 
 

            # if no asteroids have hit the ground yet
            # check if the players bullet hit an asteroid
            # do we need to worry about traveling time of bullet to asteroid?
            # or do we just assume its immediately hitting the asteroid?

            # subscribe to channel, listen for shot
                
    
    def updateAsteroids(self, dt):
        newDict = {}
        for i in self.dictOfAsteroids:
            
            # if hit, just continue, we dont want to update this asteroid and add it to tempList
            # only non-hit asteroids go on tempList
            if self.dictOfAsteroids[i].isHit:
                continue
            
            else:
                pos = self.dictOfAsteroids[i].getPos()
                newDict[i] = self.dictOfAsteroids[i]
                # x,y,z - z represents height from ground each asteroid is
                newDict[i].updatePos(pos[0], pos[1], pos[2] - (self.asteroidSpeed * dt))
        
        self.dictOfAsteroids = newDict

        if len(self.dictOfAsteroids) == 0:
            return -1
        else:
            return 0
    
    #def initBullet(self, x, y, z, vx, vy, vz):



if __name__ == "__main__":
    initEnv()
    print(listOfAsteroids)

    