class Dashboard {

    constructor(form) {
        this.form = form;
        let sensors = $('#sensors');
        if (sensors.length > 0) {
            this.sensors = sensors.data('sensors');
        } else {
            return;
        }
        this.sensor = $('#id_sensor');
        this.type = $('input[name=type]');
        this.features = this.makeFeatures();

        const vectorSource = new ol.source.Vector({
            features: this.features,
        });

        const vectorLayer = new ol.layer.Vector({
            source: vectorSource,
        });

        this.map = new ol.Map({
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

        this.popup = new ol.Overlay({
            element: $('#popup')[0],
            positioning: 'bottom-center',
            stopEvent: false,
        });
        this.map.addOverlay(this.popup);

        this.map.on('click', this.mapClick.bind(this));
        this.map.on('pointermove', this.mapPointer.bind(this));
        this.map.on('movestart', this.disposePopover.bind(this));
        this.sensor.on('change', this.sensorChange.bind(this));
        this.type.on('change', this.graph.bind(this));

        this.graph();

        let that = this;
        setTimeout(function () {
            that.popupIcon(that.sensor.val());
        }, 500);
    }

    makeFeatures() {
        let features = []
        Object.keys(this.sensors).forEach((sensor_id) => {
            let sensor = this.sensors[sensor_id];
            for (var index = sensor['supply'].length - 1; index >= 0; index--) {
                if (sensor['supply'][index] !== null) {
                    break;
                }
            }
            let date = sensor.timestamp[index];
            date = new Date(date + ' UTC').toLocaleString("nl-NL", {timeZone: "Europe/Amsterdam"});
            let temperature = sensor['temperature'][index];
            let humidity = sensor['humidity'][index];
            let pm25 = sensor['pm25'][index];
            let pm10 = sensor['pm10'][index];
            let sourceImage;
            if ($('#id_pm:checked').length === 1 &&
                sensor['is_particulate_matter'] === false) {
                return;
            }
            if ($('#id_inactive:checked').length === 0 && sensor['is_active'] === false) {
                return;
            }
            if (sensor['is_active_sensor'] === false) {
                sourceImage = '/static/img/sensor-red.png'
            } else {
                sourceImage = '/static/img/sensor-green.png'
            }
            let mean_longitude = 0;
            let null_count = 0;
            for (let index = 0; index < sensor.longitude.length; index++) {
                if (sensor.longitude[index] === null) {
                    null_count++;
                } else {
                    mean_longitude += sensor.longitude[index];
                }
            }
            mean_longitude = mean_longitude / (sensor.longitude.length - null_count);
            let mean_latitude = 0;
            null_count = 0;
            for (let index = 0; index < sensor.latitude.length; index++) {
                if (sensor.latitude[index] === null) {
                    null_count++;
                } else {
                    mean_latitude += sensor.latitude[index];
                }
            }
            mean_latitude = mean_latitude / (sensor.latitude.length - null_count);
            let feature = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([mean_longitude, mean_latitude])),
                id: sensor_id,
                longitude: mean_longitude,
                latitude: mean_latitude,
                name: '<p class="sensor-title">Sensor ' + sensor_id + '</p>' +
                    '<p>' + date + '</p>' +
                    '<p>Temperatuur: ' + this.displayFloat(temperature) + ' °C</p>' +
                    '<p>Luchtvochtigheid: ' + this.displayFloat(humidity) + ' RV %</p>' +
                    '<p>Fijnstof 2.5: ' + this.displayFloat(pm25) + ' µg/m³</p>' +
                    '<p>Fijnstof 10: ' + this.displayFloat(pm10) + ' µg/m³</p>',
            });
            feature.setStyle(
                new ol.style.Style({
                    image: new ol.style.Icon({
                        crossOrigin: 'anonymous',
                        src: sourceImage,
                        width: 30,
                        height: 30,
                    }),
                }),
            );
            features.push(feature)
        });

        return features;
    }

    popupIcon(evt) {
        let feature;
        if (typeof evt === 'object') {
            feature = this.map.forEachFeatureAtPixel(evt.pixel, function (feature) {
                return feature;
            });
        } else {
            this.features.forEach(function (element) {
                if (element.get('id') === evt) {
                    feature = element;
                }
            })
        }
        this.disposePopover();
        if (!feature) {
            return 0;
        }
        if (typeof evt === 'object') {
            this.popup.setPosition(evt.coordinate);
        } else {
            this.popup.setPosition(ol.proj.fromLonLat([feature.get('longitude'), feature.get('latitude')]));
        }
        this.popover = new bootstrap.Popover($('#popup')[0], {
            placement: 'top',
            html: true,
            content: feature.get('name'),
        });
        this.popover.show();

        if (typeof evt === 'object') {
            this.sensor.val(feature.get('id'));
            this.graph();
        }

        return evt;
    }

    mapClick(event) {
        if (this.popupIcon(event)) {
            this.sensor.val()
        }
    }

    mapPointer(event) {
        const hit = this.map.hasFeatureAtPixel(event.pixel);
        this.map.getTargetElement().style.cursor = hit ? 'pointer' : '';
    }

    sensorChange() {
        if (this.sensor.val() !== '') {
            this.popupIcon(this.sensor.val());
            let dateFirst = new Date(this.sensors[this.sensor.val()].timestamp[0])
            let dateLast = new Date(this.sensors[this.sensor.val()].timestamp.slice(-1)[0])
            if ((dateLast.getTime() - dateFirst.getTime()) / 1000 > 24 * 60 * 60) {
                $("input[name=interval][value='3month']").prop("checked",true);
            } else {
                $("input[name=interval][value='24hour']").prop("checked",true);
            }
        }
        this.graph();
    }

    disposePopover() {
        if (this.popover) {
            this.popover.dispose();
            this.popover = undefined;
        }
    }

    displayFloat(value) {
        if (value !== 0) {
            return (Math.round(value * 10) / 10).toFixed(1);
        } else {
            return 'N/B';
        }
    }

    graph() {
        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(this.drawChart.bind(this));
    }

    drawChart() {
        let id = this.sensor.val();
        let vertical = '°C';
        let horizontal = 't';
        let horizontalData = [new Date()];
        let verticalData = [null];
        let type = $('input[name=type]:checked').val();
        let title = 'Temperatuur';
        let rawData;
        if (id === '') {
            rawData = [0];
        } else {
            rawData = this.sensors[id].timestamp;
        }
        if (id !== '' && rawData.length > 1) {
            horizontalData = [];
            rawData.forEach(function (element) {
                let date = new Date(element + ' UTC');
                horizontalData.push(date);
            });
            if (type === 'temperature') {
                title = 'Temperatuur';
                vertical = '°C';
                verticalData = this.sensors[id]['temperature'];
            } else if (type === 'humidity') {
                title = 'Luchtvochtigheid';
                vertical = 'RV %';
                verticalData = this.sensors[id]['humidity'];
            } else if (type === 'pm25') {
                title = 'Fijnstof 2.5 µm';
                vertical = 'µg/m³';
                verticalData = this.sensors[id]['pm25'];
            } else if (type === 'pm10') {
                title = 'Fijnstof 10 µm';
                vertical = 'µg/m³';
                verticalData = this.sensors[id]['pm10'];
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

        if (horizontalData.length === 0 || verticalData.length === 0) {
            verticalData = [null]
            horizontalData = [new Date()];
        }

        let data = new google.visualization.DataTable();
        data.addColumn('date', 'Date');
        data.addColumn('number', 'Value');

        horizontalData.forEach(function(element, index) {
            data.addRow([horizontalData[index], verticalData[index]])
        })

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
}
