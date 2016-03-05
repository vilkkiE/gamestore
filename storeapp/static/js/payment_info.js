$(document).ready(function() {
  window.setInterval(function() {
    window.location.href = $('#link').attr('href');
  }, 2000);
});
