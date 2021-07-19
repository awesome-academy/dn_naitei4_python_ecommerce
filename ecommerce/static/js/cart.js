$(document).ready(function () {
    // catch the form's submit event
        $('#cartForm').submit(function (event) {
            // create an AJAX call
            $.ajax({
                data: $(this).serialize(), // get the form data
                type: $(this).attr('POST'), // GET or POST
                url: $('#cartForm').attr('data-url-name'),
                // on success
                success: function (data) {
                    alert(data)
                },
                // on error
                error: function (data) {
                    // alert the error if any error occured
                    alert(data)
                }
            });
            return false;
        })
    })
    