import '@fortawesome/fontawesome-free/js/all.js';
require("bulmahead/src/bulmahead.js");


function api(value) {
    return new Promise(function(rs, js) {
        $("#check").hide();
        $("#indicator").show();

         Intercooler.triggerRequest($('#prova'), function (data) {
            //console.log("ic-trigger",data);
            var resp = $.parseJSON(data);
            rs(resp);
          });
    })
}
if ($("#prova").length > 0 ) {
    bulmahead("prova", "prova-menu", api, function( item) {
        $("[name='client_id']").val(item.value);
        $("#prova-label").text(item.label);
        $("#check").show();
            if ($("[name='client_id']").attr("ic-get-from")) {
                Intercooler.refresh($("[name='client_id']"));
            }
            
     

    },0);
}
