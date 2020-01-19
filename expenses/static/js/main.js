$(document).ready(function(){
    $('.home').addClass('active');
    var next = 0;
    const today = new Date().toISOString().split('T')[0];
    const fields = ['expense', 'cost', 'due_date', 'desc'];
    const form_anchor = $('.form_anchor');

    function add_row(v, next){

        let form_row = $('<div class="row" id=row_expense_div_' + next + '/>');
        let form_group1 = $('<div class="form-group col-lg-2"/>');
        let form_group2 = $('<div class="form-group col-lg-2"/>');
        let form_group3 = $('<div class="form-group col-lg-3"/>');
        let form_group4 = $('<div class="form-group col-lg-2"/>');
        let form_group5 = $('<div class="form-group col-lg-1"/>');
        let form_group6 = $('<div class="form-group col-lg-2"/>');

        let input_expense = $('<input class="form-control" placeholder="<Expense>" name="items-' + next + '-expense" value="' + v + '" id="expense_' + next + '">')
        let input_cost = $('<input class="form-control" placeholder="Cost" name="items-' + next + '-cost" value="" id="cost_' + next + '">')
        let input_due_date = $('<input class="form-control" type="date" name="items-' + next + '-due_date" value="' + today + '" id="due_date_' + next + '">')
        let input_type = $('<select class="form-control" type="text" id="desc_' + next + '" name="items-' + next + '-desc">')
        let type_option1 = $('<option value="Mutual"/>').text('Mutual');
        let type_option2 = $('<option value="Personal" />').text('Personal');

        let del_row_btn = $('<button id="del_row_' + next + '" class="btn btn-outline-danger delete-row" type="button">-</button>');

        form_group1.append(input_expense);
        form_row.append(form_group1);
        form_anchor.append(form_row);

        form_group2.append(input_cost);
        form_row.append(form_group2);
        form_anchor.append(form_row);

        form_group3.append(input_due_date);
        form_row.append(form_group3);
        form_anchor.append(form_row);

        form_group4.append(input_type);
        form_row.append(form_group4);
        form_anchor.append(form_row);

        form_group5.append(del_row_btn);
        form_row.append(form_group5);
        form_anchor.append(form_row);

        form_group5.append("");
        form_row.append(form_group6);
        form_anchor.append(form_row);

        input_type.text("Mutual");


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
        $('.form_anchor div.row').remove();

        // Add rows per default fields
        default_fields = default_fields.split(', ');
        $.each(default_fields, function(k, v){
            add_row(v, next);
            next += 1;
        });
        $('.add-more').remove();
        $('.col-lg-2').last().append($('<button id="add_row_btn" class="btn btn-primary add-more" type="button">+</button>'));
        update_fields();
    }

    function delete_rows(value){
        if (value == 'all'){
            $('.form_anchor .row').remove();
        }else{
            $("#row_expense_div_" + value).remove();
        }
    }


    // Change Template
    if (templates){
        let avail_templates = $('#avail_templates');
        let temp = $('<button class="dropdown-item list_template" type="button"/>');
        temp.text('None');
        $(avail_templates).append(temp);

        $.each(templates, function(idx, value){
            let template_option = $('<button class="dropdown-item list_template" type="button"/>');
            template_option.text(value);
            $(avail_templates).append(template_option)
        })
        // Set selected template name to the default template name
        $('#avail_templates').val(default_template_name);
    }else{
        let template_option = $('<button class="dropdown-item list_template" type="button"/>');
        template_option.text('None');
        avail_templates.append(template_option)
    };
    
    // Get Changed Template data
    $('.list_template').click(function () {
        let selected_template = $(this).text();
        console.log(selected_template);
        let clone_add_row = $('#add_row_btn').clone(true, true);  //Therefore we keep the event handlers
        if (selected_template === 'None') {
            delete_rows('all');
            next = 0;
            add_row('', next);
            clone_add_row.appendTo($('.col-lg-2').last());
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
                    clone_add_row.appendTo($('.col-lg-2').last());
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
        clone_add_row.appendTo($('.col-lg-2').last());

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
        const g_total = $('.g_total');

        mutual.text("$ " + total[1].toFixed(2));
        perperson.text("$ " + (total[1]/2).toFixed(2));
        personal.text("$ " + total[0].toFixed(2));
        g_total.text("$ " + (total[1] + total[0]).toFixed(2));
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
       expenses.push(personal, mutual);
       return expenses
    }
    $("select[id^=desc_]").change(function(){
        totals = get_totals();
        edit_totals(totals);
    });


    // Delete Selected Row and Re-index Fields
    $('form').on('click', '.delete-row', function(){
        let clone_add_row = $('#add_row_btn').clone(true, true);
        $('#add_row_btn').remove();
        if($("[id^=del_row]").length > 1){
            delete_rows($(this).attr('id').split("_")[2]);
            update_fields();
        }
        clone_add_row.appendTo($('.col-lg-2').last());
    });

    // Re-index All Fields
    function update_fields(){
        const re_index_fields = ['row_expense_div', 'expense', 'cost', 'due_date', 'desc', 'del_row', 'br'];
        $.each(re_index_fields, function(idx, value){
            let ctr = 0;
            $("[id^=" + value + "]").each(function(index, el){
                $(this).attr('id', value + '_' + ctr);
                ctr += 1;
            });
        });
        update_del_btn();
        edit_totals(get_totals());
    }

    function update_del_btn(){
        $('.delete-row').off('click');
        $('.delete-row').on('click', function(e){});
    }
});
