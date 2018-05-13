from pyEngine import event, scene
from random import randint

class main(scene.BaseScene):
    def __init__(self, pygame, pymunk, space, size, **kwargs):
        scene.BaseScene.__init__(self, pygame, pymunk, space, size, **kwargs)

        # Custom vars
        self.counter = 0


    def load(self):
        print("Loading scene")

        #Creating flooring
        floor_shape = self.pymunk.Poly(self.space.static_body, [(0, 0), (500, 0), (500, 50), (0, 50)])


        #Add floor to the pymunk space
        self.space.add(floor_shape)

    def beforeLoop(self):
        self.counter += 1
        if self.counter > 300:
            for body in self.space.bodies:
                if body.position[1] < -1000:
                    self.space.remove(body, body.shapes)
            self.counter = 0

            print(len(self.space.shapes))

    def spawnRandom(self, data):
        pos = [randint(10, 490), 400]
        mass = randint(10, 100)
        radius = int(mass / 10)

        #Create a ball
        ball = self.pymunk.Body(mass)
        ball_shape = self.pymunk.Circle(ball, radius)

        ball.position = pos
        ball.moment = self.pymunk.moment_for_circle(mass, 0, radius)
        ball.friction = 0.5
        ball.elasticity = 0.7

        self.space.add(ball, ball_shape)


    def setupEvents(self):
        randomEvent = event.Event(event.LEFTMOUSEBUTTONHOLD, self.spawnRandom)
        self.eventManager.add(randomEvent)
