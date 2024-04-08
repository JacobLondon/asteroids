import pygame

from .component import Component

class Label(Component):
    """@brief A simple component used for displaying text.
    """

    def __init__(self, controller, text: str, parent: Component=None, z: int=0):
        Component.__init__(self, controller, parent, z)
        self.text = text
        self.background = None

    def load(self):
        """@brief Load text details into Label.
        """
        pygame.font.init()
        self.width, self.height = self.font.size(self.text)
        self.set_anchor()

    def draw(self):
        """@brief Put the text into a surface and blit it to the display.
        """

        # draw the text in the component
        surface_args = [self.text, True, self.foreground, self.background]
        self.text_surface = self.font.render(*surface_args)
        self.controller.display.blit(self.text_surface, self.anchored_loc)
