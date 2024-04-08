from .component import Component

class Panel(Component):
    """@brief A simple component used for displaying color.
    """

    def __init__(self, controller, parent: Component=None, z: int=0):
        Component.__init__(self, controller, parent, z)
        self.text = 'Panel'

    def load(self):
        """@brief Ensure the panel is anchored correctly.
        """
        self.set_anchor()

    def draw(self):
        """@brief Fill the area with color.
        """

        # draw the area of the panel
        self.controller.painter.fill_rect(
            self.anchored_loc[0],
            self.anchored_loc[1],
            self.width,
            self.height,
            self.background)
