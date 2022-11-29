module sourceModel() {
	resize([w, 0, 0], auto=true) scale(scaling) import(sourceFile, center=true);
}

module sourceModelHull() {
	hull() sourceModel();
}

// The cutter
minkowski() {
	linear_extrude(height=0.001) difference() {
		offset(delta=0.001) sourceModel();
		offset(delta=-0.001) sourceModel();
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

		sourceModelHull();
	}

	difference() {
		offset(r=baseWidth/2) sourceModelHull();
		offset(r=-baseWidth/2) sourceModelHull();
	}
}