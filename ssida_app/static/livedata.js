$(window).on('load', function () {
    //---visualization code--- with help from Xinyue Wang ---
    // Define margins
    var margin = { top: 10, right: 10, bottom: 45, left: 55 };

    //Width and height
    var outer_width = 900;
    var outer_height = 450;
    var svg_width = outer_width - margin.left - margin.right;
    var svg_height = outer_height - margin.top - margin.bottom;

    // The year to display
    //let display_year = 2007;

    // define a function that filters data by year
    function dataFilter(value) {
        return true; //all pass filter for now...
        //return (value.Year == display_year)
    }

    //data formating for D3.js
    function parseData(dataset, test = false){
        if (!test) {
            let arr = [];

            _.forEach(dataset, function(row){
                let str = row.fields.device_id;

                let item = {
                    pk : +row.pk,
                    fields : { device_id : str.slice(str.length-7, str.length),
                        latitude : +row.fields.latitude,
                        longitude : +row.fields.longitude,
                        accelerometer_x : +row.fields.accelerometer_x,
                        accelerometer_y : +row.fields.accelerometer_y,
                        accelerometer_z : +row.fields.accelerometer_z,
                        gyroscope_x : +row.fields.gyroscope_x,
                        gyroscope_y : +row.fields.gyroscope_y,
                        gyroscope_z : +row.fields.gyroscope_z,
                        timestamp : new Date(row.fields.timestamp)
                    }
                };

                arr.push(item);
            });

            //console.log("parseData:: arr->"+arr[0].fields.accelerometer_x); //TESTING
            return arr;
        } else {
            let arr = [];

            let str1 = "com.google.android.gms.iid.InstanceID@4ee6c85";

            let item1 = {
                pk : 32812,
                fields : { device_id : str1.slice(str1.length-7, str1.length),
                    latitude : +0.0,
                    longitude : +0.0,
                    accelerometer_x : -0.03896594,
                    accelerometer_y : 0.0074944496,
                    accelerometer_z : 0.17051125,
                    gyroscope_x : 0.22357668,
                    gyroscope_y : 0.535118,
                    gyroscope_z : -0.093462385,
                    timestamp : new Date("2018-11-12T19:34:06.288Z")
                }
            };

            arr.push(item1);

            let str2 = "com.google.android.gms.iid.InstanceID@4ee6c85";

            let item2 = {
                pk : 32811,
                fields : { device_id : str2.slice(str2.length-7, str2.length),
                    latitude : +0.0,
                    longitude : +0.0,
                    accelerometer_x : -0.039434314,
                    accelerometer_y : 0.084646225,
                    accelerometer_z : 0.04882002,
                    gyroscope_x : 0.18753563,
                    gyroscope_y : 0.36041048,
                    gyroscope_z : -0.025045475,
                    timestamp : new Date("2018-11-12T19:34:06.030Z")
                }
            };

            arr.push(item2);

            return arr;
        }
    }

    //Create SVG element as a group with the margins transform applied to it
    var svg = d3.select("#g1")
        .append("svg")
        .attr("width", svg_width + margin.left + margin.right)
        .attr("height", svg_height + margin.top + margin.bottom)
        .style("background", "aliceblue")
        //.style("width", "80vw")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Create linear Y scale for sensor values
    var yScale = d3.scaleLinear()
        .domain([-10, 10])
        .range([svg_height, 0]);

    //Create linear X scale for the time
    var xScale = d3.scaleLinear()
        .domain([0, 100])
        .range([0, svg_width]);

    //var xScale = d3.scaleTime().rangeRound([0, svg_width]);

    //Define Y axis
    var yAxis = d3.axisLeft()
        .scale(yScale)
        .ticks(5)
        .tickFormat(d3.format(".0s"))
        ;

    // Create an x-axis connected to the x scale
    var xAxis = d3.axisBottom()
        .scale(xScale)
        // .tickFormat(d3.format(".0s"))
        .ticks(10, ".0s")
        ;

    // Define the div for the tooltip
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // Call the y axis
    svg.append("g")
        .attr("class", "axis")
        .attr("id", "y-axis")
        .call(yAxis);

    // All but call the x-axis
    svg.append("g")
        .attr("class", "axis")
        .attr("id", "x-axis")
        .attr("transform", "translate(0," + svg_height + ")")
        .call(xAxis)
        ;

    // text label for the x axis
    svg.append("text")
        .attr("transform",
            "translate(" + (outer_width / 2) + " ," +
            (svg_height + margin.top + 30) + ")")
        .style("text-anchor", "middle")
        .text("Time");

    // text label for the y axis
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (svg_height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Sensor Values");

    // Define a fucntion to draw a simple bar chart
    function generateVis(data) {
        //console.log("generateVis:: data->"+data[0].pk); //TESTING
        //console.log("generateVis:: data->"+data[0].fields.device_id); //TESTING

        // Filter the data to only include the current year
        //let filtered_dataset = data.filter(dataFilter);
        let filtered_dataset = data; //no filtering...

        filtered_dataset = parseData(filtered_dataset, false);

        // Update the domain of the x scale
        //xScale.domain(filtered_datset.map(function(d) { return d.Company; }));

        // Call the x-axis
        svg.select("#x-axis").call(xAxis);

        /******** PERFORM DATA JOIN ************/
        // Join new data with old elements, if any.
        /*let points = svg.selectAll("path")
            .data(filtered_dataset, function key(d) {
                return d.pk;
            });*/
        let points = svg.selectAll("paths")
                        .data(filtered_dataset);


        //Create a line for drawing
        let line = d3.line()
                    .x(function(d) { 
                        console.log("d3.line():: x ->"+xScale(d.fields.accelerometer_x)); //TESTING
                        return xScale(d.fields.accelerometer_x)*100;
                        //return xScale(d.fields.timestamp)
                    })
                    .y(function(d) {
                        console.log("d3.line():: y ->"+yScale(d.fields.accelerometer_x)); //TESTING
                         return yScale(d.fields.accelerometer_x)
                        });

        /*xScale.domain(d3.extent(filtered_dataset, function(d) { return d.fields.timestamp }));
        yScale.domain(d3.extent(filtered_dataset, function(d) { return d.fields.accelerometer_x }));*/

        /******** HANDLE UPDATE SELECTION ************/
        // Update the display of existing elelemnts to match new data
        // Perform a data join and add points to the chart
        points
            .transition()
            .duration(2000)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 1.5)
            .attr("d", line(filtered_dataset));

        /******** HANDLE ENTER SELECTION ************/
        // Create new elements in the dataset
        // Perform a data join and add points to the chart
        points.enter()
            .append("path")
            .transition()
            .duration(2000)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 1.5)
            .attr("d", line(filtered_dataset));

        /******** HANDLE EXIT SELECTION ************/
        // Remove elements that not longer have a matching data element
        points.exit()
            .style("fill", "red")
            .transition()
            .duration(2000)
            .remove();

        // Set the year label
        //d3.select("#year_header").text("Year: " + display_year);

    }

    //Add legend frame
    var legend_margin = { top: 10, right: 10, bottom: 10, left: 10 };
    var rect_width = svg_width*0.2;
    var rect_height = svg_height*.2;
    var gap = 10;
    svg.append("rect")
    .attr("x", svg_width-rect_width)
    .attr("y", 0)
    .attr("width", rect_width)
    .attr("height", rect_height)
    .style("fill", "lightsteelblue")
    .style("opacity",.9)
    ;

    //Add legend rects and Text
    var legend_circle_r = svg_width*0.01;
    svg.append("rect")
    .attr("id","blue")
    .attr("x", svg_width-rect_width+legend_margin.left)
    .attr("y", legend_margin.top)
    .attr("width", legend_circle_r)
    .attr("height", legend_circle_r)
    .style("fill", "blue")
    ;

    svg.append("rect")
    // .attr("id","blue")
    .attr("x", svg_width-rect_width+legend_margin.left)
    .attr("y", legend_margin.top+gap+legend_circle_r)
    .attr("width", legend_circle_r)
    .attr("height", legend_circle_r)
    .style("fill", "green")
    ;

    svg.append("rect")
    // .attr("id","blue")
    .attr("x", svg_width-rect_width+legend_margin.left)
    .attr("y", legend_margin.top+2*(gap+legend_circle_r))
    .attr("width", legend_circle_r)
    .attr("height", legend_circle_r)
    .style("fill", "orange")
    ;

    svg.append("rect")
    // .attr("id","blue")
    .attr("x", svg_width-rect_width+legend_margin.left)
    .attr("y", legend_margin.top+3*(gap+legend_circle_r))
    .attr("width", legend_circle_r)
    .attr("height", legend_circle_r)
    .style("fill", "red")
    ;

    svg.append("text")
    .attr("transform",
            "translate(" + (svg_width-rect_width+legend_margin.left+legend_circle_r+gap) + " ," +
            (legend_margin.top+10) + ")")
        // .style("text-anchor", "middle")
        .text("New Enter");

    svg.append("text")
    .attr("transform",
            "translate(" + (svg_width-rect_width+legend_margin.left+legend_circle_r+gap) + " ," +
            (legend_margin.top+10+gap+legend_circle_r) + ")")
        // .style("text-anchor", "middle")
        .text("Update");

    svg.append("text")
    .attr("transform",
            "translate(" + (svg_width-rect_width+legend_margin.left+legend_circle_r+gap) + " ," +
            (legend_margin.top+2*(gap+legend_circle_r)+10) + ")")
        // .style("text-anchor", "middle")
        .text("Missing Value");

    svg.append("text")
    .attr("transform",
            "translate(" + (svg_width-rect_width+legend_margin.left+legend_circle_r+gap) + " ," +
            (legend_margin.top+3*(gap+legend_circle_r)+10) + ")")
        // .style("text-anchor", "middle")
        .text("Exiting");
    //---visualization code---

    
    //getting data periodically, generating visualization and creating the table
    setInterval( function() { 
            getLiveData(8, function(data){

            //---visualization code---
            // Call the x-axis
            svg.select("#x-axis").call(xAxis);
            // Generate the visualisation
            generateVis(data);
            //---visualization code---
    
            let table = document.getElementById('responseTable');
            let tableBody = document.getElementById('tbody_response');

            //remove the old table body with old data
            tableBody.parentNode.removeChild(tableBody);

            //create a new table body
            tableBody = document.createElement('tbody');
            tableBody.setAttribute("id", "tbody_response");
            table.appendChild(tableBody);

            //populate the new table body with fresh data
            _.forEach(data, function(row){
                //for each record from database, create a row
                let tr = document.createElement("tr");

                //primary key is separate from the rest of the fields and will be set first
                let td = document.createElement("td");
                td.innerHTML = row.pk;
                tr.appendChild(td)

                //for each other field in a row, create a column of data
                _.forEach(row.fields, function(column){
                    let td = document.createElement("td");
                    td.innerHTML = column;
                    tr.appendChild(td)
                });

                //append the finished row
                tableBody.appendChild(tr);
            });

        })
    }, 1000); //every second
});