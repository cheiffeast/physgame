import Engine
from sceneExample import scene1

# GLOBALS
phys_iterations = 5
fps_calculated  = 60
running         = True
gravity         = [0, -1000]
delta           = 0
debug           = False
size            = [500, 500]
fps             = 60
n               = 0


# Setup engine
engine = Engine.Engine(size, gravity = gravity,
                       iterations = phys_iterations,
                       debug = debug, fps = fps)

scene = scene1(Engine.pygame, Engine.pymunk, engine.space, size)
engine.addScene(scene)
engine.setCurrentScene(scene)

while running:
    flag = engine.loop()
    if flag: running = False

Engine.pygame.quit()
