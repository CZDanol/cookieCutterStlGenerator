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

// Waternark
if(watermark) intersection() {
	translate([0, 0, baseHeight]) linear_extrude(height=cutterHeight) difference() {
		offset(delta=cutterWidth / 2 + 0.5) resize([w, 0, 0], auto=true) import(sourceFile, center=true);
		offset(delta=-cutterWidth / 2 - 0.5) resize([w, 0, 0], auto=true) import(sourceFile, center=true);
	}

	translate([0, 0, baseHeight + cutterHeight / 2]) rotate([90, 0, 0]) linear_extrude(height=1000)
	text(watermarkText, size=4, font="Fira Sans", halign="center", valign="center");
}