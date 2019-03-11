$(document).ready(function () {
    var data = hist_data;
    var fields = ['expense', 'cost', 'due_date', 'type'];
    var history_div = $("#history");

    function sanitize(data) {
        var output = data.replace(/<script[^>]*?>.*?<\/script>/gi, '').
        replace(/<[\/\!]*?[^<>]*?>/gi, '').
        replace(/<style[^>]*?>.*?<\/style>/gi, '').
        replace(/<![\s\S]*?--[ \t\n\r]*>/gi, '');
        return output;
    }

    populate_history(data);

    function populate_history(hist_data) {
        current_data = {};
        $.each(hist_data, function (idx, value) {
            var row_div = $('<div id="hist_row_' + value.id + '"/>')
            var input_id = $('<input type=hidden value="' + value.id + '" id="' + value.id + '">')
            var input_expense = $('<input value="' + value.expense + '" id="expense_' + value.id + '">')
            var input_cost = $('<input value="' + value.cost + '" id="cost_' + value.id + '">')
            var input_due_date = $('<input type="date" value="' + value.due_date + '" id="due_date_' + value.id + '">')
            var input_type = $('<input value="' + value.type + '" id="type_' + value.id + '">')
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


            $("#update_" + value.id).click(function (e) {
                var message = '';
                e.preventDefault();
                var update_id = $(this).attr('id').split('_')[1]
                $.each(fields, function (idx, value) {
                    if ($("[id^=" + value + '_' + update_id + "]").val() != current_data[update_id][value]) {
                        update_data = {
                            'update_id': sanitize(update_id),
                            'expense': sanitize($('#expense_' + update_id).val()),
                            'cost': sanitize($('#cost_' + update_id).val()),
                            'due_date': sanitize($('#due_date_' + update_id).val()),
                            'type': sanitize($('#type_' + update_id).val())
                        }
                        update_row(update_data);
                    } else {
                        message = 'No Difference Detected !'
                    }
                });
            });

            // Save currently displayed data to check 
            // against if there is an update
            var row_id = value.id;
            current_data[row_id] = {
                'expense': value.expense,
                'cost': value.cost,
                'due_date': value.due_date,
                'type': value.type
            }
        });

        // Disable all fields at the beginning
        $.each(fields, function (idx, value) {
            $("[id^=" + value + "]").each(function (index, el) {
                $(this).attr('disabled', true)
            })
        });

        // Disable and Enable the Update button
        $('[id^=checkbox_]').click(function () {
            var id_value = $(this).attr('id').split("_")[1];
            if ($(this).is(':checked')) {
                toggle_row(id_value, false);
                $('#update_' + id_value).css("display", "inline");
            } else {
                toggle_row(id_value, true);
                $('#update_' + id_value).css("display", "none");
            }
        });
    }

    // Disable / Enable rows
    function toggle_row(id_value, disable) {
        $.each(fields, function (idx, value) {
            $("[id^=" + value + '_' + id_value + "]").each(function (index, el) {
                $(this).attr('disabled', disable)
            });
        })
    }

    // Emply out the history page
    function clear_rows() {
        $('#history').empty();
    };

    // Get the new history data per passed in dates
    $("#hist_btn").click(function (e) {
        e.preventDefault();
        $.ajax({
            url: "/get_history",
            type: "POST",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'to_date': $('#to_date').val(),
                'from_date': $('#from_date').val()
            }),
            success: function (result) {
                clear_rows();
                populate_history(result);
            },
            error: function (result) {
                console.log('Server error !! Can\'t get the history data');
            }
        });
    });

    // Update row and disable it    
    function update_row(update_data) {
        $.ajax({
            url: "/update_history_row",
            type: "POST",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(update_data),
            success: function (result) {
                $('#update_' + update_data['update_id']).css("display", "none");
                toggle_row(update_data['update_id'], true);
                $('#checkbox_' + update_data['update_id']).prop('checked', false);
                $('#hist_row_' + update_data['update_id']).animate({backgroundColor: '#2196F3'}, 'slow');
                $('#hist_row_' + update_data['update_id']).animate({backgroundColor: 'white'}, 'slow');
            },
            error: function (result) {
                alert('Server error !!');
            }
        });
    }

});