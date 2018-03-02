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
			d3.csv('ufo_dataset_final_with_lat_lon.csv', function(err, data){


				d3.csv('us_airports.csv', function(err, data2){
					// Adding a filter function to filter the data based on parameters
					var filterFunction = function(filter_key, filter_value){
						var filterData = data.filter(function(d){
							if(d[filter_key] == filter_value){
								return d;
							}
						});

						return filterData;
					}





					l = [[-73.9866136,40.7306458], [-118.24368,34.05224] ,["none", "none"], [-77.211630,38.700660]];
					ufo_coords = []
					meteor_coords = []
					major_metro_coords = []
					airport_coords = []
					satellite_coords = [[-80.52662,28.45077], [-120.5155986,34.7425933], [-75.45752345,37.93843385], [-74.151876, 40.012573], [-152.342484, 57.4346198]]
					aa = [-118.24368, 34.05224];
					bb = [-118.24368, 34.05224];

					var color_hash = {  
						0 : ["UFO Sighting", "green"],
						1 : ["Satellite Launch Station", "red"]
						// 2 : ["Major Sport Sighting", "yellow"]
					}

					id_added = []
					// filteredData = filterFunction('meteor_sighting', 1);
					filteredData = data
					console.log(filteredData)
					dataset = []


					for (var i = 0; i< filteredData.length; i++){
						try {
							var rowID = filteredData[i]['id']
							if (id_added.indexOf(rowID) == -1){
								console.log(filteredData[i]['metorite_long']);
								ufo_coords.push([filteredData[i]["geocoded_longitude"], filteredData[i]["geocoded_latitude"]])
								meteor_coords.push([filteredData[i]['metorite_long'], filteredData[i]['metorite_lat']])
								major_metro_coords.push([filteredData[i]['sports_metro_lon'], filteredData[i]['sports_metro_lat']])
								airport_coords.push([filteredData[i]['airport_lon'], filteredData[i]['airport_lat']])
								id_added.push(rowID)
							}
						} catch (e) {

						} finally {

						}
					}

					// console.log(data2)

					// for(var j=0; j<data2.length; j++){
					// 	// console.log(data2[j]['coordinates'].replace(/\s/g,'').split(','))
					// 	coords = data2[j]['coordinates'].replace(/\s/g,'').split(',')
					// 	// console.log(coords[0])
					// 	// break;
					// 	airport_coords.push([coords[0], coords[1]])
					// }



					dataset[0] = ufo_coords
					dataset[1] = satellite_coords
					// dataset[2] = sports_coords



					svg.selectAll("rect")
						.data(dataset[0]).enter()
						.append("rect")
						.attr("x", function(d){ return projection(d)[0]; })
						.attr("y", function(d){ return projection(d)[1]; })
						.attr("width", "4px")
						.attr("height", "4px")
						.attr("fill", "green")


					svg.selectAll("circle")
						.data(dataset[1]).enter()
						.append("circle")
						.attr("cx", function(d){ return projection(d)[0]; })
						.attr("cy", function(d){ return projection(d)[1]; })
						.attr("r", "10px")
						.attr("fill", "red")
						.style("opacity", 1)


					var legend = svg.append("g")
							  	.attr("class", "legend")
							  	.attr("height", 100)
							  	.attr("width", 100)
						    	.attr('transform', 'translate(-100,400)');

					legend.selectAll('rect')
						.data(dataset)
						.enter()
						.append('rect')
						.attr("x", width - 65)
				        .attr("y", function(d, i){ return i *  20;})
				        .attr("width", 10)
	  					.attr("height", 10)
	  					.style("fill", function(d) { 
					        var color = color_hash[dataset.indexOf(d)][1];
					        return color;
					      });

	  				legend.selectAll('text')
				      .data(dataset)
				      .enter()
				      .append("text")
					  .attr("x", width - 52)
				      .attr("y", function(d, i){ return i *  20 + 9;})
					  .text(function(d) {
				        var text = color_hash[dataset.indexOf(d)][0];
				        return text;
				      });
				})




				});

				// svg.selectAll("circle")
				// .data([aa,bb]).enter()
				// .append("circle")
				// .attr("cx", function (d) { console.log(projection(d)); return projection(d)[0]; })
				// .attr("cy", function (d) { return projection(d)[1]; })
				// .attr("r", "8px")
				// .attr("fill", "red")


});
