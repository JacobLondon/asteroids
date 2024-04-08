import copy
import time
from threading import Thread

from ..graphics import Color
from .component import Component
from .panel import Panel
from .label import Label
from .layout import Relative

class Textbox(Component):
    """@brief Box for users to type text into.
    """

    def __init__(self, controller, num_chars: int=15, parent: Component=None, z: int=0):
        Component.__init__(self, controller, parent, z)

        # textbox specific details
        self.num_chars = num_chars
        self.typing = False
        self.cursor_active = False
        self.cursor_rate = 0.5

        self.background = Color['white']
        self.foreground = Color['black']
        self.font = self.controller.font['large']

        # textbox made with a panel
        self.panel = Panel(self.controller, parent=self)
        # typed text goes into the label
        self.label = Label(self.controller, self.text, parent=self)

        # set size to be arbitrarily wide
        self.width, self.height = self.font.size('o' * self.num_chars)
        self.current_width = self.font.size(self.label.text)[0]

        # have a flashing cursor
        self.cursor_char = '|'
        self.cursor_offset = 3
        self.cursor_width = self.font.size(self.cursor_char)[0]
        self.cursor_label = Label(self.controller, self.cursor_char)
        self.cursor_label.visible = False

    def load(self):
        """@brief Load all subcomponents of textbox.
        """

        self.set_anchor()

        # load panel
        self.panel.anchor = self.anchor
        self.panel.loc = self.loc
        self.panel.background = self.background
        self.panel.width = self.width
        self.panel.height = self.height
        self.panel.load()

        # update the label with button's members
        self.center_layout = Relative(self.panel)
        self.label.loc = self.center_layout.northwest
        self.label.text = self.text
        self.label.font = self.font
        self.label.foreground = self.foreground
        self.label.background = None
        self.label.load()

        # keep the cursor on the far right of the text
        w = self.label.font.size(self.label.text)[0]
        self.cursor_label.loc = self.center_layout.northwest
        cursor_x_offset = self.cursor_label.loc[0] + w - self.cursor_width / self.cursor_offset
        self.cursor_label.loc = (cursor_x_offset, self.cursor_label.loc[1])
        
        self.cursor_label.font = self.font
        self.cursor_label.foreground = self.foreground
        self.cursor_label.background = None
        self.cursor_label.load()

    def refresh_actions(self):
        """@brief Every frame, check if typing is occurring.
        If it is, load text from the controller's keyboard,
        and handle cursor flashing.
        """
        # typing setup
        if self.focused and not self.typing:
            self.controller.keyboard.typing = True
            self.typing = True
            self.controller.keyboard.typed_text = copy.copy(self.text)

        # when the user is typing
        if self.focused and self.typing:

            # determine if the width of the text is wider than textbox's width
            new_width = self.font.size(self.controller.keyboard.typed_text)[0]

            # remove the new character if there is no room left
            if new_width > self.width:
                self.controller.keyboard.typed_text = self.controller.keyboard.typed_text[:-1]
            
            # update text because there is room
            else:
                self.text = copy.copy(self.controller.keyboard.typed_text)
                self.current_width = self.font.size(self.text)[0]

            self.load()

        # start/stop typing
        self.typing = self.focused

        # setup cursor flashing
        if self.typing and not self.cursor_active:
            self.cursor_active = True
            Thread(target=self.flash_cursor, daemon=True).start()

    def draw(self):
        """@brief Refresh all subcomponents after typing has been checked.
        """
        self.panel.refresh()
        self.label.refresh()
        self.cursor_label.refresh()

    def flash_cursor(self):
        """@brief Running and close down of cursor flashing.
        """
        while self.typing:
            self.cursor_label.visible = not self.cursor_label.visible
            time.sleep(self.cursor_rate)

            # stop the cursor flashing when it should not be
            if not self.controller.keyboard.typing:
                self.focused = False
                break

        # reset the cursor state to be gone
        self.cursor_active = False
        self.cursor_label.visible = False
