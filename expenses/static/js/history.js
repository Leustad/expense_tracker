$(document).ready(function () {
    var data = hist_data;
    var fields = ['expense', 'cost', 'due_date', 'type'];
    var history_div = $("#history_data");
    var data_to_draw_with = all_data;

    let default_graph_type = $("input[name='graph_type']:checked").val();

    function sanitize(data) {
        var output = data.replace(/<script[^>]*?>.*?<\/script>/gi, '').
        replace(/<[\/\!]*?[^<>]*?>/gi, '').
        replace(/<style[^>]*?>.*?<\/style>/gi, '').
        replace(/<![\s\S]*?--[ \t\n\r]*>/gi, '');
        return output;
    }

    $('input:radio[name="graph_type"]').change(
        function(){
            let graph_type = $(this).val();
            if( graph_type != default_graph_type){
                draw_hist_graph(data_to_draw_with, graph_type);
                default_graph_type = graph_type;
            }
        })

    populate_history(data);

    function populate_history(hist_data) {
        current_data = {};
        $.each(hist_data, function (idx, value) {
            let row_div = $('<div id="hist_row_' + value.id + '"/>')
            let input_id = $('<input type=hidden value="' + value.id + '" id="' + value.id + '">')
            let input_expense = $('<input value="' + value.expense + '" id="expense_' + value.id + '">')
            let input_cost = $('<input value="' + value.cost + '" id="cost_' + value.id + '">')
            let input_due_date = $('<input type="date" value="' + value.due_date + '" id="due_date_' + value.id + '">')
            let input_type = $('<input value="' + value.type + '" id="type_' + value.id + '">')
            let label = $('<label class="switch"/>')
            let input_checkbox = $('<input type="checkbox" id="checkbox_' + value.id + '">')
            let span_slider = $('<span class="slider"/>')
            let update_button = $('<button name="update" type="button" style="display: none;" id="update_' + value.id + '"/>')
            let delete_button = $('<button name="delete" type="button" style="display: none;" id="delete_' + value.id + '"/>')

            row_div.append(input_id);
            row_div.append(input_expense);
            row_div.append(input_cost);
            row_div.append(input_due_date);
            row_div.append(input_type);
            label.append(input_checkbox);
            label.append(span_slider);
            row_div.append(label);
            row_div.append(update_button);
            row_div.append(delete_button);
            update_button.text('<< Update')
            delete_button.text('X Delete')
            history_div.append(row_div);
            // history_div.append('<br>');


            $("#delete_" + value.id).click(function (e) {
                e.preventDefault();
                let delete_id = $(this).attr('id').split('_')[1]
                delete_row(delete_id);
            });

            $("#update_" + value.id).click(function (e) {
                let message = '';
                e.preventDefault();
                let update_id = $(this).attr('id').split('_')[1]
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
                $('#delete_' + id_value).css("display", "inline");
            } else {
                toggle_row(id_value, true);
                $('#update_' + id_value).css("display", "none");
                $('#delete_' + id_value).css("display", "none");
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

    // Empty out the history page
    function clear_rows() {
        $('#history_data').empty();
    };

    // Get the new history data per passed-in dates
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
                populate_history(result.hist_data);
                data_to_draw_with = result.graph_yty_data;
                draw_hist_graph(result.graph_yty_data);
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
            data: JSON.stringify({
                'to_date': $('#to_date').val(),
                'from_date': $('#from_date').val(),
                'update_data': update_data
            }),
            success: function (result) {
                $('#update_' + update_data['update_id']).css("display", "none");
                $('#delete_' + update_data['update_id']).css("display", "none");
                toggle_row(update_data['update_id'], true);
                $('#checkbox_' + update_data['update_id']).prop('checked', false);
                $('#hist_row_' + update_data['update_id']).animate({backgroundColor: '#2196F3'}, 'slow');
                $('#hist_row_' + update_data['update_id']).animate({backgroundColor: 'white'}, 'slow');

                setTimeout(function() {
                    clear_rows();
                    populate_history(result.hist_data);
                    console.log(result.hist_data);
                    // Re-Draw the graph
                    data_to_draw_with = result.graph_yty_data;
                    draw_hist_graph(data_to_draw_with);
                  }, 1000);
            },
            error: function (result) {
                alert('Server error !!');
            }
        });
    }

    function delete_row(delete_id){
        $('#hist_row_' + delete_id).animate({backgroundColor: 'red'}, 'slow');
        $('#hist_row_' + delete_id).animate({backgroundColor: 'white'}, 'slow');
        $.ajax({
            url: "/delete_hist_row",
            type: "POST",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'to_date': $('#to_date').val(),
                'from_date': $('#from_date').val(),
                'row_id': delete_id
            }),
            success: function (result) {
                setTimeout(function() {
                    clear_rows();
                    populate_history(result.hist_data);
                    // Re-Draw the graph
                    data_to_draw_with = result.graph_yty_data
                    draw_hist_graph(data_to_draw_with);
                  }, 1000);
            },
            error: function (result) {
                alert('Server error !!');
            }
        });
    };

});