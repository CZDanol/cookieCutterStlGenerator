# Danol's SVG -> Cookie Cutter STL Generator

## How it works
* Takes in SVG files (even in batch)
  * Works with **STROKES ONLY**. Ignores non-stroked objects.
  * It can contain multiple paths.
* Spits out OpenSCAD files
* If you specify OpenSCAD filepath, it can automatically generate STL files

## Settings
Settings can be specified in multiple ways (ordered by priority)
1. TODO: File names. File name is split by `_` and then every item is scanned against settings list (for example `cook1_h=10.svg`)
1. Command line arguments to the script.
1. TODO: INI file.

### Available settings
TODO: See `svg2cookie --help` .

## Requirements
* Python
* OpenSCAD
* `svgoutline` Python library