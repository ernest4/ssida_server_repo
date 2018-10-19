$(window).on('load', function () {

    $( "#downloadDataButton" ).on( "click", function() {
        let rows = $('#rowsInput').val();

        window.location = "downloadData?"+"rows="+rows;
    });

    //handling submit button
    $( "#submitQueryButton" ).on( "click", function() {
        let rows = $('#rowsInput').val();

        getStoredData(rows, function(data){

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
        });
    });
});