function openPopupForm() {
  document.cookie = 'MCEvilPopupClosed=;path=/;expires=Thu, 01 Jan 1970 00:00:00 UTC;';
  require(["mojo/signup-forms/Loader"],
  function (L) {
    L.start({"baseUrl":"mc.us13.list-manage.com","uuid":"110f637e29d9b2b5f89664fe8","lid":"22f1ab3b1f"})
  });
}

$(document).ready(function() {

  function scrollDown(name, time) {
    var aTag = $("." + name);
    $('html,body').animate({
        scrollTop: aTag.offset().top - 75
      },
      time, 'swing');
  }

  $('.howitworks').click(function() {
    scrollDown('how-it-works', 1000);
  });

  $('.why').click(function() {
    scrollDown('why-why', 1000);
  });

  $('.whatwedo').click(function() {
    scrollDown('what-we-do', 1000);
  });

  $('.howtohelp').click(function() {
    scrollDown('how-to-help', 1000);
  });

  $('.lines-button').click(function(){
    $(this).toggleClass('x close');
    $('.nav-bar').toggleClass('small-screen-nav');
    $('.nav-link').toggleClass('nav-link--mobile');
  });

});