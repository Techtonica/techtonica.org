function openPopupForm() {
  document.cookie = 'MCEvilPopupClosed=;path=/;expires=Thu, 01 Jan 1970 00:00:00 UTC;';
  require(['mojo/signup-forms/Loader'],
  function (L) {
    L.start({'baseUrl':'mc.us13.list-manage.com','uuid':'110f637e29d9b2b5f89664fe8','lid':'22f1ab3b1f'})
  });
}

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = 'expires=' + d.toUTCString();
  document.cookie = cname + '=' + cvalue + '; ' + expires;
}

function getCookie(cname) {
  var name = cname + '=';
  var ca = document.cookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length,c.length);
    }
  }
  return '';
}

function cookieExists(cname) {
  var cookie=getCookie(cname);
  if (cookie !== '') {
    return true;
  } else {
    return false;
  }
}

$('a.contact').on('click', function(){
  var href = $(this).attr('href');
  $(this).attr('href', href.replace('badmail.', ''));
});

$(document).ready(function() {

  // check cookie to see if the user has visited if not popup newsletter registration.
  if (cookieExists('techtonica-visited') === false) {
    openPopupForm();
    setCookie('techtonica-visited', 'yes', 9999)
  }

  function scrollDown(name, time) {
    var aTag = $('.' + name);
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

  $('.supporters').click(function() {
    scrollDown('our-supporters', 1000)
  });

  $('.lines-button').click(function(){
    $(this).toggleClass('x close');
    $('.nav-bar').toggleClass('small-screen-nav');
    $('.nav-link').toggleClass('nav-link--mobile');
  });
});
