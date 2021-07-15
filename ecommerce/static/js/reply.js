$(document).ready(function () {
    // catch the form's submit event
        $('.submitReplyCmt').click(function (event) {
            event.preventDefault();
            // create an AJAX call
            form = $(this).closest("form");
            $.ajax({
                data: form.serialize(), // get the form data
                type: $(form).attr('method'), // GET or POST
                url: $(form).attr('data-url-name'),
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
    