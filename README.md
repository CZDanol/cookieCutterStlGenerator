# Danol's SVG -> Cookie Cutter STL Generator

## How it works
* Takes in SVG/DWF files (even in batch)
  * Best to set the SVG to strokes only.
  * It can contain multiple paths.
* Spits out OpenSCAD files
* If you specify OpenSCAD filepath, it can automatically generate STL files
* The OpenSCAD generation is quite slow because it's using minkowski sum. Well, OpenSCAD sucks :/ But at least I've made it when processing multiple svgs.

## Settings
Settings can be specified in multiple ways (ordered by priority)
1. File names. File name is split by `_` and then every item is scanned against settings list (for example `cook1_h=10.svg`)
1. Command line arguments to the script.
1. INI file in the directory of the svg.
   * Default ini location: "config.ini" in the working folder.
   * Can set all values from "help", they must be in the `[DEFAULT]` section.

### Available settings
```
Usage:
        cookie2stl (options) (files or dirs)

Options:
--baseWidth=4
        (mm) Width of the base

--baseHeight=1
        (mm) Height of the base

--cutterWidth=0.5
        (mm) Width of the cutter extrusion

--cutterHeight=10
        (mm) Height of the cutter extrusioon (including wedge)

--cutterWedgeHeight=1
        (mm) Height of the wedge of the cutter extrusion. The larger this number, the sharper the cutter.

--mesh=0
        If set to 1, a support mesh is generated (needed for multi-path cutters)

--meshDistance=10
        (mm) Distance of mesh grills

--meshWidth=1
        (mm) Width of mesh grills

--meshArea=400
        (mm) Area where the mesh is generated (+-)

--watermark=1
        If set to 1, a watermark is added on the cutter

--watermarkText=DANOL
        Text of the watermark

--openscadLocation=None
        Location of the scad exe file

--genStl=0
        Will automatically generate STL files if set to 1. openscadLocation needs to be set
```

## Requirements
* Python
* OpenSCAD