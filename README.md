# Danol's SVG -> Cookie Cutter STL Generator

## How it works
* Takes in SVG files (even in batch)
  * Works with **STROKES ONLY**. Ignores non-stroked objects.
  * It can contain multiple paths.
  * The input required is quite fiddly. The SVG must contain the file dimensions. It works for me in Affinity Designer when checking "Flatten tranforms" and "Set viewbox" in the "More" menu in export to SVG.
* Spits out OpenSCAD files
* If you specify OpenSCAD filepath, it can automatically generate STL files

## Settings
Settings can be specified in multiple ways (ordered by priority)
1. TODO: File names. File name is split by `_` and then every item is scanned against settings list (for example `cook1_h=10.svg`)
1. Command line arguments to the script.
1. INI file.
   * Default ini location: "config.ini" in the working folder.
   * Can set all values from "help", they must be in the `[DEFAULT]` section.

### Available settings
```
Usage:
	svg2cookie (options) (file1) (file2) (dir1)

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

--meshAlways=0
        If set to 1, a support mesh is always generated

--meshDistance=10
        (mm) Distance of mesh grills

--meshWidth=1
        (mm) Width of mesh grills

--meshArea=400
        (mm) Area where the mesh is generated (+-)

--openscadLocation=None
        Location of the scad exe file

--genStl=0
        Will automatically generate STL files if set to 1. openscadLocation needs to be set

--configFile=config.ini
        Path to the config file. Settings from this file will be aplied if the file exists. Settings have to be in the [DEFAULT] section.
```

## Requirements
* Python
* OpenSCAD
* `svgoutline` Python library