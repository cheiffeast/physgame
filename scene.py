from pickle import loads, dumps
from camera import Camera
from event import eventManager

class BaseScene():
    def __init__(self, pygame, pymunk, space, size, **kwargs):
        self.pygame = self.pyg = pygame
        self.pymunk = self.pym = pymunk
        self.space  = space
        self.size   = size

        self.name      = kwargs.get("name", None)

        self.eventManager  = eventManager(self)
        self.camera        = Camera(self)

        self.load()
        self.setupEvents()

    def beforeLoop(self):
        pass

    def afterLoop(self):
        pass

    def load(self):
        print("No loading function applied")
        return 0

    def setupEvents(self):
        print("No events setup")
        return 0

    def loop(self):
        return self.eventManager.manage(), self.camera.processData()

    def flipy(self, y):
        return -y + self.size[1]

    def listflipy(self, pos):
        return pos[0], self.flipy(pos[1])

    def addEvent(self, event):
        self.eventManager.add(event)


def SceneManange():
    def __init__(self, scenes = []):
        self.scenes = scenes

    def add(self, *args):
        for scene in args: self.scenes.append(scene)
