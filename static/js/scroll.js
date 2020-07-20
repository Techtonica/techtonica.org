$(document).ready(function () {
  function scrollDown(name, time) {
    var aTag = $("." + name);
    $("html,body").animate(
      {
        scrollTop: aTag.offset().top - 75,
      },
      time,
      "swing"
    );
  }

  $(".whatwedo").click(function () {
    scrollDown("what-we-do", 1000);
  });

  $(".supporters").click(function () {
    scrollDown("our-supporters", 1000);
  });

  $(".lines-button").click(function () {
    $(this).toggleClass("x close");
    $(".nav-bar").toggleClass("small-screen-nav");
    $(".nav-link").toggleClass("nav-link--mobile");
  });
});
