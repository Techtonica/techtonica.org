document.addEventListener('DOMContentLoaded', () => {
    window.open_window = function(cause_id, domain_link) {
        var protocol = String(document.location.protocol);

        var new_url;

        if (
          /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
            navigator.userAgent,
          )
        ) {
          //new_url="https://www."+ domain_link +"/widget/"+cause_id
          new_url = "https://www.flipcause.com/widget/" + cause_id;

          window.open(new_url);
        } else {
          document.getElementById("fc-lightbox-loader").style.display = "block";

          document.getElementById("fc-fade").style.display = "block";

          document.getElementById("fc-fade").style.webkitAnimation =
            "backfadesin .5s";

          document.getElementById("fc-fade").style.animation =
            "backfadesin .5s";

          document.getElementById("fc-fade").style.mozAnimation =
            "backfadesin .5s";

          document.getElementById("fc-light").style.display = "block";

          document.getElementById("fc-light").style.webkitAnimation =
            "fadesin 0s";

          document.getElementById("fc-light").style.animation = "fadesin 0s";

          document.getElementById("fc-light").style.mozAnimation = "fadesin 0s";

          document.getElementById("fc-main").style.display = "block";

          document.getElementById("fc-main").style.webkitAnimation =
            "fadesin 2.2s";

          document.getElementById("fc-main").style.animation = "fadesin 2.2s";

          document.getElementById("fc-main").style.mozAnimation =
            "fadesin 2.2s";

          document.getElementById("fc-close").style.display = "block";

          document.getElementById("fc-close").style.webkitAnimation =
            "fadesin 2.2s";

          document.getElementById("fc-close").style.animation = "fadesin 2.2s";

          document.getElementById("fc-close").style.mozAnimation =
            "fadesin 2.2s";

          document.getElementById("fc-myFrame").style.display = "block";

          document.getElementById("fc-myFrame").style.webkitAnimation =
            "fadesin 2.2s";

          document.getElementById("fc-myFrame").style.animation =
            "fadesin 2.2s";

          document.getElementById("fc-myFrame").style.mozAnimation =
            "fadesin 2.2s";

          //document.getElementById("fc-myFrame").src="https://www."+ domain_link +"/widget/"+cause_id;

          document.getElementById("fc-myFrame").src =
            "https://www.flipcause.com/widget/" + cause_id;
        }
    };
  
    window.close_window = function() {
        document.getElementById("fc-lightbox-loader").style.display = "none";

        document.getElementById("fc-fade").style.display = "none";

        document.getElementById("fc-light").style.display = "none";

        document.getElementById("fc-main").style.display = "none";

        document.getElementById("fc-close").style.display = "none";

        document.getElementById("fc-myFrame").style.display = "none";
    };
  
    window.embed_frame = function(cause_id, domain_link) {
        document.getElementById("fc-embed-loader").style.display = "block";

        document.getElementById("fc-embed-main-box").style.display = "block";

        document.getElementById("fc-embed-main-box").style.webkitAnimation =
          "fadesin 2s";

        document.getElementById("fc-embed-main-box").style.animation =
          "fadesin 2s";

        document.getElementById("fc-embed-main-box").style.mozAnimation =
          "fadesin 2s";

        document.getElementById("fc-embed-frame").style.display = "block";

        document.getElementById("fc-embed-frame").style.webkitAnimation =
          "fadesin 2s";

        document.getElementById("fc-embed-frame").style.animation =
          "fadesin 2s";

        document.getElementById("fc-embed-frame").style.mozAnimation =
          "fadesin 2s";

        //document.getElementById("fc-embed-frame").src="https://www."+ domain_link +"/widget/"+cause_id;

        document.getElementById("fc-embed-frame").src =
          "https://www.flipcause.com/widget/" + cause_id;
    };
  });