import '@fortawesome/fontawesome-free/js/all.js';
window.Intercooler = require("intercooler");
window.$ = window.jQuery = require('jquery'); 
require("bulmahead/src/bulmahead.js");

function api(value) {
    return new Promise(function(rs, js) {
                 $("#check").hide();
                $("#indicator").show();

         Intercooler.triggerRequest($('#prova'), function (data) {
            console.log("ic-trigger",data);
            var resp = $.parseJSON(data);
            rs(resp);
          });
    })
}
if ($("#prova").length > 0 ) {
    bulmahead("prova", "prova-menu", api, function( item) {
        console.log("selected", item);
        $("input[name='client_id']").val(item.value);
        $("#prova-label").text(item.label);
        $("#check").show();
        if( $("#cars").length  > 0 ) {
            console.log("service"); 
        }

    },0);
}
