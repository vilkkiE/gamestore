/**
 * When the share button is clicked this script opens a new window to Facebook where the player
 * can share the game.
*/
$(document).ready(function() {
    $('#sharebutton').bind('click', function(e){
        e.preventDefault();
        var title = 'JavaScript Gamestore';
        var image_url = 'https://media.licdn.com/mpr/mpr/p/1/005/06a/152/1c6c64b.jpg';
        var facebook_appID = '731336653632731';
        var desc = $('#sharebutton').attr("data-name") + " is an awesome game! " +
            "You can now buy and play it too for just " + $('#sharebutton').attr("data-price") + "!";
        url = "https://www.facebook.com/dialog/feed?app_id="+ facebook_appID +
                    "&link=" + encodeURIComponent($('#sharebutton').attr("data-href")) +
                    "&name=" + encodeURIComponent(title) +
                    "&caption=" + encodeURIComponent('Shared from http://morning-hollows-34668.herokuapp.com/') +
                    "&description=" + encodeURIComponent(desc) +
                    "&picture=" + encodeURIComponent(image_url) +
                    "&redirect_uri=https://www.facebook.com";
        window.open(url);
    });
});