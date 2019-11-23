bl_info = {
    "name": "Texture Atlas Generator",
    "author": "Lukas Florea",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Material",
    "description": "Generates a Texture Atlas from multi-material object",
    "warning": "",
    "wiki_url": "https://github.com/LuFlo/texture_atlas_generator/wiki",
    "tracker_url": "https://github.com/LuFlo/texture_atlas_generator/issues/new",
    "category": "Material"
}

from . import util

import bpy

from bpy.props import IntProperty
from bpy.props import StringProperty


class PerformGeneration(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.generate_texture_atlas"
    bl_label = "Generate Texture Atlas"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None

    def execute(self, context):
        scene = context.scene
        try:
            util.generate_texture_atlas((scene.tag_image_width, scene.tag_image_height),
                                        (scene.tag_tile_width, scene.tag_tile_height),
                                        scene.tag_image_name)
        except ValueError as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}


class PropsPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Texture atlas generator"
    bl_idname = "OBJECT_PT_props_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Settings", icon='PLUGIN')

        row = layout.row()

        col = row.column()
        col.label(text='Image name')
        col = row.column()
        col.prop(context.scene, "tag_image_name")

        row = layout.row()

        col = row.column()
        col.label(text='Image width')
        col = row.column()
        col.prop(context.scene, "tag_image_width")

        row = layout.row()

        col = row.column()
        col.label(text='Image height')
        col = row.column()
        col.prop(context.scene, "tag_image_height")

        row = layout.row()

        col = row.column()
        col.label(text='Tile width')
        col = row.column()
        col.prop(context.scene, "tag_tile_width")

        row = layout.row()

        col = row.column()
        col.label(text='Tile height')
        col = row.column()
        col.prop(context.scene, "tag_tile_height")

        row = layout.row()
        row = layout.row()
        row.operator("object.generate_texture_atlas")


def register():
    bpy.utils.register_class(PropsPanel)
    bpy.utils.register_class(PerformGeneration)
    bpy.types.Scene.tag_image_width = IntProperty(
            attr="tag_image_width",
            name="",
            default=512, min=64, max=4096,
            description="Width of texture atlas image"
        )
    bpy.types.Scene.tag_image_height = IntProperty(
        attr="tag_image_height",
        name="",
        default=512, min=64, max=4096,
        description="Height of texture atlas image"
    )
    bpy.types.Scene.tag_tile_width = IntProperty(
            attr="tag_tile_width",
            name="",
            default=64, min=8, max=512,
            description="Width of color tiles"
        )
    bpy.types.Scene.tag_tile_height = IntProperty(
            attr="tag_tile_height",
            name="",
            default=64, min=8, max=512,
            description="Height of color tiles"
        )
    bpy.types.Scene.tag_image_name = StringProperty(
            attr="tag_image_name",
            name="",
            default="texture_atlas",
            description="Name of the texture atlas image in the UV editor"
        )


def unregister():
    bpy.utils.unregister_class(PropsPanel)
    bpy.utils.unregister_class(PerformGeneration)


if __name__ == "__main__":
    register()
