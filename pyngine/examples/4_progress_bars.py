import sys, time
from threading import Thread
sys.path.append('..')

from src import *

class ExampleController(Controller):

    def __init__(self):
        Controller.__init__(self, tick_rate=1, debug=False)

        # prevent multiple threads from accessing the timer
        self.timer_on = False
        
        # components to control the timer
        self.start_button = Button(self, 'Start')
        self.start_button.action = self.start_timer
        self.reset_button = Button(self, 'Reset')
        self.reset_button.loc = self.screen_grid.pixel_at(0, 8)
        self.reset_button.action = self.reset_timer

        # details about the timer duration, defaulting to 5s
        self.duration_label = Label(self, 'Duration (s)')
        self.duration_label.loc = self.screen_grid.pixel_at(4, 29)
        self.duration_textbox = Textbox(self)
        self.duration_textbox.loc = self.screen_grid.pixel_at(4, 32)
        self.duration_textbox.text = '5'

        # loading bar details and width setting
        self.timer_bar = Bar(self)
        self.timer_bar.loc = self.screen_relative.center
        self.timer_bar.anchor = self.timer_bar.center
        self.timer_bar.width = self.screen_width * 0.8


    """Start the timer in another thread to prevent the main window from freezing"""
    def start_timer(self):
        if not self.timer_on:
            Thread(target=self.timer).start()

    """Run the timer"""
    def timer(self):
        self.timer_on = True
        
        # break the job down into steps
        steps = 100
        sleep_step = float(self.duration_textbox.text) / steps

        # fill the bar until full
        for step in range(steps):
            self.timer_bar.increment(num_steps=steps, step=step)
            # some calculation, represented by sleep
            time.sleep(sleep_step)
        # make sure the bar is filled when done
        self.timer_bar.complete()

        self.timer_on = False

    """Reset the timer"""
    def reset_timer(self):
        self.timer_bar.reset()
        
if __name__ == '__main__':
    example = ExampleController()
    example.run()
    