$(document).ready(function(){
    var data = hist_data;
    var fields = ['expense_', 'cost_', 'due_date_', 'type_'];
    var history_div = $("#history");

    populate_history(data);

    function populate_history(hist_data){
        $.each(hist_data, function(idx, value){
            var row_div = $('<div id=hist_row_"' + value.id + '"/>')
            var input_id = $('<input type=hidden value="' + value.id + '" id="' + value.id +'">')
            var input_expense = $('<input value="' + value.expense + '" id="expense_' + value.id +'">')
            var input_cost = $('<input value="' + value.cost + '" id="cost_' + value.id + '">')
            var input_due_date = $('<input type="date" value="' + value.due_date + '" id="due_date_' + value.id +'">')
            var input_type = $('<input value="' + value.type + '" id="type_' + value.id+ '">')
            var label = $('<label class="switch"/>')
            var input_checkbox = $('<input type="checkbox" id="checkbox_' + value.id + '">')
            var span_slider = $('<span class="slider"/>')
            var update_button = $('<button name="update" type="button" style="display: none;" id="update_' + value.id + '"/>')
    
            row_div.append(input_id);
            row_div.append(input_expense);
            row_div.append(input_cost);
            row_div.append(input_due_date);
            row_div.append(input_type);
            label.append(input_checkbox);
            label.append(span_slider);
            row_div.append(label);
            row_div.append(update_button);
            update_button.text('Update')
            history_div.append(row_div);
            history_div.append('<br>');
        });
    
        // Disable all fields at the beginning
        $.each(fields, function(idx, value){
            $("[id^=" + value + "]").each(function(index, el){
                $(this).attr('disabled', true)
            })
        });
    
        // Disable and Enable the Update button
        $('[id^=checkbox_]').click(function(){
            var id_value = $(this).attr('id').split("_")[1];   
            if($(this).is(':checked')){
                $.each(fields, function(idx, value){
                    $("[id^=" + value + id_value + "]").each(function(index, el){
                        $(this).attr('disabled', false)
                    })
                });
                $('#update_' + id_value).css("display", "inline");
            }else{
                $.each(fields, function(idx, value){
                    $("[id^=" + value + id_value + "]").each(function(index, el){
                        $(this).attr('disabled', true)
                    })
                });
                $('#update_' + id_value).css("display", "none");
            }
        });
    }
    
    // Emply out the history page
    function clear_rows(){
        $('#history').empty();
    };

    // Get the new history data per passed in dates
    $("#hist_btn").click(function(e) {
        e.preventDefault();
        $.ajax({
            url: "/get_history",
            type: "POST",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({ 
                'to_date': $('#to_date').val(),
                'from_date': $('#from_date').val()
            }),
            success: function(result) {
                clear_rows();
                populate_history(result)
            },
            error: function(result) {
                alert('Server error !!');
            }
        });
    });
});
