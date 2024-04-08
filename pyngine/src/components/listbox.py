from ..graphics import Color
from ..input import Mouse
from .component import Component
from .layout import Grid
from .panel import Panel

class Listbox(Component):
    """@brief Component to hold many subcomponents in a
    vertically scrolling list.
    """

    def __init__(self, controller, parent: Component=None, z: int=0):
        Component.__init__(self, controller, parent)
        self.text = 'Listbox'

        # listbox specific details
        self.scrolled_index = 0     # initial scrolled index
        self.num_visible_items = 5  # number of subcomponents visible in given area
        self.height_scaling = 0.9   # vertical space each components takes (<1 gives a clear border)

        self.background = Color['darkgray']

    def load(self):
        """@brief Load all subcomponents and set their visiblity based on their index.
        """
        
        # calculate height by given height scaling
        self.item_height = self.height / self.num_visible_items * self.height_scaling
        self.set_anchor()

        # create a vertical grid to place all subcomponents in
        self.item_layout = Grid(self, 1, self.num_visible_items)

        # traverse all components
        for i in range(len(self.subcomponents)):

            # set sizes to fill the width/height so all subcomponents are the same size
            self.subcomponents[i].loc = self.item_layout.pixel_at(0, i - self.scrolled_index)
            self.subcomponents[i].width = self.width
            self.subcomponents[i].height = self.item_height
            self.subcomponents[i].anchor = self.northeast

            # set visibility if on/off scrolled area
            if i < self.scrolled_index:
                self.subcomponents[i].visible = False
            elif self.scrolled_index <= i < self.scrolled_index + self.num_visible_items:
                self.subcomponents[i].visible = self.visible
            else:
                self.subcomponents[i].visible = False
            
            # load all subcomponents to apply visibility, etc...
            self.subcomponents[i].load()

    def refresh_actions(self):
        """@brief Allow scrolling control if the mouse is over the listbox.
        """

        # scroll control
        if self.hovering:
            if self.controller.mouse.presses[Mouse.scroll_up]:
                self.scroll_up()
            elif self.controller.mouse.presses[Mouse.scroll_down]:
                self.scroll_down()

    def scroll_up(self):
        """@brief Scroll up with bounds check.
        """
        if self.scrolled_index - 1 >= 0:
            self.scrolled_index -= 1
            self.load()

    def scroll_down(self):
        """Scroll down with bounds check.
        """
        if self.scrolled_index + self.num_visible_items < len(self.subcomponents):
            self.scrolled_index += 1
            self.load()

    def add(self, component: Component):
        """@brief Simple way of adding a component to the listbox.
        """
        self.subcomponents.append(component)

    def remove(self, component: Component):
        """@brief Simple way of removing a component to the listbox.
        """
        self.subcomponents.remove(component)
