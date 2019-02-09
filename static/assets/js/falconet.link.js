jQuery(document).ready(function($){
    $( "#datepicker" ).datepicker({inline: true, dateFormat: "yy-mm-dd"});

    // GENERATE LINK NAME
    $( '#sites1, #isp' ).on('change', function(){
        var sites_select = document.getElementById("sites1");
        var sites_text = sites_select.options[sites_select.selectedIndex].text;

        var isp_select = document.getElementById("isp");
        var isp_text = isp_select.options[isp_select.selectedIndex].text;

        $('#links_name').val(sites_text+"-"+isp_text);
    })
});
