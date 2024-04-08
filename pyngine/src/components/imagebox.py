from ..graphics import Image
from .component import Component

class Imagebox(Component):
    """@brief Component to hold an image for simpler z index placement.
    """

    def __init__(self, controller, path: str, parent: Component=None, z: int=0):
        Component.__init__(self, controller, parent, z)
        self.text = 'Imagebox'
        
        # create image and set methods to be the same
        self.image = Image(path)
        self.reset = self.image.reset
        self.rotate_by = self.image.rotate_by
        self.rotate_to = self.image.rotate_to
        self.scale_by = self.image.scale_by
        self.scale_to = self.image.scale_to

    def load(self):
        """@brief Load the image itself into the component.
        """
        self.width = self.image.width
        self.height = self.image.height
        self.set_anchor()

        self.image.visible = self.visible
        self.image.loc = self.anchored_loc

    def draw(self):
        """@brief Draw using the image's draw method.
        """
        self.image.draw(self.controller.display)

