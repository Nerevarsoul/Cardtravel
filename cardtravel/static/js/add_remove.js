
// start operation
(function ($) {
    $(function () {

		$.ajaxSetup({
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		            // Send the token to same-origin, relative URLs only.
		            // Send the token only if the method warrants CSRF protection
		            // Using the CSRFToken value acquired earlier
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    }
		});

		// add and delete button
        $(document).on("click", ".operation a", function(e) {
            e.preventDefault();
            var card_id = $(this).attr("class");
            var url = $(this).attr("href");
            
            $.ajax({
                type: "POST",
                url: url,
                dataType: "json",
                data: ({"card_id": card_id}),
                success: function (result) {
                    if(result['status'] === 1) {
                        alert(result['status'])
                    } 
                }
            });
    	});


    });
})(jQuery);