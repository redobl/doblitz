import os
import itertools

from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle
from kivy.logger import Logger
from kivy.properties import ListProperty
from kivy.uix.widget import Widget

import pytmx


class KivyTiledMap(pytmx.TiledMap):
    """
    Loads Kivy images. Make sure that there is an active OpenGL context
    (Kivy Window) before trying to load a map.
    """

    def __init__(self, map_file_path=None, *args, **kwargs):
        assert map_file_path, 'No map file provided, please provide the path to a .tmx file.'
        super(KivyTiledMap, self).__init__(map_file_path, *args, **kwargs)

        # pull out the directory containing the map file path
        self.map_dir: str = os.path.dirname(map_file_path)
        Logger.debug('KivyTiledMap: directory containing map file: "{}"'.format(self.map_dir))

        for ind, tile_image in enumerate(self.images):
            if tile_image is None: continue
            self.images[ind] = CoreImage(tile_image[0]).texture

    def find_tiles_with_property(self, property_name, layer_name='Meta'):
        tiles = []
        layer = self.get_layer_by_name(layer_name)
        index = self.layers.index(layer)
        for tile in layer:
            properties = self.get_tile_properties(tile[0], tile[1], index)
            if properties and property_name in properties:
                tiles.append((tile[0], tile[1]))

        return tiles

    def tile_has_property(self, x, y, property_name, layer_name='Meta'):
        """Check if the tile coordinates passed in represent a collision.
        :return: Boolean representing whether or not there was a collision.
        :rtype: bool
        """
        layer = self.get_layer_by_name(layer_name)
        layer_index = self.layers.index(layer)

        properties = self.get_tile_properties(x, y, layer_index)

        # if there are properties to look at, check whether the name is in them
        return property_name in properties if properties else False

    def valid_move(self, x, y, debug=False):
        # check if the tile is out of bounds
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            if debug:
                Logger.debug('KivyTiledMap: Move {},{} is out of bounds'.format(x, y))
            return False

        # check if the tile has the property 'Collidable'
        if self.tile_has_property(x, y, 'Collidable'):
            if debug:
                Logger.debug('KivyTiledMap: Move {},{} collides with map object'.format(x, y))
            return False

        return True

    def get_adjacent_tiles(self, x, y):
        """Get the tiles surrounding the north, south, east and west of x,y.
        :return: A list of coordinate tuples adjacent to x,y.
        :rtype: list
        """
        adjacent_tiles = []

        # try each direction and add to the list if they are valid_moves
        # up
        if self.valid_move(x, y - 1):
            adjacent_tiles.append((x, y - 1))

        # down
        if self.valid_move(x, y + 1):
            adjacent_tiles.append((x, y + 1))

        # left
        if self.valid_move(x - 1, y):
            adjacent_tiles.append((x - 1, y))

        # right
        if self.valid_move(x + 1, y):
            adjacent_tiles.append((x + 1, y))

        return adjacent_tiles


class TileMap(Widget):
    """Creates a Kivy grid and puts the tiles in a KivyTiledMap in it."""
    scaled_tile_size = ListProperty()

    def __init__(self, map_file_path=None, **kwargs):
        assert map_file_path, 'No map file path provided to TileMap. Please pass in a path to a .tmx file.q'
        self.tiled_map = KivyTiledMap(map_file_path)
        super(TileMap, self).__init__(**kwargs)

        self._scale = 1.0
        self.tile_map_size = (self.tiled_map.width, self.tiled_map.height)
        self.tile_size = (self.tiled_map.tilewidth, self.tiled_map.tileheight)
        self.scaled_tile_size = self.tile_size
        self.scaled_map_width = self.scaled_tile_size[0] * self.tile_map_size[0]
        self.scaled_map_height = self.scaled_tile_size[1] * self.tile_map_size[1]

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.scaled_tile_size = (self.tile_size[0] * self._scale, self.tile_size[1] * self._scale)
        self.scaled_map_width = self.scaled_tile_size[0] * self.tile_map_size[0]
        self.scaled_map_height = self.scaled_tile_size[1] * self.tile_map_size[1]
        self.on_size()

    def on_size(self, *args):
        Logger.debug('TileMap: Re-drawing')

        screen_tile_size = self.get_root_window().width / 32
        self.scaled_tile_size = (screen_tile_size, screen_tile_size)
        self.scaled_map_width = self.scaled_tile_size[0] * self.tile_map_size[0]
        self.scaled_map_height = self.scaled_tile_size[1] * self.tile_map_size[1]

        self.canvas.clear()

        with self.canvas:
            layer_idx = 0
            for layer in self.tiled_map.layers:
                if not layer.visible:
                    continue  # skip the layer if it's not visible
                if not isinstance(layer, pytmx.TiledTileLayer):
                    continue
                # set up the opacity of the tiled layer
                Color(1.0, 1.0, 1.0, layer.opacity)

                # iterate through the tiles in the layer
                for tile in layer:
                    tile_x = tile[0]
                    tile_y = tile[1]
                    try:
                        texture = self.tiled_map.get_tile_image(tile_x, tile_y, layer_idx)
                    except AttributeError:
                        continue  # keep going if the texture is empty

                    # calculate the drawing parameters of the tile
                    draw_pos = self._get_tile_pos(tile_x, tile_y)
                    draw_size = self.scaled_tile_size

                    # create a rectangle instruction for the gpu
                    Rectangle(texture=texture, pos=draw_pos, size=draw_size)
                layer_idx += 1

    def _get_tile_pos(self, x, y):
        """Get the tile position relative to the widget."""
        pos_x = x * self.scaled_tile_size[0]
        pos_y = (self.tile_map_size[1] - y - 1) * self.scaled_tile_size[1]
        return pos_x, pos_y

    def get_tile_position(self, x, y):
        """Get the tile position according to the window."""
        return self._get_tile_pos(x, y)

    def get_tile_at_position(self, pos: tuple[float, float]):
        """Find out the tile coordinates of the position.
        :param pos: The screen position to get the tile of.
        :type pos: (float, float)
        :return: The tile position.
        :rtype: (int, int) | None
        """
        # convert the pos to local coords
        pos = self.to_local(*pos)
        Logger.debug('TileMap: Finding tile at position {}'.format(pos))

        found_x = False
        tile_x = 0
        while tile_x < self.tiled_map.width:
            tile_x_right = (tile_x + 1) * self.scaled_tile_size[0]
            if tile_x_right < pos[0]:
                tile_x += 1
            else:
                found_x = True
                break

        # start at the bottom of the map, same as kivy coords
        tile_y = self.tiled_map.height
        while tile_y != 0:
            # calculate how far up from the bottom of the widget the tile is
            tile_y_top = (self.tiled_map.height - tile_y) * self.scaled_tile_size[1]
            if tile_y_top < pos[1]:
                tile_y -= 1
            else:
                if found_x:
                    return tile_x, tile_y
                break

        return None

    def get_tile_name_at_pos(self, x: int, y: int, layer: int = 0):
        return self.tiled_map.get_tile_gid(x, y, layer)

    def get_tile_properties_at_pos(self, x: int, y: int, layer: int = 0):
        try:
            return self.tiled_map.get_tile_properties(x, y, layer)
        except AttributeError:
            print("error getting tile properties")
            return None
        except Exception:
            print("layer is invalid")
            return None
