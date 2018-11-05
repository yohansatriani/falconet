jQuery(document).ready(function($){
            
    $.ajax({ 
        type: 'GET', 
        url: '/ajax/get_contacts_type/',
        dataType: 'json',
        success: function (data) {
            var option = "";
            $.each(data, function(index, element) {
                $.each(element, function(x, y) {
                    option=option+"<option value='"+y+"'>"+y.toUpperCase()+"</option>";
                    //console.log(y);
                });
                //console.log(element);
                //console.log(option);
            });
            
            //dmcelmn = dynamic element
            var dmcelmn = "<div class='form-group row dynamic-element'>"+
                        "<div class='col-sm-12'>"+
                        "<div class='input-group'>"+
                        "<select name='contact_type' id='select' class='col-sm-3 form-control'>"+
                        option+
                        "</select>"+
                        "<input type='text' name='contact_number[]' class='form-control'>"+
                        "<button type='button' class='delete btn btn-danger btn-sm'><i class='fa fa-times'></i></button>"+
                        "</div></div></div>";
            
            $('.add-one').click(function(){
                $(".dynamic-stuff").append(dmcelmn);
                attach_delete();
            });
                    
            //Attach functionality to delete buttons
            function attach_delete(){
                $('.delete').off();
                $('.delete').click(function(){
                    console.log("click");
                    $(this).closest('.form-group').remove();
                });
            }
        }
    });
    
    $('.delete-contact').click(function(){
        //console.log("click");
        $(this).parents().find('.is-deleted').val("1");
        //console.log("1");
        $(this).closest('.form-group').hide();
        //console.log("hide");           
    });
    
    $('#reset-contact').click(function(){
        $('#site-form').trigger("reset");
        $('#contact-form').trigger("reset");
    });
});