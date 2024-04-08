import sys
sys.path.append('..')

from src import *

class ExampleController(Controller):

    def __init__(self):
        Controller.__init__(self, tick_rate=1, debug=True)

        # create a panel to make a background color
        self.color_panel = Panel(self)
        self.color_panel.background = Color['blue']
        # set the panel size to be the size of the window
        self.color_panel.width = self.screen_width
        self.color_panel.height = self.screen_height

        # create a text label
        self.hello_world_label = Label(self, 'Hello, World!')
        
        # create a button
        self.example_button = Button(self, 'Toggle Panel')
        # the button needs an action: create a func and assign it to action
        self.example_button.action = self.toggle_color_panel
        # to center the button on the screen, create a layout
        # all controllers have a background_panel which is the size of the screen
        # this creates a way of getting the center of any panel
        # anchor the button at its center (top left is default)
        self.example_button.anchor = self.example_button.center
        # set the location of the panel at the center of the screen
        self.example_button.loc = self.screen_relative.center

    '''Example method to toggle the visibility of color panel
    '''
    def toggle_color_panel(self):
        self.color_panel.visible = not self.color_panel.visible

if __name__ ==  '__main__':
    example = ExampleController()
    example.run()
    