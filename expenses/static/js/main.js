$(document).ready(function(){
    var next = 0;
    $(".add-more").click(function(){
        // e.preventDefault();
        var addto = $("#desc_" + next);

        next = next + 1;
        var today = new Date().toISOString().split('T')[0]
        var newIn = '<br id=br_' + next + '><input id="expense_' + next + '" placeholder="Expense Name" type="text" name="items-' + next + '-expense"> \
                    <input id="cost_' + next + '" placeholder="Cost" class="cost" type="text" name="items-' + next + '-cost" value=""> \
                    <input id="due_date_' + next + '" type="date" name="items-' + next + '-due_date" value="2018-01-01"> \
                    <select id="desc_' + next + '" type="text" name="items-' + next + '-desc"> \
                        <option value="mutual">Mutual</option> \
                        <option value="personal#1">Personal #1</option > \
                        <option value="personal#2">Personal #2</option>';
        var newInput = $(newIn);
        $(addto).after(newInput);

        var previous_row = next - 1;
        $("#desc_" + previous_row).after('<button id="del_row_' + previous_row + '" class="btn btn-secondary delete-row" type="button">-</button>');
        $('#due_date_' + next).val(today);

        update_fields();
        function edit_totals(total){
            var mutual = $('.mutual');
            var perperson = $('.perperson');
            var personalNumbOne = $('.paycheck1');
            var personalNumbTwo = $('.paycheck2');

            mutual.text("$ " + total[2]);
            perperson.text("$ " + (total[2]/2).toFixed(2));
            personalNumbOne.text("$ " + parseFloat(total[0]).toFixed(2));
            personalNumbTwo.text("$ " + parseFloat(total[1]).toFixed(2));

        }
        function get_totals(){
            var personals = [];
            var pay1 = 0;
            var pay2 = 0;
            var mutual = 0;
            $("[id^=desc]").each(function(){
                val = $(this).val();
                row_num = this.id.split("_")[1];

                if (val == "personal#2"){
                    pay2 += parseFloat($("#cost_" + row_num).val());
                }
                else if (val == "personal#1"){
                    pay1 += parseFloat($("#cost_" + row_num).val());
                }
                else if (val == "mutual"){
                    mutual += parseFloat($("#cost_" + row_num).val());
                }
           });
           personals.push(pay1.toFixed(2), pay2.toFixed(2), mutual.toFixed(2));
           return personals
        }
        $("select[name=desc]").change(function(){
            totals = get_totals();
            edit_totals(totals);
        })

        $(".cost").focusout(function() {
            totals = get_totals();
            edit_totals(totals);
        })
    });

    // Delete Selected Row and Re-index Fields
    $('.delete-row').on('click', function(){
        var fields = ['expense', 'cost', 'due_date', 'desc', 'del_row', 'br'];
        var row = this.id.split('_')[2];
        var prev_row = row - 1;
        console.log(prev_row);
        $.each(fields, function(idx, value){
            $("[id^=" + value + '_' + row + "]").remove();
        });
        $("[id^=br_" + prev_row + "]").remove();
        update_fields();
    });

    // Re-index All Fields
    function update_fields(){
        var fields = ['expense', 'cost', 'due_date', 'desc', 'del_row', 'br'];
        $.each(fields, function(idx, value){
            var ctr = 1;
            $("[id^=" + value + "]").each(function(index, el){
                $(this).attr('id', value + '_' + ctr);
                ctr += 1;
            });
        });
        update_del_btn();
    }

    function update_del_btn(){
        $('.delete-row').off('click');
        $('.delete-row').on('click', function(e){});
    }
});
