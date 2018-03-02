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


				// Adding a filter function to filter the data based on parameters
				var filterFunction = function(filter_key, filter_value){
					var filterData = data.filter(function(d){
						if(d[filter_key] == filter_value){
							return d;
						}
					});

					return filterData;
				}

				var filterData = data.filter(function(d){
					if(d['meteor_sighting'] == 1){
						return d;
					}
				});


				l = [[-73.9866136,40.7306458], [-118.24368,34.05224] ,["none", "none"], [-77.211630,38.700660]];
				ufo_coords = []
				meteor_coords = []
				major_metro_coords = []
				airport_coords = []
				aa = [-118.24368, 34.05224];
				bb = [-118.24368, 34.05224];

				var color_hash = {  
					0 : ["UFO Sighting", "green"],
					1 : ["Meteorite Sighting", "red"]
					// 2 : ["Major Sport Sighting", "yellow"]
				}

				// filteredData = filterFunction('meteor_sighting', 1);
				filteredData = data
				console.log(filteredData)
				dataset = []


				for (var i = 0; i< filteredData.length; i++){
					try {
						ufo_coords.push([filteredData[i]["geocoded_longitude"], filteredData[i]["geocoded_latitude"]])
						meteor_coords.push([filteredData[i]['meteorite_lon'], filteredData[i]['meteorite_lat']])
						major_metro_coords.push([filteredData[i]['sports_metro_lon'], filteredData[i]['sports_metro_lat']])
						airport_coords.push([filteredData[i]['airport_lon'], filteredData[i]['airport_lat']])
					} catch (e) {

					} finally {

					}
				}

				// console.log("ufo_coord",ufo_coords);
				// console.log("metorite_coord", meteor_coords)


				dataset[0] = ufo_coords
				dataset[1] = airport_coords
				// dataset[2] = sports_coords



				svg.selectAll("rect")
					.data(dataset[1]).enter()
					.append("rect")
					.attr("x", function(d){ return projection(d)[0]; })
					.attr("y", function(d){ return projection(d)[1]; })
					.attr("width", "7px")
					.attr("height", "7px")
					.attr("fill", "red")


				svg.selectAll("circle")
					.data(dataset[0]).enter()
					.append("circle")
					.attr("cx", function(d){ return projection(d)[0]; })
					.attr("cy", function(d){ return projection(d)[1]; })
					.attr("r", "3px")
					.attr("fill", "green")
					.style("opacity", 0.5)


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

				});

				// svg.selectAll("circle")
				// .data([aa,bb]).enter()
				// .append("circle")
				// .attr("cx", function (d) { console.log(projection(d)); return projection(d)[0]; })
				// .attr("cy", function (d) { return projection(d)[1]; })
				// .attr("r", "8px")
				// .attr("fill", "red")


});
