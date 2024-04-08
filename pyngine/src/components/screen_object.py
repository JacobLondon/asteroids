
class ScreenObject(object):
    """@brief Parent for all things shown on screen.
    """

    def __init__(self):
        self.loc = (0, 0)
        self.width = 0
        self.height = 0
        self.visible = True
