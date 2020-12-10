// The cutter
minkowski() {
	union() for(line = lines) {
		linear_extrude(height=0.001) difference() {
			offset(delta=0.001) polygon(points = line);
			offset(delta=-0.001) polygon(points = line);
		}
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
if(len(lines) > 1 || meshAlways == 1) linear_extrude(height=baseHeight) intersection() {
	union() for(i = [-meshArea : meshDistance : meshArea]) {
		translate([i, 0, 0]) {
			rotate([0, 0, 45]) square(size=[meshArea * 3, meshWidth], center=true);
			rotate([0, 0, -45]) square(size=[meshArea * 3, meshWidth], center=true);
		}
	}

	union() for(line = lines) polygon(points=line);
}