import pygame

class Font(object):
    """@brief Hold a set of fonts and allow for user defined fonts.
    """

    def __init__(self, font, scale):

        pygame.font.init()

        # details about the font created
        self.name = font
        # scale is the ratio of screen width / number of grids wide the screen is
        self.scale = scale

        # make a set of font point sizes for built in components to use
        self.set = {}
        # default fonts
        self.set['small'] = self.named_font(10)
        self.set['standard'] = self.named_font(20)
        self.set['large'] = self.named_font(40)

    def __setitem__(self, key, val):
        """@brief Add user defined fonts.
        """
        self.set[key] = val

    def __getitem__(self, key):
        """@brief Get set fonts.
        """
        return self.set[key]

    def named_font(self, point):
        """@brief Create a font from the specified name.
        """
        return Font.create(self.name, point * self.scale)

    @staticmethod
    def create(font_name, point):
        """@brief Simplify creating a font.
        """
        return pygame.font.SysFont(font_name, int(point))
