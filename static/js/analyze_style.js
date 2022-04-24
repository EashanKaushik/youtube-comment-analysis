
// Create the chart
Highcharts.chart('sentiment', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Sentiment Analysis'
    },
    subtitle: {
        text: ''
    },
    accessibility: {
        announceNewData: {
            enabled: true
        }
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        title: {
            text: 'Total percent comment sentiment'
        }

    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y:.1f}%'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
    },

    series: [
        {
            name: "Browsers",
            colorByPoint: true,
            data: [
                {
                    name: "Positive",
                    y: _positve
                },
                {
                    name: "Neutral",
                    y: _neutral
                },
                {
                    name: "Negative",
                    y: _negative
                },
            ]
        }
    ]
});