from ..graphics import Color
from .component import Component
from .label import Label
from .layout import Relative
from .panel import Panel

class Bar(Component):
    """@brief A progress bar for showing progress on a task.
    """
    
    def __init__(self, controller, parent: Component=None, z: int=0):
        Component.__init__(self, controller, parent, z)
        self.percentage = 0
        self.text = '0 %'

        # loading bar has text over the loading color
        self.background = Color['darkgray']
        self.foreground = Color['green']
        self.font = self.controller.font['large']
        self.width, self.height = self.font.size(self.text)

        # panels for front/back, label for percentage text
        self.back_panel = Panel(self.controller, parent=self)
        self.front_panel = Panel(self.controller, parent=self)
        self.label = Label(self.controller, self.text, parent=self)
        self.label.anchor = self.center

    def load(self):
        """@brief Load all subcomponents to be in the correct order.
        """

        self.set_anchor()

        # update the background
        self.back_panel.loc = self.loc
        self.back_panel.width = self.width
        self.back_panel.height = self.height
        self.back_panel.background = self.background
        self.back_panel.anchor = self.anchor
        self.back_panel.visible = self.visible
        self.back_panel.load()

        # update foreground
        self.load_layout = Relative(self.back_panel)
        self.front_panel.loc = self.load_layout.northwest
        self.front_panel.width = self.width * self.percentage / 100
        self.front_panel.height = self.height
        self.front_panel.background = self.foreground
        self.front_panel.anchor = self.northwest
        self.front_panel.visible = self.visible
        self.front_panel.load()

        # update the label with the percentage
        self.center_layout = Relative(self.back_panel)
        self.label.loc = self.center_layout.center
        self.label.text = self.text
        self.label.font = self.font
        self.label.foreground = Color['black']
        self.label.background = None
        self.label.visible = self.visible
        self.label.load()

    def refresh_actions(self):
        """@brief Every frame check to see if the percentage changed.
        """
        self.text = str(self.percentage) + ' %'

    def increment(self, num_steps: int, step: int):
        """@brief Increase the percentage bar showing. \\
        @param num_steps The total number of steps needed for 100%. \\
        @param step The step that the program is at.
        """
        if step >= num_steps:
            self.percentage = 100
        elif step > 0:
            self.percentage = int(step / num_steps * 100)
        else:
            self.percentage = 0

        self.load()

    def complete(self):
        """@brief Set the bar to be full.
        """
        self.percentage = 100
        self.load()

    def reset(self):
        """@brief Set the bar to be empty.
        """
        self.percentage = 0
        self.load()