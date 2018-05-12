import event as _event
from time import time

DONE = 0
QUIT = 1

class eventManager():
    def __init__(self, scene):
        self.scene  = scene
        self.pygame = scene.pygame

        # event variables
        self.LEFTMBHELDSINCE  = 0
        self.RIGHTMBHELDSINCE = 0

        self.LEFTMBHELDFROM   = None
        self.RIGHTMBHELDFROM  = None

    def timeHeld(self, m):
        if m == 0 and self.LEFTMBHELDSINCE != -1: return time() - self.LEFTMBHELDSINCE
        elif m == 2 and self.RIGHTMBHELDSINCE != -1: return time() - self.RIGHTMBHELDSINCE

        return -1


    def manage(self):
        # This function will return an integer
        # Values are as shown
        # 0 = Everything has run fine
        # 1 = Quit button has been pressed
        events         = self.pygame.event.get()
        mouse_pos      = self.pygame.mouse.get_pos()
        mouse_state    = self.pygame.mouse.get_pressed()
        keyboard_state = self.pygame.key.get_pressed()

        data = [events, mouse_pos, mouse_state, keyboard_state]

        MOUSEBUTTONDOWN = False

        for event in events:
            if event.type == self.pygame.QUIT:
                return QUIT
            # Check against all events in the scene
            if event.type == self.pygame.MOUSEBUTTONDOWN: MOUSEBUTTONDOWN = True
            for sceneEvent in self.scene.events:
                if sceneEvent.on == event.type:
                    sceneEvent.run(data)


        for sceneEvent in self.scene.events:
            if MOUSEBUTTONDOWN:
                # Left mouse button pressed
                if sceneEvent.on == _event.LEFTMOUSEBUTTONPRESS and mouse_state[0]:
                    sceneEvent.run(data)
                # Right mouse button pressed
                if sceneEvent.on == _event.RIGHTMOUSEBUTTONPRESS and mouse_state[2]:
                    sceneEvent.run(data)
                # Any mouse button pressed
                if sceneEvent.on == _event.ANYMOUSEBUTTONPRESS:
                    sceneEvent.run(data)

                if mouse_state[0]:
                    self.LEFTMBHELDSINCE = time()
                    self.LEFTMBHELDFROM = mouse_pos
                if mouse_state[2]:
                    self.RIGHTMBHELDSINCE = time()
                    self.RIGHTMBHELDFROM = mouse_pos
            else:
                # Left mouse button held
                if sceneEvent.on == _event.LEFTMOUSEBUTTONHOLD and mouse_state[0]:
                    sceneEvent.run(data)
                # Right mouse button held
                if sceneEvent.on == _event.RIGHTMOUSEBUTTONHOLD and mouse_state[2]:
                    sceneEvent.run(data)
                # Any mouse button held
                if sceneEvent.on == _event.ANYMOUSEBUTTONHOLD and 1 in mouse_state:
                    sceneEvent.run(data)

            if sceneEvent.on in _event.keys:
                if keyboard_state[sceneEvent.on]:
                    sceneEvent.run(data)


        if not mouse_state[0]:
            self.LEFTMBHELDSINCE = -1
            self.LEFTMBHELDFROM = None
        if not mouse_state[2]:
            self.RIGHTMBHELDSINCE = -1
            self.RIGHTMBHELDFROM = None

        return data
