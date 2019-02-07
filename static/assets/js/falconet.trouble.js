jQuery(document).ready(function($){
    $( "#start_datetimepicker" ).datetimepicker({
        dateFormat: "yy-mm-dd",
        controlType: 'select',
        oneLine: true
    });
    $( "#end_datetimepicker" ).datetimepicker({
        dateFormat: "yy-mm-dd",
        controlType: 'select',
        oneLine: true
    });
});
