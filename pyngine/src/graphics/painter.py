import pygame

from .color import colors as Color

class Painter(object):
    """@brief Helper class to use Pygame for drawing lines/shapes/areas.
    """
    
    def __init__(self, controller):
        self.display = controller.display
        self.px = controller.px
        self.py = controller.py

    def fill_grid(self, gx, gy, color=Color['white']):
        """@brief Fill tile with color."""
        area = [gx * self.px, gy * self.py, self.px, self.py]
        pygame.draw.rect(self.display, color, area)

    def fill_rect(self, x, y, width, height, color=Color['white']):
        """@brief Fill area with color."""
        area = [x, y, width, height]
        pygame.draw.rect(self.display, color, area)

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color=Color['white']):
        """@brief Fill the triangle with color."""
        pointlist = [(x0, y0), (x1, y1), (x2, y2)]
        pygame.draw.polygon(self.display, color, pointlist)

    def draw_line(self, x0, y0, x1, y1, color=Color['white']):
        """@brief Draw line from x0, y0 to x1, y1."""
        pygame.draw.line(self.display, color, (x0, y0), (x1, y1))

    def draw_circle(self, x, y, radius, color=Color['white']):
        """@brief Draw a circle given the top left corner of a surrounding square."""
        pygame.draw.circle(self.display, color, (x, y), radius)

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color=Color['white']):
        """@brief Draw triangle border lines."""
        self.draw_line(x0, y0, x1, y1, color)
        self.draw_line(x1, y1, x2, y2, color)
        self.draw_line(x2, y2, x0, y0, color)
