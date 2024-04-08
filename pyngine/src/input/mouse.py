from collections import defaultdict
import copy
from math import pi
import pygame

class Mouse(object):
    """@brief Control mouse presses/scrolling.
    """

    l_click = 1
    m_click = 2
    r_click = 3
    scroll_u = 4
    scroll_d = 5

    def __init__(self, controller):
        self.controller = controller

        # standard mouse controls
        self.presses = defaultdict(lambda: False)
        self.x, self.y = pygame.mouse.get_pos()
        self.l_clicked_x, self.l_clicked_y = -1, -1
        self.m_clicked_x, self.m_clicked_y = -1, -1
        self.r_clicked_x, self.r_clicked_y = -1, -1
        self.visible = True

        # first person view controls
        self.locked = False
        self.dx, self.dy = 0.0, 0.0
        self.last_dx = 0.0
        self.last_dy = 0.0
        self.yaw = 0.0
        self.pitch = 0.0
        # settings
        self.sensitivity = 0.8
        self.unit_step = 10.0
        self.smoothing = 0.3
        self.cutoff = 0.1

    def lock_update(self):
        """@brief Called every frame to lock the mouse if applicable.
        """
         
        # control direction based on movement
        self.yaw += float(self.dx * self.controller.delta_time * self.sensitivity)
        self.pitch += float(self.dy * self.controller.delta_time * self.sensitivity)
        self.yaw %= 2.0 * pi
        self.pitch %= 2.0 * pi
        
        # set vel to 0 if it is small else smooth the slowdown
        if abs(self.dx) < self.cutoff:
            self.dx = 0.0
        else:
            self.dx *= self.smoothing

        if abs(self.dy) < self.cutoff:
            self.dy = 0.0
        else:
            self.dy *= self.smoothing

        self.fix_mouse()
    
    def motion_update(self):
        """@brief Called every time the mouse moves to track position.
        Calculates dx/dy mouse movement if locked mode.
        """
        if self.locked:
            x, y = pygame.mouse.get_pos()
            new_dx = float((self.x - x) * self.controller.delta_time * self.sensitivity)
            new_dy = float((self.y - y) * self.controller.delta_time * self.sensitivity)

            # turning left/right
            if self.last_dx - new_dx < 0 and self.x < self.controller.center[0]:
                self.dx -= self.sensitivity * self.unit_step
            elif self.last_dx - new_dx > 0 and self.x > self.controller.center[0]:
                self.dx += self.sensitivity * self.unit_step

            # turning up/down
            if self.last_dy - new_dy < 0 and self.y < self.controller.center[1]:
                self.dy -= self.sensitivity * self.unit_step
            elif self.last_dy - new_dy > 0 and self.y > self.controller.center[1]:
                self.dy += self.sensitivity * self.unit_step

            self.last_dx = new_dx
            self.last_dy = new_dy

        self.x, self.y = pygame.mouse.get_pos()

    def set_visible(self, visible=True):
        """@brief Specify mouse visibility.
        """
        self.visible = visible
        pygame.mouse.set_visible(visible)

    def toggle_visibility(self):
        """@brief Toggles the mouse visible or not.
        """
        self.set_visible(not self.visible)

    def fix_mouse(self):
        """@brief Sets the mouse to the center of the screen.
        """
        pygame.mouse.set_pos(self.controller.center)
        self.x, self.y = pygame.mouse.get_pos()

    def actions(self):
        """@brief Mouse button press action checks.
        """
        if self.presses[Mouse.l_click]:
            self.l_clicked_x, self.l_clicked_y = pygame.mouse.get_pos()
            self.controller.keyboard.typing = copy.copy(self.controller.background_panel.focused)
            self.l_click_down()
            
        if self.presses[Mouse.m_click]:
            self.m_clicked_x, self.m_clicked_y = pygame.mouse.get_pos()
            self.m_click_down()

        if self.presses[Mouse.r_click]:
            self.r_clicked_x, self.r_clicked_y = pygame.mouse.get_pos()
            self.r_click_down()

        if self.presses[Mouse.scroll_up]:
            self.scroll_up()
            self.presses[Mouse.scroll_up] = False

        if self.presses[Mouse.scroll_down]:
            self.scroll_down()
            self.presses[Mouse.scroll_down] = False

    def l_click_down(self):
        pass
    def m_click_down(self):
        pass
    def r_click_down(self):
        pass
    def scroll_up(self):
        pass
    def scroll_down(self):
        pass