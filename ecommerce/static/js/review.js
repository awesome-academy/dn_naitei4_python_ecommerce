$(document).ready(function () {
// catch the form's submit event
    $('#commentForm').submit(function (event) {
        // create an AJAX call
        $.ajax({
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $('#commentForm').attr('data-url-name'),
            // on success
            success: function (data) {
                //alert(response);
                $('.close_modal').click();
                $('.no-row').remove();
                $('.review-row').last().append(data.list);
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
