let sensors = $('#sensors');
let sensorIds = sensors.data('sensors');

function displayFloat(value) {
    if (value !== 0) {
        return (Math.round(value * 10) / 10).toFixed(1);
    } else {
        return 'N/B';
    }
}

function displayPMDate(date, value) {
    if (value === 0) {
        return '';
    } else {
        return date + ': ';
    }
}

sensorsArray = []
sensorIds.forEach((index) => {
    let dates = $('#sensor-' + index + '-timestamp').data('timestamp');
    let temperatures = $('#sensor-' + index + '-temperature').data('temperature');
    let longitudes = $('#sensor-' + index + '-longitude').data('longitude');
    let latitudes = $('#sensor-' + index + '-latitude').data('latitude');
    let humidities = $('#sensor-' + index + '-humidity').data('humidity');
    let pm25s = $('#sensor-' + index + '-pm25').data('pm25');
    let pm10s = $('#sensor-' + index + '-pm10').data('pm10');
    let total = 0;
    for(let i = 0; i < longitudes.length; i++) {
        total += longitudes[i];
    }
    let longitude = total / longitudes.length;
    total = 0;
    for(let i = 0; i < latitudes.length; i++) {
        total += latitudes[i];
    }
    let latitude = total / latitudes.length;
    let date = dates[dates.length - 1];
    date = new Date(date + ' AM UTC').toLocaleString();
    let temperature = temperatures[temperatures.length - 1];
    let humidity = humidities[humidities.length - 1];
    let pm25 = pm25s[pm25s.length - 1];
    let pm10 = pm10s[pm10s.length - 1];
    let sensor = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude, latitude])),
        name: '<p class="sensor-title">Sensor ' + index + '</p>' +
            '<p class="text-nowrap">' + date +
            ': Temperatuur ' + displayFloat(temperature) + '</p>' +
            '<p class="text-nowrap">' + date +
            ': RV ' + displayFloat(humidity) + '</p>' +
            '<p class="text-nowrap">' + displayPMDate(date, pm25) +
            'Fijnstof 2.5 ' + displayFloat(pm25) + '</p>' +
            '<p class="text-nowrap">' + displayPMDate(date, pm10) +
            'Fijnstof 10 ' + displayFloat(pm10) + '</p>',
    });
    sensor.setStyle(
        new ol.style.Style({
            image: new ol.style.Icon({
                crossOrigin: 'anonymous',
                src: '/static/img/sensor-blue.png',
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
        center: ol.proj.fromLonLat([5.085, 52.085]),
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
    const feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
        return feature;
    });
    disposePopover();
    if (!feature) {
        return;
    }
    popup.setPosition(evt.coordinate);
    popover = new bootstrap.Popover(element, {
        placement: 'top',
        html: true,
        content: feature.get('name'),
    });
    popover.show();
});

// change mouse cursor when over marker
map.on('pointermove', function (e) {
    const hit = map.hasFeatureAtPixel(e.pixel);
    map.getTargetElement().style.cursor = hit ? 'pointer' : '';
});
// Close the popup when the map is moved
map.on('movestart', disposePopover);
