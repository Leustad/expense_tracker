$(document).ready(function () {
    $('.history').addClass('active');
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
            let history_group1 = $('<div class="form-group col-lg-2"/>');
            let history_group2 = $('<div class="form-group col-lg-2"/>');
            let history_group3 = $('<div class="form-group col-lg-2"/>');
            let history_group4 = $('<div class="form-group col-lg-2"/>');
            let history_group5 = $('<div class="form-group col-lg-2"/>');
            let history_group6 = $('<div class="form-group col-lg-2"/>');


            let row_div = $('<div class="form-row" id="hist_row_' + value.id + '"/>')

            let input_id = $('<input class="form-control" type=hidden value="' + value.id + '" id="' + value.id + '">')
            let input_expense = $('<input class="form-control" value="' + value.expense + '" id="expense_' + value.id + '">')
            let input_cost = $('<input class="form-control" value="' + value.cost + '" id="cost_' + value.id + '">')
            let input_due_date = $('<input class="form-control" type="date" value="' + value.due_date + '" id="due_date_' + value.id + '">')
            let input_type = $('<input class="form-control" value="' + value.type + '" id="type_' + value.id + '">')
            let label = $('<label class="switch"/>')
            let input_checkbox = $('<input class="form-control" type="checkbox" id="checkbox_' + value.id + '">')
            let span_slider = $('<span class="slider"/>')
            let update_button = $('<button name="update" class="btn btn-primary update-button" type="button" style="display: none;" id="update_' + value.id + '"/>')
            let delete_button = $('<button name="delete" class="btn btn-outline-danger delete-button" type="button" style="display: none;" id="delete_' + value.id + '"/>')

            history_group1.append(input_expense);
            history_group2.append(input_cost);
            history_group3.append(input_due_date);
            history_group4.append(input_type);
            history_group5.append(label);
            history_group5.append(update_button);
            history_group6.append(delete_button);


            row_div.append(history_group1);
            row_div.append(history_group2);
            row_div.append(history_group3);
            row_div.append(history_group4);
            row_div.append(history_group5);
            row_div.append(history_group6);
            label.append(input_checkbox);
            label.append(span_slider);

            update_button.text('Update')
            delete_button.text('Delete')
            history_div.append(row_div);


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
                edit_totals(get_totals());
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

                edit_totals(get_totals());

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


    edit_totals(get_totals());

    function edit_totals(total){
        const mutual = $('.mutual');
        const perperson = $('.perperson');
        const personal = $('.personal');
        const g_total = $('.g_total');

        mutual.text("$ " + total[1].toFixed(2));
        perperson.text("$ " + (total[1]/2).toFixed(2));
        personal.text("$ " + total[0].toFixed(2));
        g_total.text("$ " + (total[1] + total[0]).toFixed(2));
    }

    function get_totals(){
        let expenses = [];
        var personal = 0.0;
        var mutual = 0.0;
        $("[id^=cost_]").each(function(){
            row_num = this.id.split("_")[1];
            desc = $("#type_" + row_num).val();

            var val = $(this).val();
            var amount = parseFloat(val);

            if (desc == "Personal"){
                personal += amount;
            }
            else if (desc == "Mutual"){
                mutual += amount;
            }
       })
       expenses.push(personal, mutual);
       return expenses
    }

});