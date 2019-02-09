jQuery(document).ready(function($){
    $( "#start_datetimepicker" ).datetimepicker({
        dateFormat: "yy-mm-dd",
        timeFormat: "HH:mm",
        controlType: 'select',
        oneLine: true
    });
    $( "#end_datetimepicker" ).datetimepicker({
        dateFormat: "yy-mm-dd",
        timeFormat: "HH:mm",
        controlType: 'select',
        oneLine: true
    });
});
