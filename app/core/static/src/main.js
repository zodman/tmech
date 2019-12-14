import '@fortawesome/fontawesome-free/js/all.js';
window.$ = window.jQuery = require('jquery'); 
window.Intercooler = require("intercooler");


var Turbolinks = require("turbolinks")
Turbolinks.start()
document.addEventListener("turbolinks:load", function() {
      if ($(document).data('ic-init')) return;
          document.addEventListener("turbolinks:render", function(){
              Intercooler.processNodes($('body'));
            });
           $(document).data('ic-init', true);
            var burger = document.querySelector('.burger');
            var menu = document.querySelector('nav.menu');
            var nav = document.querySelector('#'+burger.dataset.target);
            burger.addEventListener('click', function(){
              burger.classList.toggle('is-active');
              nav.classList.toggle('is-active');
              menu.classList.toggle("is-hidden-touch");
              menu.classList.toggle("is-active");
              
            });

});




