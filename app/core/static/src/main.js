window.Intercooler = require("intercooler");
window.$ = window.jQuery = require('jquery'); 


var Turbolinks = require("turbolinks")
Turbolinks.start()


document.addEventListener("turbolinks:load", function() {

  if ($(document).data('ic-init')) return;
  document.addEventListener("turbolinks:render", function(){Intercooler.processNodes($('body'));})
  $(document).data('ic-init', true);
});
