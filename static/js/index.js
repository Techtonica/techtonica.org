function openPopupForm() {
  document.cookie =
    "MCEvilPopupClosed=;path=/;expires=Thu, 01 Jan 1970 00:00:00 UTC;";
  require(["mojo/signup-forms/Loader"], function (L) {
    L.start({
      baseUrl: "mc.us13.list-manage.com",
      uuid: "110f637e29d9b2b5f89664fe8",
      lid: "22f1ab3b1f",
    });
  });
}

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
  var expires = "expires=" + d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) === " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function cookieExists(cname) {
  var cookie = getCookie(cname);
  if (cookie !== "") {
    return true;
  } else {
    return false;
  }
}

const timeWrapper = document.querySelector('.timeline-wrapper')
const timelines = document.querySelectorAll('.timeline li .data');
for (const time of timelines) {
  time.onclick = () => time.classList.toggle('show');
}
const links = document.getElementsByClassName('links-inside');
for (const link of links) {
  link.addEventListener('click', (event) => event.stopPropagation());
}


$(document).ready(function () {
  // check cookie to see if the user has visited if not popup newsletter registration.
  if (cookieExists("techtonica-visited") === false) {
    openPopupForm();
    setCookie("techtonica-visited", "yes", 9999);
  }
});

