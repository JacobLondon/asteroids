import sys
sys.path.append('..')

from src import *

class ExampleController(Controller):

    def __init__(self):
        Controller.__init__(self, tick_rate=1, debug=False)

        self.test_textbox = Textbox(self)
        self.test_textbox.loc = self.screen_relative.center
        self.test_textbox.anchor = self.test_textbox.center

if __name__ == '__main__':
    example = ExampleController()
    example.run()
