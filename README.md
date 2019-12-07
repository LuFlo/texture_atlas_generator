# Texture Atlas Generator

This is a litte tool which helps creating a texture atlas if you have a flat
shaded multi-material object in Blender. Currently the add-on is only working
for Blender 2.80 and 2.81, because it looks for the "Principled BSDF" node in
order to determine the color of the texture tile.

![Generating Texture Atlas](doc/images/overview_demo.png?raw=true "Generating Texture Atlas")


## Installation

1. Download the latest release: [https://github.com/LuFlo/texture_atlas_generator/releases](https://github.com/LuFlo/texture_atlas_generator/releases)
2. Open Blender, go to Edit > Preferences > Add-ons
3. Click the "Install..." button in the top right corner
4. Choose the .zip file you have downloaded beforehand
5. Check the checkbox in order to enable the add-on. Don't forget to save your preferences.


## Quick introduction

After installation you should find a new panel in the Properties > Material Tab.
Select an object with multiple materials assigned.

Be sure to unwrap your object before using the tool. After you select the
object, you can change the image size and tile size settings. It is usually a
good idea to choose powers of 2 for the image and tile sizes. It is also recommended
to have square images / tiles.

![Plugin Settings](doc/images/intro1.png?raw=true "Plugin Settings")

Click "Generate Texture Atlas". You will find a new image in the image list on
the UV editor. Now you can save or export the image to your favorite
game engine :)


## Limitations

### Multi-Texture-Objects are not supported

This tool currently works with single color materials (it uses the color channel of
the Principled BSDF shader). You have to go through Blender's internal bake process
if you want to use multi texture objects.


## Issues and help

If you encounter any issues or bugs, please open an issue on [GitHub](https://github.com/LuFlo/texture_atlas_generator/issues)

Also feel free to suggests new ideas or open a pull-request if you are a coder :)