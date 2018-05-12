import event
from scene import BaseScene
from math import sin, cos, pi

class scene1(BaseScene):
    def __init__(self, pygame, pymunk, space, size, **kwargs):
        self.deadZone = 1
        self.other    = 2
        BaseScene.__init__(self, pygame, pymunk, space, size, **kwargs)



    def load(self):
        self.generateFloor()

        wall        = self.pym.Body(body_type = self.pym.Body.STATIC)
        wall_shape1 = self.pym.Segment(wall, (400, 50), (400, 300), 1)
        wall_shape2 = self.pym.Segment(wall, (100, 100), (100, 300), 1)
        self.space.add([wall_shape1, wall_shape2])


        ball = self.pym.Body(100, 10)
        ball_shape = self.pym.Poly(ball, ((0, 0), (10, 0), (10, 100), (0, 200)))
        ball.position = (250, 200)
        ball.moment = self.pym.moment_for_poly(100, ((0, 0), (10, 0), (10, 100), (0, 200)))

        j = self.pym.PivotJoint(self.space.static_body, ball, (250, 350), (5, 100))


        self.space.add(ball, ball_shape, j)


        self.deadZoneHandler = self.space.add_collision_handler(self.other, self.deadZone)
        self.deadZoneHandler.pre_solve = self.deleteBall


    def generateFloor(self):
        floor        = self.pymunk.Body(body_type = self.pymunk.Body.STATIC)
        floor_shape  = self.pymunk.Segment(floor, (100, 100), (375, 100), 1)
        floor_shape2 = self.pymunk.Segment(floor, (-100000, -10000), (100000, -10000), 1)
        floor_shape2.collision_type = self.deadZone
        floor_shape.friction = 2
        floor_shape.elasticity = 0.2

        self.space.add([floor_shape, floor_shape2])

    def spawnBall(self, mass, radius, pos = None):
        if pos == None: x, y = self.camera.trueMouse(self.pygame.mouse.get_pos())
        else: x, y = pos
        y = flipY(y, self.size[1])

        ball       = self.pymunk.Body(mass, 10)
        ball_shape = self.pymunk.Circle(ball, radius, (0, 0))


        ball.position = (x, y)
        ball_shape.friction = 0.2
        ball_shape.elasticity = 0.7
        ball_shape.collision_type = self.other

        self.space.add(ball, ball_shape)

    def zoomIn(self, data):
        self.camera.zoom += 0.01

    def zoomOut(self, data):
        self.camera.zoom -= 0.01


    def stress(self, n):
        for i in range(n):
            self.spawnBall(100000, 2, ((250 - n) + (2 * i), 0))

    def spawnBigBall(self, data):
        self.spawnBall(10000, 100)

    def spawnSmallBall(self, data):
        self.spawnBall(1, 5)

    def spawnParticleBall(self, data):
        self.spawnBall(1, 5, [250, 0])

    def deleteBall(self, arbiter, space, data):
        self.space.remove(arbiter.shapes[0], arbiter.shapes[0].body)

        # Some do not register the collision, hence we need to check for them
        missed = [[shape, shape.body] for shape in self.space.shapes if shape.body.position[1] < -10000 or shape.body.position[1] > 10000]
        for shape in missed:
            self.space.remove(shape[0], shape[1])


        return 0

    def moveLeft(self, data):
        self.camera.offset[0] += 1

    def moveRight(self, data):
        self.camera.offset[0] -= 1

    def moveUp(self, data):
        self.camera.offset[1] += 1

    def moveDown(self, data):
        self.camera.offset[1] -= 1


    def explosion(self, n, vel):
        step = (2 * pi) / n

        for i in range(n):
            xvel = vel * sin(step * i)
            yvel = vel * cos(step * i)

            ball       = self.pymunk.Body(10, 10)
            ball_shape = self.pymunk.Circle(ball, 2, (0, 0))


            ball.position = self.camera.trueMouse(self.pygame.mouse.get_pos())
            ball.position = [ball.position[0], flipY(ball.position[1], self.size[1])]
            ball.velocity = [xvel, yvel]
            ball_shape.friction = 0.2
            ball_shape.elasticity = 0.7
            ball_shape.collision_type = self.other

            self.space.add(ball, ball_shape)

    def boxExplosion(self, n, v, size = [10, 10]):
        step = (2 * pi) / n

        for i in range(n):
            xvel = v * sin(step * i)
            yvel = v * cos(step * i)

            box = self.pymunk.Body(10)
            box_shape = self.pymunk.Poly(box, ((0, 0), (size[0], 0), (size[0], size[1]), (0, size[1])))

            box.position = self.camera.trueMouse(self.pygame.mouse.get_pos())
            box.moment = self.pymunk.moment_for_poly(10, ((0, 0), (size[0], 0), (size[0], size[1]), (0, size[1])))
            box.velocity = [xvel, yvel]
            box_shape.collision_type = self.other
            box_shape.friction = 1


            self.space.add(box, box_shape)


    def smallExplosion(self, data):
        self.explosion(100, 1000)

    def smallBoxExplosion(self, data):
        self.boxExplosion(10, 1000)


    def setupEvents(self):
        self.events.append(event.Event(event.RIGHTMOUSEBUTTONHOLD, self.zoomOut))
        self.events.append(event.Event(event.LEFTMOUSEBUTTONHOLD, self.zoomIn))
        self.events.append(event.Event(event.K_a, self.moveLeft))
        self.events.append(event.Event(event.K_d, self.moveRight))
        self.events.append(event.Event(event.K_w, self.moveUp))
        self.events.append(event.Event(event.K_s, self.moveDown))
        self.events.append(event.Event(event.K_SPACE, self.smallExplosion))

def flipY(y, ys):
    return -y + ys
