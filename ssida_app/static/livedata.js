$(window).on('load', function () {
    let visualisationActive = false;
    let maxDisplayRowCount = 10; //for the table
    let rows = maxDisplayRowCount; //rows to fetch

    $( "#visualizationButton" ).on( "click", function() {
        visualisationActive = !visualisationActive; //toggle
        //let rows = $('#rowsInput').val();
        if (visualisationActive) {
            //get enough for both the plot and the table
            rows = 200;
        } else {
            //get just the minimum needed for the table
            rows = maxDisplayRowCount;
        }
        console.log("visButton:: rows -> "+rows);
    });

    let deviceID = "";
    $( "#deviceIDfilterButton" ).on( "click", function() {
        visualisationActive = !visualisationActive; //toggle
        deviceID = $('#deviceIDinput').val();
        console.log("visButton:: rows -> "+deviceID);
    });

    //---visualization code--- with help from Xinyue Wang ---
    // Define margins
    var margin = { top: 10, right: 10, bottom: 45, left: 55 };

    //Width and height
    var outer_width = 1000;
    var outer_height = 450;
    var svg_width = outer_width - margin.left - margin.right;
    var svg_height = outer_height - margin.top - margin.bottom;

    // The year to display
    //let display_year = 2007;
    let firstRun = true;

    // define a function that filters data by year
    function dataFilter(value) {
        //return true; //all pass filter for now...
        return (value.fields.device_id == "com.google.android.gms.iid.InstanceID@"+deviceID);
    }

    //data formating for D3.js
    function parseData(dataset){
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

    function setAxesAndScales(xDomainMin, xDomainMax, yDomainMin, yDomainMax, firstRun){
        // Create linear Y scale for sensor values
        let yScale = d3.scaleLinear()
        .domain([yDomainMin, yDomainMax])
        .range([svg_height, 0]);

        //Create linear X scale for the time
        let xScale = d3.scaleLinear()
            .domain([xDomainMin, xDomainMax])
            //.domain([30000, 33000]) //TESTING
            .range([0, svg_width]);

        //var xScale = d3.scaleTime().rangeRound([0, svg_width]);

        //Define Y axis
        let yAxis = d3.axisLeft()
            .scale(yScale)
            .ticks(5)
            .tickFormat(d3.format(".0s"));

        // Create an x-axis connected to the x scale
        let xAxis = d3.axisBottom()
        .scale(xScale)
        .tickFormat(d3.format(""))
        .ticks(25, "");

        if (firstRun) {
            //Create and attach the axes for the first run
            // Attach and call the y axis
            svg.append("g")
                .attr("class", "axis")
                .attr("id", "y-axis")
                .call(yAxis);

            // Attach and call the x-axis
            svg.append("g")
                .attr("class", "axis")
                .attr("id", "x-axis")
                .attr("transform", "translate(0," + svg_height + ")")
                .call(xAxis);
        } else {
            //just call the axes for update...
            svg.select("#y-axis").call(yAxis);
            svg.select("#x-axis").call(xAxis);
        }

        return {xScale: xScale, yScale: yScale};
    }


    // Define the div for the tooltip
    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // text label for the x axis
    svg.append("text")
        .attr("transform",
            "translate(" + (outer_width / 2) + " ," +
            (svg_height + margin.top + 30) + ")")
        .style("text-anchor", "middle")
        .text("Time: Rows of data for a particular device. 4 rows (not ticks!) represent 1 second of time.");

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

        let xMin = data[0].pk;
        let xMax = data[data.length-1].pk;
        let yMin = -30;
        let yMax = 30;
        let scales = setAxesAndScales(xMin, xMax, yMin, yMax, firstRun);
        if (firstRun) { firstRun = !firstRun };

        // Filter the data to only include the current year
        let filtered_dataset = data.filter(dataFilter);
        //let filtered_dataset = data; //no filtering...

        //filtered_dataset = parseData(filtered_dataset);

        //Prepare canvas
        //d3.select('svg').selectAll('path').remove();

        /******** PERFORM DATA JOIN ************/
        // Join new data with old elements, if any.
        /*let points = svg.selectAll("path")
            .data(filtered_dataset, function key(d) {
                return d.pk;
            });*/

        let points = svg.selectAll("path")
                        .data(filtered_dataset);


        //Create a line for drawing
        let line = d3.line()
                    .x(function(d) { 
                        return scales.xScale(+d.pk);
                    })
                    .y(function(d) {
                        return scales.yScale(d.fields.accelerometer_x)
                    });

        /*xScale.domain(d3.extent(filtered_dataset, function(d) { return d.fields.timestamp }));
        yScale.domain(d3.extent(filtered_dataset, function(d) { return d.fields.accelerometer_x }));*/

        /******** HANDLE UPDATE SELECTION ************/
        // Update the display of existing elelemnts to match new data
        // Perform a data join and add points to the chart
        points
            //.transition()
            //.duration(2000)
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
            //.transition()
            //.duration(2000)
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
            //.transition()
            //.duration(2000)
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
    .style("opacity",.9);

    //Add legend rects and Text
    var legend_circle_r = svg_width*0.01;
    svg.append("rect")
    .attr("id","blue")
    .attr("x", svg_width-rect_width+legend_margin.left)
    .attr("y", legend_margin.top)
    .attr("width", legend_circle_r)
    .attr("height", legend_circle_r)
    .style("fill", "blue");

    svg.append("rect")
    // .attr("id","blue")
    .attr("x", svg_width-rect_width+legend_margin.left)
    .attr("y", legend_margin.top+gap+legend_circle_r)
    .attr("width", legend_circle_r)
    .attr("height", legend_circle_r)
    .style("fill", "green");

    svg.append("rect")
    // .attr("id","blue")
    .attr("x", svg_width-rect_width+legend_margin.left)
    .attr("y", legend_margin.top+2*(gap+legend_circle_r))
    .attr("width", legend_circle_r)
    .attr("height", legend_circle_r)
    .style("fill", "orange");

    svg.append("rect")
    // .attr("id","blue")
    .attr("x", svg_width-rect_width+legend_margin.left)
    .attr("y", legend_margin.top+3*(gap+legend_circle_r))
    .attr("width", legend_circle_r)
    .attr("height", legend_circle_r)
    .style("fill", "red");

    svg.append("text")
    .attr("transform",
            "translate(" + (svg_width-rect_width+legend_margin.left+legend_circle_r+gap) + " ," +
            (legend_margin.top+10) + ")")
        // .style("text-anchor", "middle")
        .text("--");

    svg.append("text")
    .attr("transform",
            "translate(" + (svg_width-rect_width+legend_margin.left+legend_circle_r+gap) + " ," +
            (legend_margin.top+10+gap+legend_circle_r) + ")")
        // .style("text-anchor", "middle")
        .text("--");

    svg.append("text")
    .attr("transform",
            "translate(" + (svg_width-rect_width+legend_margin.left+legend_circle_r+gap) + " ," +
            (legend_margin.top+2*(gap+legend_circle_r)+10) + ")")
        // .style("text-anchor", "middle")
        .text("--");

    svg.append("text")
    .attr("transform",
            "translate(" + (svg_width-rect_width+legend_margin.left+legend_circle_r+gap) + " ," +
            (legend_margin.top+3*(gap+legend_circle_r)+10) + ")")
        // .style("text-anchor", "middle")
        .text("--");
    //---visualization code---

    
    //getting data periodically, generating visualization and creating the table
    setInterval( function() { 
            getLiveData(rows, function(data){

            //---visualization code---
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


            let currentRowCount = 0;
            //populate the new table body with fresh data
            _.forEach(data, function(row){
                if (currentRowCount == maxDisplayRowCount) { //breaks out for foreach loop
                    return false;
                } //else...
                currentRowCount++;

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