import getopt
import sys
import os
import svgoutline
import svgoutline
import configparser
import subprocess
import traceback
import concurrent.futures
import xml.etree.ElementTree

globalOptions = {
	"baseWidth": [4, "(mm) Width of the base"],
	"baseHeight": [1, "(mm) Height of the base"],

	"cutterWidth": [0.5, "(mm) Width of the cutter extrusion"],
	"cutterHeight": [10, "(mm) Height of the cutter extrusioon (including wedge)"],
	"cutterWedgeHeight": [1, "(mm) Height of the wedge of the cutter extrusion. The larger this number, the sharper the cutter."],

	"meshAlways": [0, "If set to 1, a support mesh is always generated"],
	"meshDistance": [10, "(mm) Distance of mesh grills"],
	"meshWidth": [1, "(mm) Width of mesh grills"],
	"meshArea": [400, "(mm) Area where the mesh is generated (+-)"],

	"openscadLocation": [None, "Location of the scad exe file"],
	"genStl": [0, "Will automatically generate STL files if set to 1. openscadLocation needs to be set"],

	"configFile": ["config.ini", "Path to the config file. Settings from this file will be aplied if the file exists. Settings have to be in the [DEFAULT] section."],
}

templateContent = open(os.path.dirname(os.path.realpath(__file__)) + "/supp/template.scad", "r").read()

def processFile(filename):
	try:
		print(F"Processing '{filename}'...");

		options = globalOptions
		absoluteFilePath = os.path.realpath(filename)
		baseFilePath = os.path.splitext(absoluteFilePath)[0]

		scadFilePath = baseFilePath + ".scad"
		stlFilePath = baseFilePath + ".stl"

		# Generate scad file
		if True:
			scadContent = ""

			svgData = svgoutline.svg_to_outlines(xml.etree.ElementTree.parse(filename).getroot(), pixels_per_mm=10)
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

			for key, data in options.items():
				val = data[0] if str(data[0]).replace('.', '', 1).isnumeric() else F"\"{str(data[0])}\""
				scadContent += F"{key} = {val};\n"

			scadContent += templateContent

			open(scadFilePath, "w").write(scadContent)

		if str(options["genStl"][0]) == "1":
			subprocess.run([options["openscadLocation"][0], scadFilePath, "--o", stlFilePath])

		print(F"Processed '{filename}'...");

	except Exception as e:
		traceback.print_exc()

def main():
	try:
		# Parse command line options
		optlist, files = getopt.getopt(sys.argv[1:], "", list(map(lambda x : x + "=", globalOptions.keys())) + ["help"])

		for key, value in optlist:
			if key == "--help":
				print("Danol's Cookie Cutter STL Generator\n\nUsage:\n\tsvg2cookie (options) (file1) (file2) (dir1)\n\nOptions:")

				for key, data in globalOptions.items():
					print(F"--{key}={data[0]}\n\t{data[1]}\n")

				return

			globalOptions[key.lstrip("--")] = [value, "--"]

		# Prase config file
		if os.path.exists(globalOptions["configFile"][0]):
			config = configparser.ConfigParser()
			config.optionxform=str
			config.read(globalOptions["configFile"][0])

			cfg = config["DEFAULT"]
			for key in cfg:
				globalOptions[key] = [cfg.get(key), "--"]

		else:
			print("Config file not found.")

		# Process files
		executor = concurrent.futures.ThreadPoolExecutor()
		for file in files:
			executor.submit(processFile, file)

	except Exception as e:
		traceback.print_exc()

main()
