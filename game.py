import pyEngine
#from sceneExample import scene1
from example import main

# GLOBALS
phys_iterations = 1
fps_calculated  = 60
running         = True
gravity         = [0, -1000]
delta           = 0
debug           = True
size            = [500, 500]
fps             = 60
n               = 0


# Setup engine
engine = pyEngine.Engine(size, gravity = gravity,
                       iterations = phys_iterations,
                       debug = debug, fps = fps)

#scene = scene1(pyEngine.pygame, pyEngine.pymunk, engine.space, size)
scene = main(pyEngine.pygame, pyEngine.pymunk, engine.space, size)

engine.addScene(scene)
engine.setCurrentScene(scene)

while running:
    flag = engine.loop()
    if flag: running = False

pyEngine.Engine.pygame.quit()
