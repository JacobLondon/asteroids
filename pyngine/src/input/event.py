
class Event(object):
    """@brief Event object is used to simplify connecting a
    keypress or set of keypresses to a given function.
    """

    def __init__(self, controller, action=None, args=(), keys=()):
        """@brief Setup the event into the controller. \\
        @param Controller the parent controller. \\
        @param key Tuple of pygame.key presses. \\
        @param action A function to call on when the key combination is pressed
        """
        if type(keys) == tuple:
            self.keys = keys
        else:
            self.keys = tuple([keys])
        self.action = action
        if type(args) == tuple:
            self.args = args
        else:
            self.args = tuple([args])
        self.controller = controller
        self.controller._add_event(self)

    def halt(self):
        """@brief Forcibly stop the input from being read until the next input.
        """
        for key in self.keys:
            self.controller.keyboard.presses[key] = False
