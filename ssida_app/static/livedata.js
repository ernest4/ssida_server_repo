$(window).on('load', function () {

    function getLiveData(){
        $.ajax({
            url: "getrawdata",
            type: "GET",
            data: { rows : 5,
                    //from_var : $('#location_from').val()
                 },

            success: function(response) {
                console.log(response); //TESTING

                //document.getElementById('test').innerHTML = response; //more efficient than using jQuery equivalent...
                //document.getElementById('response').scrollIntoView();
            },

            error: function(xhr, errmsg, err) {
                console.log(xhr, errmsg, err);
            }
        });
    }

    getLiveData();
});