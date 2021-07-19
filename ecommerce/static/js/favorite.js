$(document).ready(function () {
    // catch the form's submit event
        $('.submitFavoriteButton').click(function (event) {
            event.preventDefault();
            // create an AJAX call
            form = $(this).closest("form");
            $.ajax({
                data: { csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
                type: $(form).attr('method'), // GET or POST
                url: $(form).attr('data-url-name'),
                // on success
                success: function (data) {
                    //alert(response);
                    $('.pro_area').remove()
                    $('.product_area').append(data.list)
                }.bind(this),
                error: function(xhr, status, error) {
                    var err = JSON.parse(xhr.responseText);
                    alert(err.Message);
               }
            });
            return false;
        })
    })
    