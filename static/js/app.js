let sensors = $('#sensors');
let sensor = $('#sensor');
let utrechtRows = sensors.data('sensors');

function displayFloat(value) {
    if (value !== 0) {
        return (Math.round(value * 10) / 10).toFixed(1);
    } else {
        return 'N/B';
    }
}

sensorsArray = []
utrechtRows.forEach((index) => {
    let date = index[0];
    date = new Date(date + ' UTC').toLocaleString();
    let temperature = index[2];
    let humidity = index[5];
    let pm25 = index[9];
    let pm10 = index[10];
    let sourceImage;
    let timestamps = $('#sensor-' + index[1] + '-timestamps');
    if ($('#pm:checked').length === 1 && index[19] === '0') {
        return;
    }
    if ($('#inactive:checked').length === 0 && timestamps.length === 0) {
        return;
    }
    if (timestamps.length === 0) {
        sourceImage = '/static/img/sensor-red.png'
    } else {
        sourceImage = '/static/img/sensor-green.png'
    }
    let sensor = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([index[13], index[14]])),
        id: index[1],
        longitude: index[13],
        latitude: index[14],
        name: '<p class="sensor-title">Sensor ' + index[1] + '</p>' +
            '<p>' + date + '</p>' +
            '<p>Temperatuur: ' + displayFloat(temperature) + ' °C</p>' +
            '<p>Luchtvochtigheid: ' + displayFloat(humidity) + ' RV %</p>' +
            '<p>Fijnstof 2.5: ' + displayFloat(pm25) + ' µg/m³</p>' +
            '<p>Fijnstof 10: ' + displayFloat(pm10) + ' µg/m³</p>',
    });
    sensor.setStyle(
        new ol.style.Style({
            image: new ol.style.Icon({
                crossOrigin: 'anonymous',
                src: sourceImage,
                width: 30,
                height: 30,
            }),
        }),
    );
    sensorsArray.push(sensor)
});

const vectorSource = new ol.source.Vector({
    features: sensorsArray,
});

const vectorLayer = new ol.layer.Vector({
    source: vectorSource,
});

const map = new ol.Map({
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM(),
        }),
        vectorLayer
    ],
    target: document.getElementById('map'),
    view: new ol.View({

        center: ol.proj.fromLonLat([5.11, 52.1]),
        zoom: 12.5,
    }),
});

const element = document.getElementById('popup');

const popup = new ol.Overlay({
    element: element,
    positioning: 'bottom-center',
    stopEvent: false,
});
map.addOverlay(popup);

let popover;
function disposePopover() {
    if (popover) {
        popover.dispose();
        popover = undefined;
    }
}
// display popup on click
map.on('click', function (evt) {
    if (popupIcon(evt)) {
        sensor.val()
    }
});

// change mouse cursor when over marker
map.on('pointermove', function (e) {
    const hit = map.hasFeatureAtPixel(e.pixel);
    map.getTargetElement().style.cursor = hit ? 'pointer' : '';
});
// Close the popup when the map is moved
map.on('movestart', disposePopover);

function popupIcon(evt) {
    let feature;
    if (typeof evt === 'object') {
        feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
            return feature;
        });
    } else {
        sensorsArray.forEach(function (element) {
            if (element.get('id') === evt) {
                feature = element;
            }
        })
    }
    disposePopover();
    if (!feature) {
        return 0;
    }
    if (typeof evt === 'object') {
        popup.setPosition(evt.coordinate);
    } else {
        popup.setPosition(ol.proj.fromLonLat([feature.get('longitude'), feature.get('latitude')]));
    }
    popover = new bootstrap.Popover(element, {
        placement: 'top',
        html: true,
        content: feature.get('name'),
    });
    popover.show();

    if (typeof evt === 'object') {
        sensor.val(feature.get('id'));
        graph();
    }

    return evt;
}

function graph() {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(function(){ drawChart() });
}

function drawChart() {
    let id = sensor.val();
    let vertical = '°C';
    let horizontal = 't';
    let horizontalData = [new Date()];
    let verticalData = [0];
    let type = $('input[name=type]:checked').val();
    let title = 'Temperatuur';
    let rawData = $('#sensor-' + id + '-timestamps');
    if (id !== '' && rawData.length > 0) {
        rawData = rawData.data('timestamps');
        horizontalData = [];
        rawData.forEach(function (element) {
            let date = new Date(element + ' UTC');
            horizontalData.push(date);
        });
        if (type === 'temperature') {
            title = 'Temperatuur';
            vertical = '°C';
            verticalData = $('#sensor-' + id + '-temperatures').data('temperatures');
        } else if (type === 'humidity') {
            title = 'Luchtvochtigheid';
            vertical = 'RV %';
            verticalData = $('#sensor-' + id + '-humidities').data('humidities');
        } else if (type === 'pm25') {
            title = 'Fijnstof 2.5 µm';
            vertical = 'µg/m³';
            verticalData = $('#sensor-' + id + '-pm25s').data('pm25s');
        } else if (type === 'pm10') {
            title = 'Fijnstof 10 µm';
            vertical = 'µg/m³';
            verticalData = $('#sensor-' + id + '-pm10s').data('pm10s');
        }
    } else {
        if (type === 'temperature') {
            title = 'Temperatuur';
            vertical = '°C';
        } else if (type === 'humidity') {
            title = 'Luchtvochtigheid';
            vertical = 'RV %';
        } else if (type === 'pm25') {
            title = 'Fijnstof 2.5 µm';
            vertical = 'µg/m³';
        } else if (type === 'pm10') {
            title = 'Fijnstof 10 µm';
            vertical = 'µg/m³';
        }
    }

    let indices = []
    verticalData.forEach(function(element, index) {
        if (element === null) {
            indices.push(index)
        }
    });
    for (var i = indices.length -1; i >= 0; i--) {
        horizontalData.splice(indices[i], 1);
        verticalData.splice(indices[i], 1);
    }
    if (horizontalData.length === 0 || verticalData.length === 0) {
        verticalData = [0]
        horizontalData = [new Date()];
    }

    let dataGraph = horizontalData.map((name, index) =>
        [name, verticalData[index]]);
    let data = google.visualization.arrayToDataTable(
        [[horizontal, vertical]].concat(dataGraph));

    let options = {
        title: title,
        curveType: 'function',
        vAxis: { title: vertical },
        hAxis: { title: horizontal, format: 'MM-dd HH:mm' },
        legend: { position: 'none' }
    };
    let chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
    chart.draw(data, options);
}

graph();

sensor.on('change', function () {
    popupIcon($(this).val());
    graph();
});

$('input[name=type]').on('change', function () {
    graph();
});
