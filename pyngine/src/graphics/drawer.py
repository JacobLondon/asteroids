
class Drawer(object):
    """@brief Acts as a component, but with custom functions that are
    defined within the controller and passed into refresh/load.

    This allows for z index loading which may have
    complex drawing functionality.
    """

    def __init__(self, controller, refresh=None, load=None, z=0):
        controller._add_component(self, z)

        if refresh is not None:
            self.refresh = refresh
        if load is not None:
            self.load = load

    def __str__(self):
        return 'Drawer'

    def load(self):
        pass

    def refresh(self):
        pass