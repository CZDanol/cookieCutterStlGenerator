baseWidth = 4;
baseHeight = 1;
cutterWidth = 0.5;
cutterHeight = 10;
cutterWedgeHeight = 1;
mesh = 1;
meshDistance = 10;
meshWidth = 1;
meshArea = 400;
watermark = 1;
watermarkText = "DANOL";
openscadLocation = "D:/Programy/OpenSCAD/openscad.exe";
genStl = 1;
sourceFile = "D:\\Tvorba\\3D\\2020\\cookieCutterGenerator\\examples\\danol_mesh=1.svg";
// The cutter
minkowski() {
	linear_extrude(height=0.001) difference() {
		offset(delta=0.001) import(sourceFile, center=true);
		offset(delta=-0.001) import(sourceFile, center=true);
	}

	// This is the "extrusion" profile
	rotate_extrude($fn=8) polygon(points=[
		[0, 0],
		[baseWidth / 2, 0],
		[baseWidth / 2, baseHeight],
		[cutterWidth / 2, baseHeight],
		[cutterWidth / 2, baseHeight + cutterHeight - cutterWedgeHeight],
		[0, baseHeight + cutterHeight]
	]);
}

// Mesh for connecting multiple polygons
if(mesh) linear_extrude(height=baseHeight) {
	intersection() {
		union() for(i = [-meshArea : meshDistance : meshArea]) {
			translate([i, 0, 0]) {
				rotate([0, 0, 45]) square(size=[meshArea * 3, meshWidth], center=true);
				rotate([0, 0, -45]) square(size=[meshArea * 3, meshWidth], center=true);
			}
		}

		hull() import(sourceFile, center=true);
	}

	difference() {
		offset(r=baseWidth/2) hull() import(sourceFile, center=true);
		offset(r=-baseWidth/2) hull() import(sourceFile, center=true);
	}
}

// Waternark
if(watermark) intersection() {
	translate([0, 0, baseHeight]) linear_extrude(height=cutterHeight) difference() {
		offset(delta=cutterWidth) import(sourceFile, center=true);
		offset(delta=-cutterWidth) import(sourceFile, center=true);
	}

	translate([0, 0, baseHeight + cutterHeight / 2]) rotate([90, 0, 0]) linear_extrude(height=1000)
	text(watermarkText, size=4, font="Fira Sans", halign="center", valign="center");
}