import pygame
from collections import defaultdict

class Keyboard(object):
    """@brief Used by controllers to track keyboard input.
    """

    def __init__(self, controller):
        self.controller = controller

        self.typing = False
        self.shift = False
        self.typed_text = ''

        # key presses which are not displayed as text
        self.ignored_keys = [
            pygame.K_CAPSLOCK, pygame.K_LSHIFT, pygame.K_RSHIFT,
            pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT,
            pygame.K_LSUPER, pygame.K_RSUPER, pygame.K_NUMLOCK, pygame.K_PRINT,
            pygame.K_SCROLLOCK, pygame.K_PAUSE, pygame.K_INSERT, pygame.K_HOME,
            pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_DELETE, pygame.K_END,
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6,
            pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12]

        # keys when shifted
        self.shifted_keys = {
            pygame.K_1:'!', pygame.K_2:'@', pygame.K_3:'#',
            pygame.K_4:'$', pygame.K_5:'%', pygame.K_6:'^',
            pygame.K_7:'&', pygame.K_8:'*', pygame.K_9:'(',
            pygame.K_0:')',
            pygame.K_BACKQUOTE:'~', pygame.K_MINUS:'_', pygame.K_EQUALS:'+',
            pygame.K_LEFTBRACKET:'{', pygame.K_RIGHTBRACKET:'}',
            pygame.K_BACKSLASH:'|', pygame.K_SEMICOLON:':',
            pygame.K_QUOTE:'"', pygame.K_PERIOD:'<', pygame.K_COMMA:'>',
            pygame.K_SLASH:'?'}

        self.presses = defaultdict(lambda: False)

    def typing_actions(self, event):
        """@brief Set typed text based on a pygame keypress event.
        """
        self.shift = self.presses[pygame.K_RSHIFT] or \
            self.presses[pygame.K_LSHIFT]

        # special keys
        if self.presses[pygame.K_BACKSPACE]:
            self.typed_text = self.typed_text[:-1]
        elif self.presses[pygame.K_TAB]:
            self.typed_text += ' ' * 4
        elif self.presses[pygame.K_KP_ENTER] or self.presses[pygame.K_ESCAPE] or self.presses[pygame.K_RETURN]:
            self.typing = False
        elif self.presses[pygame.K_SPACE]:
            self.typed_text += ' '

        elif self.shift:
            # shifted letter keys
            if pygame.key.name(event.key).isalpha():
                self.typed_text += pygame.key.name(event.key).upper()

            # special shifted keys
            if event.key in self.shifted_keys:
                self.typed_text += self.shifted_keys[event.key]

        # keypad keys
        elif all(bracket in pygame.key.name(event.key) for bracket in ['[', ']']):
            self.typed_text += pygame.key.name(event.key)[1]

        # all other keys
        elif event.key not in self.ignored_keys:
            self.typed_text += pygame.key.name(event.key)
