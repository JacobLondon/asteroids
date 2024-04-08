# Pyngine
Python 3 library utilizing Pygame for visualizations, guis, and games.

## GUI
Built into Pyngine, the following components allow for easy component implementation.
- panels, labels
- textboxes, imageboxes, listboxes
- buttons, progress bars
- custom layouts for scaling screen sizes
- simple z-index placement of components

## Conveniences
- Define grids for relative component placement
- Draw with the painter by binding a function to an automatic (or explicit) z-index
- Measure real frame time
- Built in colors
- Built in first-person mouse mode
- Define key and mouse events in a single line

## Dependencies
See requirements.txt
- pygame
- numpy

# Examples
See the `~/examples` directory
## Lables and Buttons
![Labels and Buttons](/images/labels_buttons.png)

## Textboxes
![Textboxes](/images/textboxes.png)

## Hot Keys
![Hot Keys](/images/hot_keys.png)

## Related Projects
[Pyngine First Person Maze](https://github.com/JacobLondon/first)

[Pyngine Rasterizer](https://github.com/JacobLondon/rasterization)

[Pyngine  Connect Four](https://github.com/JacobLondon/ConnectFour)

# Documentation
## Controller Class
Below are the contents of the `Controller` class and how to use them.
- `self`
  - `painter`
    - The painter object owned by the Controller (see painter).
  - `delta_time`
    - The length of time the previoius frame just took in seconds.
  - `fps`
    - The current amount of frames per second the program is achieving.
  - `keyboard`
    - The keyboard object owned by the Controller (see keyboard).
  - `mouse`
    - The mouse object owned by the Controller (see mouse).
  - `background_panel`
    - The panel object representing the component as z index 0 (see panel)
  - `screen_grid`
    - The Controller's grid layout set to `self.grid` (see layout).
  - `screen_relative`
    - The Controller's relative layout set to the `background_panel` (see layout).
- `self (inherited from Interface)`
  - `resolution`
    - Resolution of the display in pixels as a tuple `(w, h)`
  - `screen_width`
    - Number of pixels width the display is.
  - `screen_height`
    - Number of pixels high the display is.
  - `aspect_ratio`
    - The ratio of the screen width by the screen height.
  - `grid_width`
    - The number of grids wide the display can reference.
  - `grid_height`
    - The number grids high that can be referenced
  - `px`
    - The pixel width of each grid.
  - `py`
    - The pixel height of each grid.
  - `center`
    - The center of the display as a tuple `(x, y)`
  - `screen_rect`
    - A list representing the display `[x, y, width, height]`
  - `refresh_rate`
    - The target frame rate to run the display at.
  - `frame_time`
    - The time each frame should take.
  - `display`
    - The Pygame display object.
- `self.painter`
  - `fill_grid(self, gx, gy, color=Color['white'])`
    - Fill a rectangle based on the Controller's `self.grid` parameters.
  - `fill_rect(self, x, y, width, height, color=Color['white'])`
    - Fill a rectangle given the top left corner and the width and height.
  - `fill_triangle(self, x0, y0, x1, y1, x2, y2, color=Color['white'])`
    - Fill a triangle given each corner.
  - `draw_line(self, x0, y0, x1, y1, color=Color['white'])`
    - Draw a line between the given coordinates.
  - `draw_circle(self, x, y, radius, color=Color['white'])`
    - Draw a circle given the coordinate and the radius.
  - `draw_triangle(self, x0, y0, x1, y1, x2, y2, color=Color['white'])`
    - Draw a triangle outline given each corner.
- `self.keyboard`
  - `presses`
    - A dictionary of pygame keys (ie. `pg.K_LSHIFT`) mapped to whether they are pressed or not.
    - For example, `if self.keyboard.presses[pg.K_LSHIFT]: ...`
- `self.mouse`
  - `x` or `y`
    - The current x or y position of the mouse.
  - `presses`
    - A dictionary of static mouse constants mapped to whether they are pressed or not
    - Static attributes
      - `Mouse.l_click`, `Mouse.m_click`, `Mouse.r_click`, `Mouse.scroll_u`, `Mouse.scroll_d`
    - For example, `if self.mouse.presses[Mouse.l_click]: ...`
  - First person view controls
    - `dx` or `dy`
      - How much the mouse moved last frame.
    - `yaw`
      - The rotation on the horizontal plane.
    - `pitch`
      - The rotation on the vertical plane
    - `sensitivity`
      - The factor to scale mouse rotation to.
    - `unit_step`
      - The smallest size which the mouse can move in any direction.
    - `smoothing`
      - Slowly decelerate the mouse after a rotation has finished.
    - `cutoff`
      - The point at which the `smoothing` will stop decelerating and just stop
  - `set_visible(self, visible=True)`
    - Specify whether the mouse is visible or invisible.
  - `toggle_visibility(self)`
    - Switch the mouse's visibility to the other option.
  - `fix_mouse(self)`
    - Freeze the mouse in the center of the screen
## Objects to create in a Controller
- Event
  - `Event(controller, action=None, args=(), keys=())`
  - `halt(self)`
    - Forcibly stop the input from being read (keys are read constantly, calling halt in the action will set key presses to False)
  - Bind keys or key combinations to a function call.
  - For example, `Event(self, action=walk_forward, args=(step_size), keys=(pg.K_w))`
  - Pass a reference to self into the Event
  - Bind a function and pass arguments to that function.
  - Bind 1 or many keys to that Event.
- Drawer
  - `Drawer(self, controller, refresh=None, load=None, z=0)`
  - Pass a reference to self into the Drawer
  - Bind a function to refresh, this occurs every frame.
  - Bind a function to load, this occurs when the program initializes.
  - Specify a z index (automatically managed if ignored) to draw at
  - Drawers are meant to be able to split draw functions up into small z-index cognizant functions
- Components
  - See `~/examples`
  - To do
## Global Objects
- Pygame imported as `pg`
- `Controller`
  - Meant to be extended for custom functionality.
- `Color`
  - See [source](https://www.webucator.com/blog/2015/03/python-color-constants-module/)
