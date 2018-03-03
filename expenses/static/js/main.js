$(document).ready(function(){
    var next = 1;
    $(".add-more").click(function(e){
        e.preventDefault();
        var year = $('#year_' + next).val();
        var addto = $("#type_" + next);
        var prev_month = $("#month_" + next).val();

        next = next + 1;
        var newIn = '<br /><input id="expense_' + next + '" placeholder="Expense Name" + type="text" name="expense_name"> \
                    <input id="cost_' + next + '" placeholder="Cost" class="cost" type="text" name="cost" value=""> \
                    <select id="month_' + next + '" placeholder="Month"  type="text" name="month"> \
                        <option value="Jan">January</option> \
                        <option value="Feb">February</option > \
                        <option value="Mar">March</option> \
                        <option value="Apr">April</option> \
                        <option value="May">May</option> \
                        <option value="Jun">June</option> \
                        <option value="Jul">July</option > \
                        <option value="Aug">August</option> \
                        <option value="Sep">September</option> \
                        <option value="Oct">October</option> \
                        <option value="Nov">November</option> \
                        <option value="Dec">December</option> \
                    <input class="year" id="year_' + next + '" placeholder="Year"  type="text" value="' + year + '" name="year"> \
                    <select id="type_' + next + '" placeholder="Type"  type="text" name="type"> \
                        <option value="mutual">Mutual</option> \
                        <option value="personal#1">Personal #1</option > \
                        <option value="personal#2">Personal #2</option> \
                    <input type="hidden" name="count" class="count" value="' + next + '">';
        var newInput = $(newIn);
        $(addto).after(newInput);
        $('#month_' + next).val(prev_month);  // Sets the new value of the Month to the previous Month's value
        $("#year_" + next).attr('data-source',$(addto).attr('data-source'));

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
            $("[id^=type]").each(function(){
                val = $(this).val();
                row_num = this.id.split("_")[1];

                if ($("#cost_" + row_num).val().match(/^\d+$/)){

                    if (val == "personal#2"){
                        pay2 += parseFloat($("#cost_" + row_num).val());
                    }
                    else if (val == "personal#1"){
                        pay1 += parseFloat($("#cost_" + row_num).val());
                    }
                    else if (val == "mutual"){
                        mutual += parseFloat($("#cost_" + row_num).val());
                    }
                }
           });
           personals.push(pay1.toFixed(2), pay2.toFixed(2), mutual.toFixed(2));
           console.log(personals);
           return personals
        }
        $("select[name=type]").change(function(){
            totals = get_totals();
            edit_totals(totals);
        })

        $(".cost").focusout(function() {
            totals = get_totals();
            edit_totals(totals);
        })
    });

    $(function () {
    $("[id^=cost]").keyup(function(){
        if (!$(this).val().match(/^\d+$/)){
              $(this).css({ 'background': '#AA453C' });
            }
            else{
            $(this).css({ 'background': 'white' });
            }
        });
    });

});
