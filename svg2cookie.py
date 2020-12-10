import getopt
import sys
import os
import svgoutline
import svgoutline
import configparser
import subprocess
import xml.etree.ElementTree

globalOptions = {
	"baseWidth": [4, "Width of the base"],
	"baseHeight": [1, "Height of the base"],

	"cutterWidth": [0.5, "Width of the cutter extrusion"],
	"cutterHeight": [10, "Height of the cutter extrusioon (including wedge)"],
	"cutterWedgeHeight": [1, "Height of the wedge of the cutter extrusion. The larger this number, the sharper the cutter."],

	"meshAlways": [0, "If set to 1, a support mesh is always generated"],
	"meshDistance": [10, "Distance of mesh grills"],
	"meshWidth": [1, "Width of mesh grills"],
	"meshArea": [400, "Area where the mesh is generated (+-)"],

	"openscadLocation": [None, "Location of the scad exe file"],
	"genStl": [0, "Will automatically generate STL files if set to 1. openscadLocation needs to be set"],

	"configFile": ["config.ini", "Path to the config file (config.ini by default). Settings from this file will be aplied if the file exists."],
}

templateContent = open(os.path.dirname(os.path.realpath(__file__)) + "/supp/template.scad", "r").read()

def processFile(filename):
	print(F"Processing '{filename}'...");

	options = globalOptions
	absoluteFilePath = os.path.realpath(filename)

	# Generate scad file
	if True:
		scadContent = ""

		svgData = svgoutline.svg_to_outlines(xml.etree.ElementTree.parse(filename).getroot(), 32, 32)
		scadContent += "lines = ["
		lineI = 0
		for lineData in svgData:
			if lineI > 0:
				scadContent += ", "

			scadContent += "["
			pointI = 0

			for point in lineData[2]:
				if pointI > 0:
					scadContent += ", "

				scadContent += F"[{point[0]}, {point[1]}]"
				pointI += 1
				
			scadContent += "]"
			lineI += 1

		scadContent += "];\n"

		for key, data in options:
			scadContent += F"{key} = {data[0] if isnumeric(data[0]) else F"\"{data[0]}\""};\n"

		scadContent += templateContent

		open(os.path.splitext(absoluteFilePath)[0] + ".scad", "w").write(scadContent)

	if options["genStl"][0] == 1:
		subprocess.run([options["openscadLocation"][0], absoluteFilePath, "--o", "stl"])

	print(F"Processed '{filename}'...");

def main():
	try:
		# Parse command line options
		optlist, files = getopt.getopt(sys.argv[1:], "", map(lambda x : x + "=", globalOptions.keys()))
		for key, value in optlist:
			globalOptions[key][0] = value

		# Prase config file
		if path.exists(globalOptions["configFile"][0]):
			config = configparser.ConfigParser()
			config.read(globalOptions["configFile"][0])

			for key, value in config["DEFAULT"]:
				globalOptions[key] = [value, "--"]

		# Process files
		executor = ThreadPoolExecutor()
		for file in files:
			executor.submit(processFile, file)

	except Exception as e:
		print(e.message)

main()
