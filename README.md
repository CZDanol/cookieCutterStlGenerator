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
See `svg2cookie --help` .

## Requirements
* Python
* OpenSCAD
* `svgoutline` Python library