$(document).ready(function(){
    var next = 1;
    $(".add-more").click(function(e){
        e.preventDefault();
        var year = $('#year_' + next).val();
        var addto = $("#year_" + next);
        next = next + 1;
        console.log(next);
        var newIn = '<br /><input id="expense_' + next + '" placeholder="Expense Name" + type="text"> \
                    <input id="cost_' + next + '" placeholder="Cost"  type="text"> \
                    <select id="month_' + next + '" placeholder="Month"  type="text"> \
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
                    <input id="year_' + next + '" placeholder="Year"  type="text" value="' + year + '"> \
                    <input type="hidden" name="count" class="count" value="' + next + '">';
        var newInput = $(newIn);
        $(addto).after(newInput);
        $("#year_" + next).attr('data-source',$(addto).attr('data-source'));
        
    });
});
