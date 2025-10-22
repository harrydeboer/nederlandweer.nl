let sensors = $('#sensors');
let sensorIds = sensors.data('sensors');
let longitudes = sensors.data('longitudes');
let latitudes = sensors.data('latitudes');
let temperatures = sensors.data('temperatures');
let temperatureDates = sensors.data('temperature-dates');
let humidities = sensors.data('humidities');
let humidityDates = sensors.data('humidity-dates');
let pm25 = sensors.data('pm25');
let pm25Dates = sensors.data('pm25-dates');
let pm10 = sensors.data('pm10');
let pm10Dates = sensors.data('pm10-dates');

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
for (let index = 0; index < sensorIds.length; ++index) {
    let sensor = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([longitudes[index], latitudes[index]])),
        name: '<p class="sensor-title">Sensor ' + sensorIds[index] + '</p>' +
            '<p class="text-nowrap">' + temperatureDates[index] +
            ': Temperatuur ' + displayFloat(temperatures[index]) + '</p>' +
            '<p class="text-nowrap">' + humidityDates[index] +
            ': RV ' + displayFloat(humidities[index]) + '</p>' +
            '<p class="text-nowrap">' + displayPMDate(pm25Dates[index], pm25[index]) +
            'Fijnstof 2.5 ' + displayFloat(pm25[index]) + '</p>' +
            '<p class="text-nowrap">' + displayPMDate(pm10Dates[index], pm10[index]) +
            'Fijnstof 10 ' + displayFloat(pm10[index]) + '</p>',
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
}

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
