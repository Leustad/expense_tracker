$(document).ready(function(){
    var next = 0;
    var today = new Date().toISOString().split('T')[0];
    var fields = ['expense', 'cost', 'due_date', 'desc'];
    var expense_div = $('#all_expense_div');

    function add_row(v, next){
        console.log(v, next);
        var expense_row = $('<div id="row_expense_div_' + next + '"/>')

        var input_expense = $('<input placeholder="<Expense>" value="' + v + '" id="expense_' + next + '">')
        var input_cost = $('<input placeholder="Cost" id="cost_' + next + '">')
        var input_due_date = $('<input type="date" value="' + today + '" id="due_date_' + next + '">')
        var input_type = $('<select type="text" id="desc_' + next + '" name="items-' + next + '-desc">')
        var type_option1 = $('<option value="Mutual"/>').text('Mutual');
        var type_option2 = $('<option value="Personal" />').text('Personal');

        var del_row_btn = $('<button id="del_row_' + next + '" class="btn btn-secondary delete-row" type="button">-</button>');

        expense_row.append(input_expense);
        expense_row.append(input_cost);
        expense_row.append(input_due_date);
        expense_row.append(input_type);
        expense_row.append(del_row_btn);
        input_type.text("Mutual");

        expense_div.append(expense_row);
        input_type.append(type_option1);
        input_type.append(type_option2);
        input_expense.css({'font-weight': 'bold'});

        input_type.on('change', function(){
            edit_totals(get_totals())
        });
        input_cost.focusout(function() {
            edit_totals(get_totals())
        });
        next += 1;
    }

    // Default_fields
    if (default_fields){
        // remove the existing row
        $("[id^=cost]").remove();
        $("[id^=expense]").remove();
        $("[id^=due_date]").remove();
        $("[id^=desc]").remove();

        // Add rows per default fields
        default_fields = default_fields.split(', ');
        $.each(default_fields, function(k, v){
            add_row(v, next);
        });
        $("[id^=del_row_]").last().remove();
        $('.add-more').remove();
        $("[id^=row_expense_div_]").last().append($('<button id="add_row_btn" class="btn btn-info add-more" type="button">+</button>'));
        update_fields();
    }

    function delete_rows(value){
        if (value == 'all'){
            $('#all_expense_div').html('');
        }else{
            $("#row_expense_div_" + value).remove();
        }
    }


    // Change Template
    if (templates){
        var avail_templates = $('#avail_templates');
        $.each(templates, function(idx, value){
            var template_option = $('<option value="' + value + '" />');
            template_option.text(value);
            avail_templates.append(template_option)
        })
    };

    // Get Changed Template data
    $('#avail_templates').change(function () {
        var selected_template = this.value;
        $.ajax({
            url: "/get_template_data",
            type: "POST",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({'name': selected_template}),
            success: function (result) {
                var clone_add_row = $('#add_row_btn').clone(true, true);  //Therefore we keep the event handlers
                delete_rows('all');
                next = 0;
                $.each(result.split(', '), function(idx, value){
                    add_row(value, next);
                    next += 1;
                })
                clone_add_row.appendTo($("[id^=row_expense_div_]").last());
            },
            error: function (result) {
                console.log('Server error !! Can\'t Get Template Data');
            }
        });
    });

    // Add a new row
    $(".add-more").click(function(){
        // e.preventDefault();
        var last_item = $("[id^=del_row_]").last();
        console.log(parseInt(last_item.attr('id').split("_")[2]) + 1);
        next = parseInt(last_item.attr('id').split("_")[2]) + 1;

        add_row(v='', next);
        var clone_add_row = $('#add_row_btn').clone(true, true);  //Therefore we keep the event handlers
        $('#add_row_btn').remove();
        clone_add_row.appendTo($("[id^=row_expense_div_]").last());

        $('#desc_' + next).on('change', function(){
            edit_totals(get_totals());
        });
        $(".cost").focusout(function() {
            edit_totals(get_totals());
        })
    });

    function edit_totals(total){
        var mutual = $('.mutual');
        var perperson = $('.perperson');
        var personal = $('.personal');

        mutual.text("$ " + total[1]);
        perperson.text("$ " + (total[1]/2).toFixed(2));
        personal.text("$ " + total[0]);
    }
    function get_totals(){
        var expenses = [];
        var personal = 0;
        var mutual = 0;
        $("[id^=row_expense_div_]").each(function(){
        console.log('a');
            row_num = this.id.split("_")[3];
            val = $("#desc_" + row_num).val();
            
            if($.isNumeric(parseFloat($("#cost_" + row_num).val()))){
                value = parseFloat($("#cost_" + row_num).val());
            }else{
                value = 0;
            }

            if (val == "Personal"){
                personal += value;
            }
            else if (val == "Mutual"){
                mutual += value;
            }
       })
       expenses.push(personal.toFixed(2), mutual.toFixed(2));
       return expenses
    }
    $("select[id^=desc_]").change(function(){
        totals = get_totals();
        edit_totals(totals);
    });


    // Delete Selected Row and Re-index Fields
    $('form').on('click', '.delete-row', function(){
        if($("[id^=del_row]").length > 1){
            delete_rows($(this).attr('id').split("_")[2]);
            update_fields();
        }
    });

    // Re-index All Fields
    function update_fields(){
        var fields = ['row_expense_div', 'expense', 'cost', 'due_date', 'desc', 'del_row', 'br'];
        $.each(fields, function(idx, value){
            var ctr = 0;
            $("[id^=" + value + "]").each(function(index, el){
                $(this).attr('id', value + '_' + ctr);
               // $(this).off('focusout');
               // $(this).on('focusout', function(e){})
                ctr += 1;
            });
        });
        update_del_btn();
        edit_totals(get_totals());
        /*$('select').off('change');
        $('select').on('change', function(e){});*/
    }

    function update_del_btn(){
        $('.delete-row').off('click');
        $('.delete-row').on('click', function(e){});
    }
});
