/**
 * When something is written in the search bar, this script does an ajax post
 * request and then updates the search-results with the data back from the server.
*/
$(document).ready(function() {
   $('#search').keyup(function() {
       $.ajax({
           type: "POST",
           url: "/search/",
           data: {
               'game_name': $('#search').val(),
               'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
           },
           success: searchSuccess,
           dataType: 'html'
       });
   });
});

function searchSuccess(data, textStatus, jqXHR) {
    $('#search-results').html(data);
}