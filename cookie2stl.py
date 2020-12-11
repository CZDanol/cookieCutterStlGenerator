import getopt
import sys
import os
import re
import configparser
import subprocess
import traceback
import concurrent.futures

globalOptions = {
	"baseWidth": [4, "(mm) Width of the base"],
	"baseHeight": [1, "(mm) Height of the base"],

	"cutterWidth": [0.5, "(mm) Width of the cutter extrusion"],
	"cutterHeight": [10, "(mm) Height of the cutter extrusioon (including wedge)"],
	"cutterWedgeHeight": [1, "(mm) Height of the wedge of the cutter extrusion. The larger this number, the sharper the cutter."],

	"mesh": [0, "If set to 1, a support mesh is generated (needed for multi-path cutters)"],
	"meshDistance": [10, "(mm) Distance of mesh grills"],
	"meshWidth": [1, "(mm) Width of mesh grills"],
	"meshArea": [400, "(mm) Area where the mesh is generated (+-)"],

	"watermark": [1, "If set to 1, a watermark is added on the cutter"],
	"watermarkText": ["DANOL", "Text of the watermark"],

	"openscadLocation": [None, "Location of the scad exe file"],
	"genStl": [0, "Will automatically generate STL files if set to 1. openscadLocation needs to be set"],
}

templateContent = open(os.path.dirname(os.path.realpath(__file__)) + "/supp/template.scad", "r").read()
fielConfigPattern = re.compile("^([a-zA-Z]+)=(.+)$")

def processFile(filename):
	try:
		absoluteFilePath = os.path.realpath(filename)
		baseFilePath = os.path.splitext(absoluteFilePath)[0]

		print(F"Processing '{filename}'...");

		options = globalOptions

		scadFilePath = baseFilePath + ".scad"
		stlFilePath = baseFilePath + ".stl"
		configFilePath = os.path.join(os.path.dirname(absoluteFilePath), "config.ini")

		# Load config file in the directory
		if os.path.exists(configFilePath):
			config = configparser.ConfigParser()
			config.optionxform=str
			config.read(configFilePath)

			cfg = config["DEFAULT"]
			for key in cfg:
				options[key] = [cfg.get(key), "--"]

		# Parse file name for options
		for part in os.path.basename(baseFilePath).split("_"):
			m = fielConfigPattern.match(part)
			if m:
				options[m.group(1)] = [m.group(2), "--"]


		options["sourceFile"] = [absoluteFilePath.replace("\\", "\\\\"), "--"]

		# Generate scad file
		if True:
			scadContent = ""

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
		optlist, entries = getopt.getopt(sys.argv[1:], "", list(map(lambda x : x + "=", globalOptions.keys())) + ["help"])

		for key, value in optlist:
			if key == "--help":
				print("Danol's Cookie Cutter STL Generator\n\nUsage:\n\tcookie2stl (options) (files or dirs)\n\nOptions:")

				for key, data in globalOptions.items():
					print(F"--{key}={data[0]}\n\t{data[1]}\n")

				return

			globalOptions[key.lstrip("--")] = [value, "--"]

		# Prase config file
		if False and os.path.exists("config.ini"):
			config = configparser.ConfigParser()
			config.optionxform=str
			config.read("config.ini")

			cfg = config["DEFAULT"]
			for key in cfg:
				globalOptions[key] = [cfg.get(key), "--"]

		# Process files
		executor = concurrent.futures.ThreadPoolExecutor()
		for entry in entries:
			if os.path.isdir(entry):
				for root, dirs, files in os.walk(entry):
					for file in filter(lambda f: f.endswith(".svg") or f.endswith(".dwf"), files):
						executor.submit(processFile, os.path.join(root, file))
			else:
				executor.submit(processFile, entry)

	except Exception as e:
		traceback.print_exc()

main()
