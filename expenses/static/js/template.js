$(document).ready(function(){
    $('.template').addClass('active');
    $("select[name=update_template_name]").change(function(){
        // AJAX: ON Template name Change for Update Template form
        // Query the db to get the template fields.
        $.ajax({
            url: '/get_template_fields',
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'template_name': $("#update_template_name").val()
            }),
            success: function(response){
                $('#update_template_fields').val(response.fields)
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});