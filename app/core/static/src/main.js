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
});
