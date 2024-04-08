from ..graphics import Color
from .component import Component
from .panel import Panel
from .label import Label
from .layout import Relative

class Button(Component):
    """@brief Let user click in a designated area
    to perform an action set by the controller
    """

    def __init__(self, controller, text: str, parent: Component=None, z: int=0):
        """@brief Initialize a Button object. \\
        @param controller Reference to the controller the Button is in. \\
        @param text The text which appears on the button. \\
        @param parent The parent Component object in case Button should be a nested object. \\
        @param z The z index to put the Button on the Controller window at.
        """
        Component.__init__(self, controller, parent, z)

        # special properties of button
        self.text = text
        self.action = None
        self.scale = 1.5 
        self.pressed = False

        # default colors for the button
        self.background = Color['azure4']
        self.foreground = Color['black']
        self.hover = Color['gray80']
        self.font = self.controller.font['large']

        # adjust the button to the given scale size
        self.width, self.height = self.font.size(self.text)
        self.width *= self.scale
        self.height *= self.scale

        # use a panel as a background
        self.panel = Panel(self.controller, parent=self)
        self.panel.text = 'Button Panel'

        # use a label as the text on the button
        self.label = Label(self.controller, self.text, parent=self)
        self.label.anchor = self.center

    def load(self):
        """@brief Load all of the attributes of button
        and all of its subcomponents
        """

        self.set_anchor()

        # panel:

        # update the panel with button's members
        self.panel.loc = self.loc
        self.panel.width = self.width
        self.panel.height = self.height
        self.panel.background = self.background
        self.panel.anchor = self.anchor
        self.panel.visible = self.visible
        self.panel.load()

        # label:

        # label is always centered on button's panel
        self.center_layout = Relative(self.panel)
        self.label.loc = self.center_layout.center
        
        # label text is the same as the button's text
        self.label.text = self.text
        self.label.font = self.font

        # text color is button's foreground color
        self.label.foreground = self.foreground
        self.label.background = None
        self.label.visible = self.visible
        self.label.load()

    def refresh_actions(self):
        """@brief Do every frame
        Button has highlighting and a press action
        """

        # highlight the panel when the mouse is over the button
        if self.hovering:
            self.panel.background = self.hover
        else:
            self.panel.background = self.background

        # do action on focus
        if self.focused and self.action is not None:
            self.focused = False
            self.action()
