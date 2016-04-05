function scrollDown(name, time) {
  var aTag = $("." + name);
  $('html,body').animate({
      scrollTop: aTag.offset().top - 75
    },
    time, 'swing');
}

$('.aboutus').click(function() {
  scrollDown('about-us', 1000);
});

$('.howitworks').click(function() {
  scrollDown('how-it-works', 1000);
});

$('.why').click(function() {
  scrollDown('why-why', 1000);
});

$('.whatwedo').click(function() {
  scrollDown('what-we-do', 1000);
});

$('.lines-button').click(function(){
  $(this).toggleClass('x close');
  $('.nav-bar').toggleClass('small-screen-nav');
  $('.nav-link').toggleClass('nav-link--mobile');
});
