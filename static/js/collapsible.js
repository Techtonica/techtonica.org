$(document).ready(function() {

  $('.collapsible').click(function() {
      $(this).toggleClass("collapsible-active");
      $(this).next(".collapsible-content").toggle();
  });
});
