from math import fabs

from collections import namedtuple

TileInfo = namedtuple('TileInfo', 'x1 y1 x2 y2 color')
class Vector:

    def __init__(self, tpl):
        self.x = tpl[0]
        self.y = tpl[1]


    def __add__(v1, v2):
        return Vector((v1.x + v2.x, v1.y + v2.y))

    def __mul__(v1, s):
        return Vector((v1.x * s, v1.y * s))


def create_tile_infos(width, height, num_tiles, tile_size, colors):
    x_tiles = int(width / tile_size)
    y_tiles = int(height / tile_size)
    if x_tiles * y_tiles < num_tiles:
        raise ValueError(f"Incorrect image dimensions for {num_tiles} tiles")
    infos = []
    i_colors = iter(colors)
    for y_pos in range(y_tiles):
        for x_pos in range(x_tiles):
            try:
                infos.append(TileInfo(
                        x_pos * tile_size,
                        y_pos * tile_size,
                        x_pos * tile_size + tile_size - 1,
                        y_pos * tile_size + tile_size - 1,
                        next(i_colors)
                    ))
            except StopIteration:
                break
    return infos


def paint_patch(
        tile_infos: list = [],
        pixels: list = [],
        width: int = 0) -> list:
    if width == 0:
        raise ValueError("width can't be 0")
    out = [pixels[i] for i in range(len(pixels))]
    for info in tile_infos:
        for y in range(info.y1, info.y2 + 1):
            for x in range(info.x1, info.x2 + 1):
                offset = (x + y * width) * 4
                for i, c in enumerate(info.color):
                    out[offset + i] = c
    return out


def translate_uvs(tile_info: TileInfo, uvs=[], margin=5.0):
    a_uv = uvs[0]

    min_x = min(uvs, key=lambda v: v.x).x
    min_y = min(uvs, key=lambda v: v.y).y
    max_x = max(uvs, key=lambda v: v.x).x
    max_y = max(uvs, key=lambda v: v.y).y
    out_uvs = [Vector((v.x - min_x, v.y - min_y)) for v in uvs]

    width = max_x - min_x
    height = max_y - min_y

    target_width = tile_info.x2 - tile_info.x1 - margin * 2
    target_height = tile_info.y2 - tile_info.y1 - margin * 2

    scale_x = target_width / width
    scale_y = target_height / height

    out_uvs = [Vector((v.x * scale_x, v.y * scale_y)) for v in out_uvs]

    t1 = Vector((tile_info.x1, tile_info.y1))
    margin_v = Vector((margin, margin))
    out_uvs = [v + t1 + margin_v for v in out_uvs]

    return out_uvs
