import datetime, math, os, time
from pyglet.gl import *
from pyglet.window import mouse
import pyglet.window.key as key

# screenshot manager parameters
screenshot_directory = 'screenshots/'
screenshot_file_type = '.png'

# control parameters
zoom_enabled = True
zoom_min = 4
zoom_max = 128
zoom_init = 16
zoom_speed = 1 / 50

translation_enabled = True
translation_init = (0, 0)

# presentation parameters
window_width = 800
window_height = 600
window_resizable = True  # set to False to force resolution even if window does not fit on screen
show_grid = True
rotate_thirty_degree = False  # the grid is not drawn correctly if the view is rotated!

# rendering parameters
target_frame_rate = 10
busy_waiting_time = 1
print_frame_stats = False

# simulation parameters
rounds_per_second = 1

# tile_alpha = 0.6
particle_alpha = 1

marker_alpha = 1


def coords_to_sim(coords):
    return coords[0], coords[1] * math.sqrt(3/4)


def sim_to_coords(x, y):
    return x, round(y / math.sqrt(3/4), 0)


def window_to_sim(x, y, view):
    x_coord = view.left + (view.right - view.left) * (x / view.width)  # correct
    y_coord = view.bottom + (view.top - view.bottom) * (y / view.height)  # not correct
    return x_coord, y_coord


class ScreenshotManager:
    dt = datetime.datetime.now()
    #prefix = dt.isoformat(sep = '_', timespec = 'seconds').replace(':', '') + '_'
    prefix = dt.isoformat(sep='_').replace(':', '') + '_'

    def takeScreenshot():
        if not os.path.exists(screenshot_directory):
            os.makedirs(screenshot_directory)

        index = math.floor(time.monotonic() * 10**3)
        file_name = screenshot_directory + ScreenshotManager.prefix + str(index) + screenshot_file_type
        pyglet.image.get_buffer_manager().get_color_buffer().save(file_name)


class View:
    def __init__(self):
        self.focusPos = translation_init
        self.zoom = zoom_init
        halfZoomRec = 0.5 / self.zoom

    def setDimensions(self, width, height):
        self.width = width
        self.height = height
        self.update()

    def drag(self, dx, dy):
        if not translation_enabled:
            return

        self.focusPos = (self.focusPos[0] - dx / self.zoom, self.focusPos[1] - dy / self.zoom)
        self.update()

    def scroll(self, x, y, scroll_x, scroll_y):
        if not zoom_enabled:
            return

        oldPos = (self.left + x / self.zoom, self.bottom + y / self.zoom)
        self.zoom = self.zoom * math.exp(-scroll_y * zoom_speed)
        self.zoom = max(self.zoom, zoom_min)
        self.zoom = min(self.zoom, zoom_max)
        self.update()
        newPos = (self.left + x / self.zoom, self.bottom + y / self.zoom)
        self.focusPos = (self.focusPos[0] + oldPos[0] - newPos[0], self.focusPos[1] + oldPos[1] - newPos[1])
        self.update()

    def update(self):
        halfZoomRec = 0.5 / self.zoom
        self.left = self.focusPos[0] - halfZoomRec * self.width;
        self.right = self.focusPos[0] + halfZoomRec * self.width;
        self.bottom = self.focusPos[1] - halfZoomRec * self.height;
        self.top = self.focusPos[1] + halfZoomRec * self.height;


class VisWindow(pyglet.window.Window):
    def __init__(self, window_size_x, window_size_y, world):
        #super().__init__(world.get_sim_x_size(), world.get_sim_y_size(), resizable=window_resizable, vsync=False, caption="Simulator")
        super().__init__(window_size_x, window_size_y , resizable=window_resizable, vsync=False, caption="Simulator")
        self.window_active = True
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.world = world
        self.init_tile_vertex_list()
        self.init_particle_vertex_list()
        self.init_marker_vertex_list()
        self.view = View()
        self.view.setDimensions(window_size_x, window_size_y)
        self.elapsed_frame_time = 0
        self.particleTexture = pyglet.image.load('lib/images/particle.png').get_mipmapped_texture()
        self.gridTexture = pyglet.image.load('lib/images/grid.png').get_mipmapped_texture()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(self.gridTexture.target)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if rotate_thirty_degree:
            glRotatef(30, 0, 0, 1)

        glMatrixMode(GL_PROJECTION)

        self.simulation_running = False
        self.video_mode = False
        self.draw()


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.view.drag(dx, dy)

    def exit_callback(self):
        self.close()
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.view.scroll(x, y, scroll_x, scroll_y)

    def on_mouse_press(self, x, y, button, modifiers):
        if modifiers & key.MOD_CTRL:
            # get correct coordinates
            sim_coords = window_to_sim(x, y, self.view)
            coords_coords = sim_to_coords(sim_coords[0], sim_coords[1])
            rounded_coords=0
            if coords_coords[1]%2!=0:
                rounded_coords = round(coords_coords[0],0) + 0.5
            else:
                rounded_coords =round(coords_coords[0], 0)
            if (rounded_coords,coords_coords[1]) not in self.world.tile_map_coords:
                # add tile and vertices
                if self.world.add_tile_vis(rounded_coords, coords_coords[1]):
                    self.tile_vertex_list.resize(4 * len(self.world.tiles), 4 * len(self.world.tiles))
                    #self.tile_vertex_list.resize(4 * len(self.world.tiles), 8 * len(self.world.tiles))
                    self.tile_vertex_list.indices[4 * (len(self.world.tiles) - 1) : 4 * (len(self.world.tiles) - 1) + 4] = range(4 * (len(self.world.tiles) - 1), 4 * (len(self.world.tiles) - 1) + 4)
                   # self.tile_vertex_list.indices = list(range(0, 8 * len(self.world.tiles)))
                   # self.update_tile(len(self.world.tiles) - 1, tile)
                    self.update_tiles(True)
            else:
                # delete tile
                self.world.remove_tile_on((rounded_coords,coords_coords[1]))
                self.tile_vertex_list.resize(4 * len(self.world.tiles), 4 * len(self.world.tiles))
                self.update_tiles(True)

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        self.view.setDimensions(width, height)
        return pyglet.event.EVENT_HANDLED

    def on_close(self):
        self.window_active = False
        return pyglet.event.EVENT_HANDLED

    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q and modifiers & key.MOD_COMMAND:  # cmd+q: quit application
            self.window_active = False
        elif symbol == key.SPACE:  # space: pause / unpause simulation
            self.pause()
        elif symbol == key.S and modifiers & key.MOD_COMMAND:  # cmd+s: save screenshot
            ScreenshotManager.takeScreenshot()
        elif symbol == key.V and modifiers & key.MOD_COMMAND:  # cmd+v: toggle video mode
            if not self.video_mode:
                self.video_mode = True
                self.simulation_running = True
                self.elapsed_frame_time = 0  # make videos completely reproducible
            else:
                self.video_mode = False
                self.simulation_running = False
        return pyglet.event.EVENT_HANDLED

    def draw(self):
        self.update_tiles()
        self.update_particles()
        self.update_markers()
        glLoadIdentity()
        glOrtho(self.view.left, self.view.right, self.view.bottom, self.view.top, 1, -1)


        if show_grid:
            self.drawGrid()
        else:
            glClearColor(1, 1, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT)

        glBindTexture(self.particleTexture.target, self.particleTexture.id)

        if len(self.world.tiles) != 0:
            self.tile_vertex_list.draw(GL_QUADS)
        self.particle_vertex_list.draw(GL_QUADS)
        self.marker_vertex_list.draw(GL_QUADS)

        self.flip()

        if self.video_mode:
            ScreenshotManager.takeScreenshot()

    def drawGrid(self):
        texLeft = math.fmod(self.view.left, 1)
        texRight = texLeft + self.view.right - self.view.left

        texHeight = 2 * math.sqrt(3/4)
        texBottom = math.fmod(self.view.bottom, texHeight)
        texTop = texBottom + self.view.top - self.view.bottom
        texBottom = texBottom / texHeight
        texTop = texTop / texHeight

        glColor4f(1, 1, 1, 1)
        glBindTexture(self.gridTexture.target, self.gridTexture.id)

        glBegin(GL_QUADS)
        glTexCoord2f(texLeft, texBottom)
        glVertex2f(self.view.left, self.view.bottom)
        glTexCoord2f(texRight, texBottom)
        glVertex2f(self.view.right, self.view.bottom)
        glTexCoord2f(texRight, texTop)
        glVertex2f(self.view.right, self.view.top)
        glTexCoord2f(texLeft, texTop)
        glVertex2f(self.view.left, self.view.top)
        glEnd()

    def pause(self):
        self.simulation_running = not self.simulation_running

    def round(self):
        if self.world.run_sim():
            return True

    def init_tile_vertex_list(self):
        self.tile_vertex_list = pyglet.graphics.vertex_list_indexed(4 * len(self.world.tiles),
                                                                    list(range(0, 4 * len(self.world.tiles))),
                                                                    #list(range(0,8 * len(self.world.tiles))),
                                                                    'v2f', 't2f', 'c4f')
        self.update_tiles(True)


    def update_tiles(self, update_all=False):
        foreground = []
        background = []

        if (len(self.world.tiles) != 0):
            if self.world.get_tile_deleted():
                self.tile_vertex_list.resize(4 * len(self.world.tiles), 4 * len(self.world.tiles))
                update_all=True
                self.world.set_tile_deleted()
            for i, tile in enumerate(self.world.tiles):
                if tile.created:
                    self.tile_vertex_list.resize(4 * len(self.world.tiles), 4 * len(self.world.tiles))
                    self.tile_vertex_list.indices[
                    4 * (len(self.world.tiles) - 1): 4 * (len(self.world.tiles) - 1) + 4] = range(
                        4 * (len(self.world.tiles) - 1), 4 * (len(self.world.tiles) - 1) + 4)
                    tile.created =  False
                if update_all or tile.modified:
                    self.update_tile(i, tile)
                    tile.modified = False

                indices = list(range(4 * i, 4 * i + 4))
                if tile.get_tile_status():
                    foreground += indices
                else:
                    background += indices

            self.tile_vertex_list.indices = background + foreground
        else:
            pass#self.tile_vertex_list.indices = list(range(0,4))

    def update_tile(self, i, tile):
        weird = 256 / 220
        pos = coords_to_sim(tile.coords)
        x = pos[0]
        y = pos[1]

        self.tile_vertex_list.vertices[8 * i: 8 * i + 8] = [x - weird, y - weird, x + weird, y - weird, x + weird,
                                                            y + weird, x - weird, y + weird]

        if tile.get_tile_status():
            texLeft = 0 / 8
            texRight = 1 / 8
            texBottom = 5 / 8
            texTop = 6 / 8
            #tile_alpha = 1
        else:
            texLeft = 7 / 8
            texRight = 1 # 8/8
            texBottom = 4 / 8
            texTop = 5 / 8
            #tile_alpha = 0.5

        self.tile_vertex_list.tex_coords[8 * i: 8 * i + 8] = [texLeft, texBottom, texRight, texBottom, texRight, texTop,
                                                              texLeft, texTop]

        self.tile_vertex_list.colors[16 * i: 16 * i + 16] = (tile.color + [tile.get_alpha()]) * 4

    def init_particle_vertex_list(self):
        self.particle_vertex_list = self.particle_vertex_list = pyglet.graphics.vertex_list \
            (4 * len(self.world.particles), 'v2f', 't2f', 'c4f')
        self.update_particles(True)

    def update_particles(self, update_all = False):
        if (len(self.world.particles) != 0):
            if self.world.get_particle_deleted():
                self.particle_vertex_list.resize(4 * len(self.world.particles))
                self.world.set_particle_deleted()
                update_all = True
            for i, particle in enumerate(self.world.particles):
                if particle.created:
                    self.particle_vertex_list.resize(4 * len(self.world.particles))
                    # self.tile_vertex_list.resize(4 * len(self.world.tiles), 8 * len(self.world.tiles))
                    particle.created=False
                if update_all or particle.modified:
                    self.update_particle(i, particle)
                    particle.modified = False
        else:
            pass


    def update_particle(self, i, particle):
        weird = 256 / 220
        pos = coords_to_sim(particle.coords)
        x = pos[0]
        y = pos[1]

        self.particle_vertex_list.vertices[8 * i: 8 * i + 8] = [x - weird, y - weird, x + weird, y - weird, x + weird,
                                                                y + weird, x - weird, y + weird]
        """UV works in such away that there are 8 Columns and 8 rows and if you want to take one you have to add the direction
        and reduce one from the inverse direction"""
        if particle.get_carried_status():
            texLeft = 0 / 8
            texRight = 1 / 8
            texBottom = 7 / 8
            texTop = 6 / 8
            #particle.set_alpha(0.5)
        else:
            texLeft = 0 / 8
            texRight = 1 / 8
            texBottom = 0 / 8
            texTop = 1 / 8
            #particle.set_alpha(1)
        self.particle_vertex_list.tex_coords[8 * i: 8 * i + 8] = [texLeft, texBottom, texRight, texBottom,
                                                                  texRight, texTop, texLeft, texTop]

        self.particle_vertex_list.colors[16 * i: 16 * i + 16] = (particle.color + [particle.get_alpha()]) * 4

    def init_marker_vertex_list(self):
        self.marker_vertex_list = self.marker_vertex_list = pyglet.graphics.vertex_list \
            (4 * len(self.world.markers), 'v2f', 't2f', 'c4f')
        self.update_markers(True)

    def update_markers(self, update_all=True):
        if (len(self.world.markers) != 0):
            if self.world.get_marker_deleted():
                self.marker_vertex_list.resize(4 * len(self.world.markers))
                self.world.set_marker_deleted()
                update_all = True
            for i, marker in enumerate(self.world.markers):
                if marker.created:
                    self.marker_vertex_list.resize(4 * len(self.world.markers))
                    # self.tile_vertex_list.resize(4 * len(self.world.tiles), 8 * len(self.world.tiles))
                    marker.created = False
                if update_all or marker.modified:
                    self.update_marker(i, marker)
                    marker.modified = False
        else:
            pass


    def update_marker(self, i, marker):
        weird = 256 / 220
        pos = coords_to_sim(marker.coords)
        x = pos[0]
        y = pos[1]

        self.marker_vertex_list.vertices[8 * i: 8 * i + 8] = [x - weird, y - weird, x + weird, y - weird, x + weird,
                                                                y + weird, x - weird, y + weird]
        texLeft = 7/8
        texRight = 1 #8/8
        texBottom = 0/8
        texTop = 1/8

        self.marker_vertex_list.tex_coords[8 * i: 8 * i + 8] = [texLeft, texBottom, texRight, texBottom,
                                                                  texRight, texTop, texLeft, texTop]

        self.marker_vertex_list.colors[16 * i: 16 * i + 16] = (marker.color + [marker.get_alpha()]) * 4

    def draw_world(self):
        while not self.simulation_running:
            self.dispatch_events()
            if self.simulation_running or self.window_active is False:
                return
        self.dispatch_events()
        #while actual simulation round is below max round
        time.sleep(1/rounds_per_second)
        self.draw()
        return

    def finished(self):
        self.window_active = False

