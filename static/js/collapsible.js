$(document).ready(function () {
  $(".collapsible").click(function () {
    $(this).toggleClass("collapsible-active");
    $(this).next(".collapsible-content").toggle();
  });

  /* Expanding a collapsible lengthens the page. If you expand one, navigate 
  away, and then return, the collapsible will be closed, and the view will 
  scroll to the bottom of the page. I could fix this by remembering collapsible
  state in a cookie or something, but the effort/reward ratio is poor. 
  Instead, just scroll back to the top. */
  if ($(".collapsible")[0]) {
    $(window).on("beforeunload", function () {
      $(window).scrollTop(0);
    });
  }
});
