baseWidth = 4;
baseHeight = 1;
cutterWidth = 0.8;
cutterHeight = 10;
cutterWedgeHeight = 3;
mesh = 1;
meshDistance = 10;
meshWidth = 1;
meshArea = 400;
w = 0;
openscadLocation = "D:/Programy/OpenSCAD/openscad.exe";
genStl = 1;
sourceFile = "D:\\Tvorba\\3D\\3D_2020\\cookieCutterGenerator\\examples\\danol_mesh=1.svg";
// The cutter
minkowski() {
	linear_extrude(height=0.001) difference() {
		offset(delta=0.001) resize([w, 0, 0], auto=true) import(sourceFile, center=true);
		offset(delta=-0.001) resize([w, 0, 0], auto=true) import(sourceFile, center=true);
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

		hull() resize([w, 0, 0], auto=true) import(sourceFile, center=true);
	}

	difference() {
		offset(r=baseWidth/2) hull() resize([w, 0, 0], auto=true) import(sourceFile, center=true);
		offset(r=-baseWidth/2) hull() resize([w, 0, 0], auto=true) import(sourceFile, center=true);
	}
}