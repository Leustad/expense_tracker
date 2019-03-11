$(document).ready(function(){
    var MONTHS = ["January", "February", "March", "April", "May", "June"];

    function getRandomColor() {
      var letters = '0123456789ABCDEF';
      var color = '#';
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }
    
    
    var config = {
        type: 'line',
        data: {
            datasets: [],
        },
      options: {
        responsive: true,
        title:{
          display:true,
          text:'Yearly Expenses'
        },
        tooltips: {
          mode: 'index',
          intersect: false,
        },
       hover: {
          mode: 'nearest',
          intersect: true
        },
        scales: {
          xAxes: [{
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Month'
            }
          }],
          yAxes: [{
            display: true,
            scaleLabel: {
              display: true,
            },
          }]
        }
      }
    };
    
    var dates = []
    var fields = []
    var cost_per_field = {}
    
    $.each(data, function(key, value){
        // Get Dates
        dates.push([key.slice(4, 6), key.slice(6, 8), key.slice(0, 4)].join(' / '));
        $.each(value, function(k, v){
            fields.push(v['expense'])
        })
    });
    
    //Make a unique expense field
    $.unique(fields.sort());
    
    function check_value(value, field_name){
        var cost = 0;
        $.each(value, function(k, v){
            if(v.expense == field_name){
                cost = v.cost;
                return false;
            }
        })
        return cost;
    }
    
    // iterate over data per @field and get the @cost per date
    $.each(fields, function(k, v){
        cost_per_field[v] = [];
        cost = 0;
        $.each(data, function(date, val){
            cost = check_value(val, v)
            if (cost != 0){
                cost_per_field[v].push(cost)
            }else{
                cost_per_field[v].push(0)
            }
    
        })
    });
    
    config.data['labels'] = dates;
    $.each(cost_per_field, function(key, value){
        color = getRandomColor();
        config.data.datasets.push({
            label: key,
            data: value,
            backgroundColor: color,
            borderColor: color,
            borderWidth: 3,
            fill: false
        })
    });
    
    var myLine = new Chart(ctx, config);
})
