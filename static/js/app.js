url = window.location.href.split('/')

if (url[4] !== undefined ) {
    $('#firstYear').val(url[4])
    $('#lastYear').val(url[5])
}

function graph(title, vertical, horizontal) {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(function(){ drawChart(title, vertical, horizontal) });
}

function drawChart(title, vertical, horizontal) {
    let jsonData = $('#curveData').data('chart');
    if (Object.keys(jsonData).length === 0) {
        jsonData = [1906, 0, 0]
    }

    let data = new google.visualization.DataTable();
        data.addColumn('number', 'x');
        data.addColumn('number', 'ysmooth');
        data.addColumn('number', 'y');

        jsonData.forEach(function(element, index) {
            data.addRow([jsonData[index][0], jsonData[index][1], jsonData[index][2]])
        })

    let options = {
        title: title,
        curveType: 'function',
        vAxis: { title: vertical },
        hAxis: { title: horizontal},
        legend: { position: 'bottom' }
    };

    let chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

    chart.draw(data, options);
}

if ($('#curve_chart').length > 0) {
    graph($('#graph-title').val(), $('#graph-vertical').val(), $('#graph-horizontal').val())
}
