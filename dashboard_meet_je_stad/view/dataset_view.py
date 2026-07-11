from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.core.handlers.wsgi import WSGIRequest
import datetime
from django.apps import apps
from dashboard_meet_je_stad.repository.sensor_repository import SensorRepository
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.form.dataset_form import DatasetForm
import os


class DatasetView:

    def __init__(self):
        self.service = MeetJeStadAPIService()
        self.sensor_repository = SensorRepository()

    def index(self, request: WSGIRequest) -> HttpResponse | FileResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect('inloggen')
        form = DatasetForm(request.GET)

        if form.is_valid() and self.validate(form):

            try:
                start = form['start'].value()
                end = form['end'].value()
                start_date = datetime.datetime.strptime(start, "%Y-%m-%d,%H:%M:%S")
                end_date = datetime.datetime.strptime(end, "%Y-%m-%d,%H:%M:%S")
                last_sensor_id = os.getenv('LAST_SENSOR_ID')
                if last_sensor_id != '' and last_sensor_id is not None:
                    last_sensor_id = int(last_sensor_id)
                else:
                    raise Exception('Last sensor id is not set.')
                end_date = end_date.replace(tzinfo=datetime.timezone.utc)
                end_date += datetime.timedelta(seconds=1)
                start_date = start_date.replace(tzinfo=datetime.timezone.utc)
                delta = end_date - start_date
                sensors = self.sensor_repository.find_all()
                sensors = self.sensor_repository.filter_and_dress_with_measurements(sensors, False,
                                                                         '24hour', True, None)
                if form['ids'].value() == '':
                    ids = 'Utrecht'
                else:
                    ids = form['ids'].value()
                self.service.get_data(form['start'].value(), form['end'].value(), 'sensors',
                                      'csv', sensors, ids, form['particulate_matter_only'].value(),
                                      (delta.days + 1) * 24 * 4 * last_sensor_id,
                                      form['active_only'].value(), form.get_requested_cleanup(), True)
                path = os.path.dirname(apps.get_app_config('dashboard_meet_je_stad').path)
                file = open(path + '/data/tmp/dataset.csv', "rb")

                return FileResponse(file, content_type='text/csv', filename='dataset.csv')

            except Exception as e:
                form.add_error(None, str(e))

        return render(request, 'dataset/index.html', {'form': form})

    def validate(self, form: DatasetForm) -> bool:
        validated = True
        start_date = datetime.datetime.strptime('2000-01-01,00:00:00', "%Y-%m-%d,%H:%M:%S")
        end_date = datetime.datetime.strptime('2000-01-02,00:00:00', "%Y-%m-%d,%H:%M:%S")
        cutoff_temp = form['cutoff_temp'].value()
        cutoff_temp_min = form['cutoff_temp_min'].value()
        cutoff_temp_max = form['cutoff_temp_max'].value()
        cutoff_pm25 = form['cutoff_pm25'].value()
        cutoff_pm25_min = form['cutoff_pm25_min'].value()
        cutoff_pm25_max = form['cutoff_pm25_max'].value()
        cutoff_pm10 = form['cutoff_pm10'].value()
        cutoff_pm10_min = form['cutoff_pm10_min'].value()
        cutoff_pm10_max = form['cutoff_pm10_max'].value()
        try:
            start_date = datetime.datetime.strptime(form['start'].value(), "%Y-%m-%d,%H:%M:%S")
        except ValueError:
            form.add_error('start', 'Voer een waarde in met formaat yyyy-mm-dd,HH:mm:ss')

            validated = False
        try:
            end_date = datetime.datetime.strptime(form['end'].value(), "%Y-%m-%d,%H:%M:%S")
        except ValueError:
            form.add_error('end', 'Voer een waarde in met formaat yyyy-mm-dd,HH:mm:ss')

            validated = False

        if start_date > end_date:
            form.add_error('start', 'Eindtijd moet later zijn dan begintijd.')

            validated = False
        ids = form['ids'].value()
        if ids != '':
            for sensor_id in ids.split(','):
                for id_underscore in sensor_id.split('-'):
                    if not id_underscore.isdigit():
                        form.add_error('ids', 'Ongeldige ids. Alleen cijfers, komma\'s en streepjes toegestaan.')

                        validated = False

        if cutoff_temp_max < cutoff_temp_min:
            form.add_error('cutoff_temp_max', 'Afkap temperatuur max moet groter zijn dan min.')
            validated = False

        if cutoff_pm25_max < cutoff_pm25_min:
            form.add_error('cutoff_pm25_max', 'Afkap fijnstof 2.5 max moet groter zijn dan min.')
            validated = False

        if cutoff_pm10_max < cutoff_pm10_min:
            form.add_error('cutoff_pm10_max', 'Afkap fijnstof 10 max moet groter zijn dan min.')
            validated = False

        if cutoff_temp:
            if cutoff_temp_min == '':
                form.add_error('cutoff_temp_min', 'Afkap temperatuur min mag niet leeg zijn.')
                validated = False
            if cutoff_temp_max == '':
                form.add_error('cutoff_temp_min', 'Afkap temperatuur max mag niet leeg zijn.')
                validated = False

        if cutoff_pm25:
            if cutoff_pm25_min == '':
                form.add_error('cutoff_pm25_min', 'Afkap fijnstof 2.5 min mag niet leeg zijn.')
                validated = False
            if cutoff_pm25_max == '':
                form.add_error('cutoff_pm25_min', 'Afkap fijnstof 2.5 max mag niet leeg zijn.')
                validated = False

        if cutoff_pm10:
            if cutoff_pm10_min == '':
                form.add_error('cutoff_pm10_min', 'Afkap fijnstof 10 min mag niet leeg zijn.')
                validated = False
            if cutoff_pm10_max == '':
                form.add_error('cutoff_pm10_min', 'Afkap fijnstof 10 max mag niet leeg zijn.')
                validated = False

        return validated
