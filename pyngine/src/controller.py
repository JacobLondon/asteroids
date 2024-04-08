import collections
import pygame
from threading import Thread, active_count as active_threads
import time

from .components import Component, Grid, Panel, Relative
from .graphics import Color, Font, Painter
from .input import Keyboard, Mouse
from .interface import Interface

class Controller(Interface):
    """@brief Handle drawing things to screen and user input from mouse/keyboard.

    This class is meant to be extended for simple functionality.
    """

    def __init__(self, name='Pyngine', resolution=(400,400), grid=(40,40), fps=60, icon='icon.png', tick_rate: int=0, debug: bool=False):
        """@brief Initialize a controller object. \\
        @param tick_rate The rate the tick thread will loop events at. \\
        @param debug Display debug information every tick if True.
        """

        Interface.__init__(self, name, resolution, grid, fps, icon)

        # interface with pygame to draw shapes/lines/areas
        self.painter = Painter(self)
        # default font for the controller
        self.font = Font('Calibri', scale=1)
        
        # tools for tracking fps/time to update
        self.update_time = time.time()
        self.delta_time = 0
        self.fps = 0

        # close the controller
        self.done = False
        # close pygame and the display
        self.quit = False

        # control input
        self.keyboard = Keyboard(self)
        self.mouse = Mouse(self)
        # all custom key events defined by the user
        self.events = {}

        # regularly do every tick
        self.tick_rate = tick_rate
        if self.tick_rate > 0:
            self._tick_thread = Thread(target=self._tick)
            self.ticking = True
            self.debug = debug
        else:
            self._tick_thread = None
            self.ticking = False
            self.debug = False

        # load/refresh components/drawers based on their z index
        self._components = collections.OrderedDict()
        self._component_index = 0

        # create an empty panel for components to be on
        self.background_panel = Panel(self)
        self.background_panel.width = self.resolution[0]
        self.background_panel.height = self.resolution[1]
        self.background_panel.background = Color['gray5']

        # create default screen layouts based on background panel
        self.screen_grid = Grid(self.background_panel, self.grid_width, self.grid_height)
        self.screen_relative = Relative(self.background_panel)

    def __str__(self):
        """@brief Get the component.text and its z index for all components.
        """
        for z in self._components.keys():
            print('z = ', str(z), '\tComponent:', str(self._components[z]))

    def _add_component(self, component: Component, z: int=0):
        """@brief Add components to the OrderedDict of components based on their z index.
        """
        # no z index given
        if z == 0:
            # append in next available index
            while self._component_index in self._components:
                self._component_index += 1
            self._components[self._component_index] = component
        # insert at given z index
        else:
            if z in self._components:
                print('Warning: overriding component at z index:', z)
            self._components[z] = component

    def _add_event(self, event):
        """@brief Add an event specified by a key and an action function.
        """
        self.events[event.keys] = event

    def _call_events(self):
        """@brief Call all events specified by the user the they are occurring.
        """
        # each key is a tuple with a combo of keypresses
        for keycombo in self.events.keys():
            # check to see if all given keys are pressed
            pressed = all(self.keyboard.presses[k] for k in keycombo)

            # do the action if the combination is fulfilled
            if pressed or self.mouse.presses[keycombo]:
                self.events[keycombo].action(*self.events[keycombo].args)

    def _draw_components(self):
        """@brief Draw all components to screen in their z index order.
        """
        for key in self._components:
            self._components[key].refresh()

    def _load(self):
        """@brief Load components before entering program loop to ensure z index order is correct.
        """
        self._components = collections.OrderedDict(sorted(self._components.items(), reverse=False))
        for key in self._components:
            self._components[key].load()

    def _tick(self):
        """@brief Tick in another thread to handle custom ticking actions and debug messages.
        """
        while self.ticking:
            self.debug_actions()
            self.tick_actions()
            time.sleep(1 / self.tick_rate)

    def debug_actions(self):
        """@brief Show thread count and frames per second.
        """
        if self.debug:
            print('Threads:', active_threads(), 'FPS:', self.fps, end='\r')

    def tick_actions(self):
        """@brief Empty method meant to be overwritten by controller children.
        """
        pass

    def elapsed_time(self):
        """@brief Find how much time has passed since the last update.
        """
        t = time.time() - self.update_time
        # make sure that t is not zero, prevent div by zero
        return t if not t == 0 else self.delta_time

    def _handle_update(self):
        """@brief Everyframe, update the screen.
        """

        # if mouse is locked, reset it to locked position
        if self.mouse.locked:
            self.mouse.lock_update()

        self._draw_components()

        # pygame update
        self.update()

        # record update
        self.delta_time = self.elapsed_time()
        self.update_time = time.time()
        self.fps = 1 / self.delta_time

    def run(self):
        """@brief The program loop
        Includes pre-program loop actions, the loop, and updating.
        """
        # if the controller loading was cancelled before opening
        if self.done:
            self.on_close()

        # pre-program loop actions
        self._load()
        if self.tick_rate > 0:
            self._tick_thread.start()

        while not self.done:

            # receive mouse input
            self.mouse.actions()
            
            # handle all pygame events per frame
            for event in pygame.event.get():
                self._handle_event(event)
            
            # call all custom user defined events
            self._call_events()

            self._handle_update()

        # close the controller and handle close actions
        self.close()

    def _handle_event(self, event):
        """@brief Given a Pygame event, record it in its
        respective mouse/keyboard presses DefaultDict.
        This dict determines pressing state for each key/button.
        """

        # top right corner X
        if event.type == pygame.QUIT:
            self.exit_program()

        # player starts doing actions
        elif event.type == pygame.KEYDOWN:
            self.keyboard.presses[event.key] = True

        # player stops doing actions
        elif event.type == pygame.KEYUP:
            self.keyboard.presses[event.key] = False

        # control user text input
        if self.keyboard.typing and event.type == pygame.KEYDOWN:
            self.keyboard.typing_actions(event)

        # mouse stops clicking/scrolling
        if event.type == pygame.MOUSEBUTTONUP:
            if not event.button == Mouse.scroll_up \
                and not event.button == Mouse.scroll_down:
                self.mouse.presses[event.button] = False

        # mouse starts clicking/scrolling
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse.presses[event.button] = True

        # mouse moves
        self.mouse.motion_update()

    def exit_program(self):
        """@brief Exit the program loop and program.
        """
        self.exit_loop()
        self.quit = True

    def exit_loop(self):
        """@brief Method for stopping the program loop.
        """
        self.done = True
        self.ticking = False

    def close(self):
        """@brief Handle closing the controller by
        stopping threads, doing custom close actions,
        and opening another controller if given.
        """
        # close actions
        self.ticking = False
        if self._tick_thread:
            self._tick_thread.join()

        # shutdown the program or open the parent container
        if self.quit:
            pygame.quit()
        self.on_close()

    def on_close(self):
        """@brief Stop the program by default.
        Override in child by importing a controller and running it here.
        """

        # by default, just close the program
        pygame.quit()
