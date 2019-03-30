$(document).ready(function(){
    var next = 0;
    const today = new Date().toISOString().split('T')[0];
    const fields = ['expense', 'cost', 'due_date', 'desc'];
    const expense_div = $('#all_expense_div');

    function add_row(v, next){
        const expense_row = $('<div id="row_expense_div_' + next + '"/>')

        let input_expense = $('<input placeholder="<Expense>" name="items-' + next + '-expense" value="' + v + '" id="expense_' + next + '">')
        let input_cost = $('<input placeholder="Cost" name="items-' + next + '-cost" value="" id="cost_' + next + '">')
        let input_due_date = $('<input type="date" name="items-' + next + '-due-date" value="' + today + '" id="due_date_' + next + '">')
        let input_type = $('<select type="text" id="desc_' + next + '" name="items-' + next + '-desc">')
        let type_option1 = $('<option value="Mutual"/>').text('Mutual');
        let type_option2 = $('<option value="Personal" />').text('Personal');

        let del_row_btn = $('<button id="del_row_' + next + '" class="btn btn-secondary delete-row" type="button">-</button>');

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
            next += 1;
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
        let avail_templates = $('#avail_templates');
        let temp = $('<option value="None"/>');
        temp.text('None')
        avail_templates.append(temp);

        $.each(templates, function(idx, value){
            let template_option = $('<option value="' + value + '" />');
            template_option.text(value);
            avail_templates.append(template_option)
        })
        // Set selected template name to the defaul template name
        $('#avail_templates').val(default_template_name);
    }else{
        let template_option = $('<option value="None"/>');
        template_option.text('None');
        avail_templates.append(template_option)
    };
    
    // Get Changed Template data
    $('#avail_templates').change(function () {
        let selected_template = this.value;
        let clone_add_row = $('#add_row_btn').clone(true, true);  //Therefore we keep the event handlers
        if (selected_template === 'None') {
            delete_rows('all');
            next = 0;
            add_row('', next);
            clone_add_row.appendTo($("[id^=row_expense_div_]").last());
        }else{
            $.ajax({
                url: "/get_template_data",
                type: "POST",
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify({'name': selected_template}),
                success: function (result) {
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
        }

    });

    // Add a new row
    $(".add-more").click(function(){
        // e.preventDefault();
        let last_item = $("[id^=del_row_]").last();
        next = parseInt(last_item.attr('id').split("_")[2]) + 1;

        add_row(v='', next);
        let clone_add_row = $('#add_row_btn').clone(true, true);  //Therefore we keep the event handlers
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
        const mutual = $('.mutual');
        const perperson = $('.perperson');
        const personal = $('.personal');

        mutual.text("$ " + total[1]);
        perperson.text("$ " + (total[1]/2).toFixed(2));
        personal.text("$ " + total[0]);
    }
    function get_totals(){
        let expenses = [];
        let personal = 0;
        let mutual = 0;
        $("[id^=row_expense_div_]").each(function(){
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
        const re_index_fields = ['row_expense_div', 'expense', 'cost', 'due-date', 'desc', 'del_row', 'br'];
        $.each(re_index_fields, function(idx, value){
            let ctr = 0;
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
