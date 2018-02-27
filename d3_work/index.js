// https://bost.ocks.org/mike/map/
d3.json('usa.json', function(error, usa){
	if(error){
		console.log("Error is ", error);
		return;
	}

	var width = 960,
    height = 1160;

	var svg = d3.select("body").append("svg")
	    .attr("width", width)
	    .attr("height", height);

	var subunits = topojson.feature(usa, usa.objects.sb_usa);

	// var projection = d3.geoMercator()
	//     .scale(100)
	//     .translate([width / 2, height / 2]);

	var projection = d3.geoAlbers()
	    .center([0, 55.4])
	    // .rotate([4.4, 0])
	    .parallels([50, 60])
	    .scale(700)
	    .translate([width / 2, height / 2]);

	var path = d3.geoPath()
    	.projection(projection);

    svg.append("path")
	    .datum(subunits)
			.attr("fill", "#D3D3D3")
	    .attr("d", path);
			// put df_nearest csv here
			d3.csv('df_nearest_airports.csv', function(err, data){
				l = [[-73.9866136,40.7306458], [-118.24368,34.05224] ,["none", "none"], [-77.211630,38.700660]];
				ufo_coords = []
				aa = [-118.24368, 34.05224];
				bb = [-118.24368, 34.05224];


				for (var i = 0; i< data.length; i++){
					try {
						ufo_coords.push([data[i]["geocoded_longitude"], data[i]["geocoded_latitude"]])
					} catch (e) {

					} finally {

					}
				}
				// put meteorite landings csv here
				d3.csv('meteorite-landings.csv', function(err, data1){

					meteor_coords = []

					for(var j=0; j<data1.length; j++){
						meteor_coords.push([data1[j]['reclong'], data1[j]['reclat']])
					}


					console.log(ufo_coords)
					console.log(meteor_coords);

					svg.selectAll("circle")
						.data(meteor_coords).enter()
						.append("circle")
						.attr("cx", function(d){ return projection(d)[0]; })
						.attr("cy", function(d){ return projection(d)[1]; })
						.attr("r", "3px")
						.attr("fill", "red")


						svg.selectAll("circle")
							.data(ufo_coords).enter()
							.append("circle")
							.attr("cx", function(d){ return projection(d)[0]; })
							.attr("cy", function(d){ return projection(d)[1]; })
							.attr("r", "2px")
							.attr("fill", "green")


				});



				});

				// svg.selectAll("circle")
				// .data([aa,bb]).enter()
				// .append("circle")
				// .attr("cx", function (d) { console.log(projection(d)); return projection(d)[0]; })
				// .attr("cy", function (d) { return projection(d)[1]; })
				// .attr("r", "8px")
				// .attr("fill", "red")


});
