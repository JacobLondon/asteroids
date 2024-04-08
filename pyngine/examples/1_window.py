import sys
sys.path.append('..')

from src import *

class ExampleController(Controller):

    def __init__(self):
        Controller.__init__(self, tick_rate=1, debug=True)

if __name__ ==  '__main__':
    # create a controller
    example = ExampleController()
    # run the controller
    example.run()
    