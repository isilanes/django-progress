var ctx = document.getElementById('item_chart').getContext('2d');
Chart.defaults.global.elements.line.fill = false;
Chart.defaults.global.legend.display = true;
Chart.defaults.global.animation.duration = 500;

$(document).ready(function() {
    var dataUrl = $('#data-url').attr("data-name");
    $.get(dataUrl, function(data) {
        dataset = {
            //label: data.label,
            label: "Autonomía",
            borderColor: data.color,
            data: data.data,
        }
        chart.data.datasets.push(dataset)

        chart.update()
    });
});

var chart = new Chart(ctx, {
    // The type of chart we want to create:
    type: 'line',
    
    // The data for our dataset (begins empty):
    data: {
        datasets: []
    },
    
    // Configuration options go here:
    options: {
        scales: {
            xAxes: [
                {
                    type: "linear",
                    position: 'bottom',
                    scaleLabel: {
                       display: true,
                       labelString: "# de repostaje",
                    }
                }
            ],
            yAxes: [
                {
                    scaleLabel: {
                        display: true,
                        labelString: "km/repostaje",
                    }
                }
            ]
        }
    }
});
