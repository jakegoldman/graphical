# Graphics Final Project

By Jake Goldman
Stuyvesant Computer Graphics Pd 10

## How to use
A demo of key features implemented has been set up using an MDL script and an object
file. To view this demo, run `make` from the command line and view the .gif file that
gets generated. For more generic instructions, see below.

1) Make sure you have both python 2 and ImageMagick installed
2) Clone the repo
3) Create an appropriate MDL file and place it in the `scripts` directory. Any
relevant object files must be placed in the `obj` directory.
4) Run your MDL file through the command `python main.py _filename_`
5) If you're generating an animation, you can run your .gif file through the command
line with `animate _filename_`

## New Features
#### Polygon Meshes
Support for polygon meshes has been implemented in the form of object files using
the [.obj file format](https://en.wikipedia.org/wiki/Wavefront_.obj_file). To use this
feature, create an appropriate polygon mesh and add it to the `obj` directory. Then
use the MDL command `mesh [constants] :_filename_` to add your image to the screen. At the moment, only
meshes with three vertices per face are supported, but quadrilateral support is likely to
be implemented very soon.

#### Lighting
The following lighting commands have been implemented:
* `ambient _r_ _g_ _b_` : sets ambient lighting for the image
* `light _name_ _r_ _g_ _b_ _x_ _y_ _z_` : sets a new point light source at the specified location with the specified color values
* `constants _name_ _ar_ _dr_ _sr_ _ag_ _dg_ _sg_ _ab_ _db_ _sb_` : saves a group of lighting constants in the symbol table
