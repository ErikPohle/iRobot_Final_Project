import math, random, asteroid, bullet, tf, rospy
from geometry_msgs.msg import PoseStamped, Pose

class Environment():
    dictOfAsteroids = {}

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

        sub_laser = rospy.Subscriber("/laser", Pose, self.checkCollision)
        
        print("LOG: Environment Succesfully Initialized.")

        # rospy.init_node("Environment")

        # what should I publish to?
        # what am I publishing?
        # publisher = rospy.Publisher("???", PoseStamped, queue_size=10)
        # while publisher.get_num_connections() == 0:
        # 	rospy.sleep(1)

        # publisher.publish(msg)

    def spawnAsteroidsEveryX(self):

        # generate x and y positions for asteroids and add them to list
        asteroidX = random.uniform(-2, 2)
        asteroidY = random.uniform(-2, 2)
        asteroidZ = 100
        ast = asteroid.Asteroid(asteroidX, asteroidY, asteroidZ)

        # very hacky but it works...lol
        x = "astr" + str(random.randint(0, 100000))
        while x in self.dictOfAsteroids:
            x = "astr" + str(random.randint(0, 100000))
        self.dictOfAsteroids[x] = ast

        ''' WEIRD BEHAVIOR WHEN SPAWNING ASTEROIDS
        pub_asteroid = rospy.Publisher("/particle_shooter", Pose, queue_size=10)
        msg = Pose()
        msg.position.x = 0
        msg.position.y = 0
        msg.position.z = 10
        msg.orientation.z = -100
        print(msg)
        pub_asteroid.publish(msg)
        '''

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
    
    def checkCollision(self, msg):

        for i in self.dictOfAsteroids:
            pos = self.dictOfAsteroids[i].getPos()

            # x and y of laser and asteroid match - laser shot at asteroid - hit if within 2 units
            if (abs(pos[0] - msg.pose.x) <= 2) and (abs(pos[1] - msg.pose.y) <= 2):
                self.dictOfAsteroids[i].isHit = True
        
        # update asteroids - they arent moving, we just want to see if any have been hit
        # and if so remove them from dict
        updateAsteroids(0)

    def getDict(self):
        return self.dictOfAsteroids


if __name__ == "__main__":
    initEnv()
    print(listOfAsteroids)

    