$(document).ready(function(){
    var next = 0;
    var today = new Date().toISOString().split('T')[0];
    function add_row(expense=None){
        var newIn = '<br id=br_' + next + '><input id="expense_' + next + '" placeholder="Expense Name" value="' + expense +'" type="text" name="items-' + next + '-expense"> \
        <input id="cost_' + next + '" placeholder="Cost" class="cost" type="text" name="items-' + next + '-cost" value=""> \
        <input id="due_date_' + next + '" type="date" name="items-' + next + '-due_date" value="2018-01-01"> \
        <select id="desc_' + next + '" type="text" name="items-' + next + '-desc"> \
            <option value="mutual">Mutual</option> \
            <option value="personal">Personal</option >';
        var del_row = $("[id^=del_row]").last();

        $(newIn).insertBefore(del_row);
        
        $("#desc_" + next).after('<button id="del_row_' + next + '" class="btn btn-secondary delete-row" type="button">-</button>');
        $('#due_date_' + next).val(today);
        next = next + 1;
        update_fields();
    }

    // default_fields
    if (default_fields){
        // remove the existing row
        $("[id^=cost]").remove();
        $("[id^=expense]").remove();
        $("[id^=due_date]").remove();
        $("[id^=desc]").remove();

        // Add rows per default fieds
        default_fields = default_fields.split(', ');
        $.each(default_fields, function(k, v){
            add_row(v);
        });
        update_fields();
        $("[id^=del_row_]").last().remove();
    }
    
    $(".add-more").click(function(){
        // e.preventDefault();
        var addto = $("[id^=desc_]").last();

        next = parseInt($(addto).last().attr('id').split("_")[1]) + 1;
        
        var newIn = '<br id=br_' + next + '><input id="expense_' + next + '" placeholder="Expense Name" type="text" name="items-' + next + '-expense"> \
                    <input id="cost_' + next + '" placeholder="Cost" class="cost" type="text" name="items-' + next + '-cost" value=""> \
                    <input id="due_date_' + next + '" type="date" name="items-' + next + '-due_date" value="2018-01-01"> \
                    <select id="desc_' + next + '" type="text" name="items-' + next + '-desc"> \
                        <option value="mutual">Mutual</option> \
                        <option value="personal">Personal</option >';
        var newInput = $(newIn);
        $(addto).after(newInput);

        var previous_row = next - 1;
        $("#desc_" + previous_row).after('<button id="del_row_' + previous_row + '" class="btn btn-secondary delete-row" type="button">-</button>');
        $('#due_date_' + next).val(today);

        //$('select').off('change');
        update_fields();

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
        $("[id^=desc]").each(function(){
            val = $(this).val();
            row_num = this.id.split("_")[1];
            
            if($.isNumeric(parseFloat($("#cost_" + row_num).val()))){
                value = parseFloat($("#cost_" + row_num).val());
            }else{
                value = 0;
            }

            if (val == "personal"){
                personal += value;
            }
            else if (val == "mutual"){
                mutual += value;
            }
       });
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
            var fields = ['expense', 'cost', 'due_date', 'desc', 'del_row', 'br'];
            var row = this.id.split('_')[2];
            var prev_row = row - 1;
            $.each(fields, function(idx, value){
                $("[id^=" + value + '_' + row + "]").remove();
            });
            // $("[id^=br_" + prev_row + "]").remove();
            update_fields();
        }
    });

    // Re-index All Fields
    function update_fields(){
        var fields = ['expense', 'cost', 'due_date', 'desc', 'del_row', 'br'];
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
