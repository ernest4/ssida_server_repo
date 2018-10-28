$(window).on('load', function () {
    $( "#cookieClose" ).on( "click", function() {
        checkCookie(true);
    });

    checkCookie();

    function checkCookie(set=false) {
        $.get( "agreetocookie", { allowCookie: set }, function( cookiePermision ) {
            console.log(cookiePermision); //TESTING

            if (!cookiePermision.allowCookie) {
                $( "#cookieAlert").css({ display: "block" });
            }
        });
    }
});