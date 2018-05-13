import pygame, sys
import draw, scene
import pymunk, pymunk.pygame_util

from time import time
from pymunk.vec2d import Vec2d


class Engine():
    def __init__(self, size, **kwargs):
        self.size = Vec2d(size)

        # Physics
        self.gravity    = kwargs.get("gravity", Vec2d(0, -1000))
        self.iterations = kwargs.get("iterations", 10)
        self.damping    = kwargs.get("damping", 0.9)

        self.debug     = kwargs.get("debug", False)
        self.fps       = kwargs.get("fps", 60)

        self.delta         = 0
        self.running       = True
        self.calculatedFps = self.fps
        self.sceneManager = scene.sceneMananger()


        self.setupSpace()
        self.setupPygame()

        if self.debug:
            self.looped = 0
            self.drawOptions = pymunk.pygame_util.DrawOptions(self.screen)

    def setupSpace(self):
        self.space = pymunk.Space()
        self.space.gravity    = self.gravity
        self.space.iterations = self.iterations
        self.space.damping    = self.damping

    def setupPygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock  = pygame.time.Clock()

    def addScene(self, scene):
        scene.Engine = self
        self.sceneManager.add(scene)

    def setCurrentScene(self, scene):
        self.sceneManager.setCurrent(scene)

    def loop(self):
        if self.running and self.sceneManager.current != None:
            self.sceneManager.current.beforeLoop()
            self.screen.fill([0, 0, 0])

            data = self.sceneManager.current.loop()
            if data[0] == 1:
                self.running = False
                return 1

            if self.debug: self.space.debug_draw(self.drawOptions)
            else: draw.simple(self.screen, data[1])

            if self.calculatedFps == 0: fps = self.fps
            else: fps = self.calculatedFps

            self.space.step(1/fps)


            self.calculatedFps = self.clock.get_fps()
            pygame.display.update()
            self.clock.tick(fps)

            if self.debug:
                self.looped += 1
                if self.looped % self.calculatedFps:
                    print("There are {} objects in the current space at fps {}".format(len(self.space.shapes), fps))

            self.sceneManager.current.afterLoop()
