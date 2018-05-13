from time import time

# All custom events
# MOUSE CUSTOM EVENTS
LEFTMOUSEBUTTONHOLD   = "LMB"
LEFTMOUSEBUTTONPRESS  = "LMBP"
RIGHTMOUSEBUTTONHOLD  = "RMB"
RIGHTMOUSEBUTTONPRESS = "RMBP"
ANYMOUSEBUTTONHOLD    = "AMBH"
ANYMOUSEBUTTONPRESS   = "AMBP"

# KEYBOARD EVENT
from pygame.locals import *

keys = [K_BACKSPACE, K_TAB, K_CLEAR, K_RETURN, K_PAUSE, K_ESCAPE, K_SPACE, K_EXCLAIM,
        K_QUOTEDBL, K_HASH, K_DOLLAR, K_AMPERSAND, K_QUOTE, K_LEFTPAREN, K_RIGHTPAREN,
        K_ASTERISK, K_PLUS, K_COMMA, K_MINUS, K_PERIOD, K_SLASH, K_0, K_1, K_2, K_3,
        K_4, K_5, K_6, K_7, K_8, K_9, K_COLON, K_SEMICOLON, K_LESS, K_EQUALS, K_GREATER,
        K_QUESTION, K_AT, K_LEFTBRACKET, K_BACKSLASH, K_RIGHTBRACKET, K_CARET, K_UNDERSCORE,
        K_BACKQUOTE, K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m, K_n, K_o,
        K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z, K_DELETE, K_KP0, K_KP1, K_KP2,
        K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9, K_KP_PERIOD, K_KP_DIVIDE, K_KP_MULTIPLY,
        K_KP_MINUS, K_KP_PLUS, K_KP_ENTER, K_KP_EQUALS, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_INSERT,
        K_HOME, K_END, K_PAGEUP, K_PAGEDOWN, K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8,
        K_F9, K_F10, K_F11, K_F12, K_F13, K_F14, K_F15, K_NUMLOCK, K_CAPSLOCK, K_SCROLLOCK,
        K_RSHIFT, K_LSHIFT, K_RCTRL, K_LCTRL, K_RALT, K_LALT, K_RMETA, K_LMETA, K_LSUPER,
        K_RSUPER, K_MODE, K_HELP, K_PRINT, K_SYSREQ, K_BREAK, K_MENU, K_POWER, K_EURO]

class Event():
    def __init__(self, on, function = None):
        self.eventOn = self.on = on
        if function: self.run = function

    def run(self, data):
        print("Empty event")

class eventManager():
    def __init__(self, scene, events = []):
        self.scene  = scene
        self.events = events
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

    def add(self, *args):
        for event in args: self.events.append(event)


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
            for sceneEvent in self.events:
                if sceneEvent.on == event.type:
                    sceneEvent.run(data)


        for sceneEvent in self.events:
            if MOUSEBUTTONDOWN:
                # Left mouse button pressed
                if sceneEvent.on == LEFTMOUSEBUTTONPRESS and mouse_state[0]:
                    sceneEvent.run(data)
                # Right mouse button pressed
                if sceneEvent.on == RIGHTMOUSEBUTTONPRESS and mouse_state[2]:
                    sceneEvent.run(data)
                # Any mouse button pressed
                if sceneEvent.on == ANYMOUSEBUTTONPRESS:
                    sceneEvent.run(data)

                if mouse_state[0]:
                    self.LEFTMBHELDSINCE = time()
                    self.LEFTMBHELDFROM = mouse_pos
                if mouse_state[2]:
                    self.RIGHTMBHELDSINCE = time()
                    self.RIGHTMBHELDFROM = mouse_pos
            else:
                # Left mouse button held
                if sceneEvent.on == LEFTMOUSEBUTTONHOLD and mouse_state[0]:
                    sceneEvent.run(data)
                # Right mouse button held
                if sceneEvent.on == RIGHTMOUSEBUTTONHOLD and mouse_state[2]:
                    sceneEvent.run(data)
                # Any mouse button held
                if sceneEvent.on == ANYMOUSEBUTTONHOLD and 1 in mouse_state:
                    sceneEvent.run(data)

            if sceneEvent.on in keys:
                if keyboard_state[sceneEvent.on]:
                    sceneEvent.run(data)


        if not mouse_state[0]:
            self.LEFTMBHELDSINCE = -1
            self.LEFTMBHELDFROM = None
        if not mouse_state[2]:
            self.RIGHTMBHELDSINCE = -1
            self.RIGHTMBHELDFROM = None

        return data
