function getLiveData(rows = 8, callback){
    $.ajax({
        url: "getrawdata",
        type: "GET",
        data: { rows : rows,
                //from_var : $('#location_from').val()
             },

        success: function(response) {
            console.log(response); //TESTING

            callback(response);
        },

        error: function(xhr, errmsg, err) {
            console.log(xhr, errmsg, err);
        }
    });
}

//UNFINISHED!!!
function getStoredData(rows = all, callback){
    $.ajax({
        url: "getstoreddata",
        type: "GET",
        data: { rows : rows,
                //from_var : $('#location_from').val()
             },

        success: function(response) {
            console.log(response); //TESTING

            callback(response);
        },

        error: function(xhr, errmsg, err) {
            console.log(xhr, errmsg, err);
        }
    });
}