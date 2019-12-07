# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

from collections import namedtuple
from typing import Tuple

from .gltf2_io_color_management import color_linear_to_srgb

try:
    import bpy
    from mathutils import Vector
except ImportError:
    from tests.helper_classes import Vector

TileInfo = namedtuple('TileInfo', 'x1 y1 x2 y2 color')


def create_tile_infos(width, height, num_tiles, tile_size: Tuple[int, int], colors):
    tile_width, tile_height = tile_size
    x_tiles = int(width / tile_width)
    y_tiles = int(height / tile_height)
    if x_tiles * y_tiles < num_tiles:
        raise ValueError(
            f"Insufficient image dimensions for {num_tiles} tiles. "
            + f"The current image size only fits {x_tiles * y_tiles} tiles.")
    infos = []
    i_colors = iter(colors)
    for y_pos in range(y_tiles):
        for x_pos in range(x_tiles):
            try:
                infos.append(TileInfo(
                    x_pos * tile_width,
                    y_pos * tile_height,
                    x_pos * tile_width + tile_width - 1,
                    y_pos * tile_height + tile_height - 1,
                    next(i_colors)
                ))
            except StopIteration:
                break
    return infos


def paint_patch(tile_infos: list = None,
                pixels: list = None,
                width: int = 0,
                use_srbg: bool = True) -> list:
    if width == 0:
        raise ValueError("width can't be 0")
    out = [pixels[i] for i in range(len(pixels))]
    for info in tile_infos:
        for y in range(info.y1, info.y2 + 1):
            for x in range(info.x1, info.x2 + 1):
                offset = (x + y * width) * 4
                for i, c in enumerate(info.color):
                    if use_srbg:
                        out[offset + i] = color_linear_to_srgb(c)
                    else:
                        out[offset + i] = c
    return out


def translate_uvs(tile_info: TileInfo, uvs=None, margin=5.0):
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


def generate_texture_atlas(image_size: Tuple[int, int],
                           tile_size: Tuple[int, int],
                           image_name: str,
                           use_srbg: bool):
    bpy.ops.object.mode_set(mode="OBJECT")

    obj = bpy.context.active_object
    in_width, in_height = image_size
    if image_name in bpy.data.images:
        _image = bpy.data.images[image_name]
        bpy.data.images.remove(_image)
    bpy.ops.image.new(name=image_name, width=in_width, height=in_height)
    image = bpy.data.images[image_name]
    image.generated_width = in_width
    image.generated_height = in_height
    width = image.size[0]
    height = image.size[1]

    colors = []
    color_face_map = {}
    for face in obj.data.polygons:
        mat_index = face.material_index
        mat = obj.material_slots[mat_index].material
        color = mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value
        if color not in colors:
            colors.append(color)
        if color not in color_face_map:
            color_face_map[color] = []
        color_face_map[color].append(face)
    tile_infos = create_tile_infos(width, height, len(colors), tile_size, colors)

    print(list(color_face_map.keys()))

    for color, faces in color_face_map.items():
        uvs = []
        for face in faces:
            for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                uvs.append(obj.data.uv_layers.active.data[loop_idx].uv)
        uvs = translate_uvs(tile_infos[colors.index(color)], uvs)
        print(color, len(uvs))
        # Normalize
        i_uvs = (Vector((v.x / width, v.y / height)) for v in uvs)
        for face in faces:
            for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                obj.data.uv_layers.active.data[loop_idx].uv = next(i_uvs)

    pixels = [0.0 for i in range(len(image.pixels))]
    pixels = paint_patch(tile_infos, pixels, width, use_srbg)

    image.pixels = pixels

    bpy.ops.object.mode_set(mode="EDIT")
