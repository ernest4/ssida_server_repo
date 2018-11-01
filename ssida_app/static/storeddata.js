$(window).on('load', function () {

    $( "#downloadDataButton" ).on( "click", function() {
        let rows = $('#rowsInput').val();

        window.location = "downloadData?"+
                          "rows="+rows+
                          "&"+
                          "device_ids="+"all"+
                          "&"+
                          "date_time_old="+"none"+
                          "&"+
                          "date_time_new="+"none";
    });

    //handling submit button
    $( "#submitQueryButton" ).on( "click", function() {
        let rows = $('#rowsInput').val();

        getStoredData(rows, 'all', 'none', 'none', function(data){

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



    $( "#downloadDataButtonAdvanced" ).on( "click", function() {
        let rows = $('#rowsInputAdvanced').val();
        let device_ids = $('#deviceIdInput').val();
        let date_time_old = $('#dateTimeInputOldest').val();
        let date_time_new = $('#dateTimeInputNewest').val();

        window.location = "downloadData?"+
                          "rows="+rows+
                          "&"+
                          "device_ids="+device_ids+
                          "&"+
                          "date_time_old="+date_time_old+
                          "&"+
                          "date_time_new="+date_time_new;
    });

    //handling submit button
    $( "#submitQueryButtonAdvanced" ).on( "click", function() {
        let rows = $('#rowsInputAdvanced').val();
        let device_ids = $('#deviceIdInput').val();
        let date_time_old = $('#dateTimeInputOldest').val();
        let date_time_new = $('#dateTimeInputNewest').val();

        getStoredData(rows, device_ids, date_time_old, date_time_new, function(data){

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