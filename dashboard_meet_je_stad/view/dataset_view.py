from django.shortcuts import render
import os
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.core.handlers.wsgi import WSGIRequest
import datetime
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.form.dataset_form import DatasetForm
import os


class DatasetView:

    def __init__(self):
        self.service = MeetJeStadAPIService()

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
                last_sensor_id = int(os.getenv('LAST_SENSOR_ID'))
                end_date = end_date.replace(tzinfo=datetime.timezone.utc)
                end_date += datetime.timedelta(seconds=1)
                start_date = start_date.replace(tzinfo=datetime.timezone.utc)
                delta = end_date - start_date
                if form['ids'].value() == '':
                    ids = 'Utrecht'
                else:
                    ids = form['ids'].value()
                cleanup = {'cutoff_temp': form['cutoff_temp'].value(),
                          'cutoff_pm25': form['cutoff_pm25'].value(),
                          'cutoff_pm10': form['cutoff_pm10'].value()}
                self.service.get_data(form['start'].value(), form['end'].value(), 'sensors',
                                      'csv', ids, form['particulate_matter_only'].value(),
                                      2 * (delta.days + 1) * 24 * 4 * last_sensor_id,
                                      form['active_only'].value(), cleanup)
                path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                parent_path = os.path.dirname(path)
                file = open(parent_path + '/data/tmp/dataset.csv', "rb")

                return FileResponse(file, content_type='text/csv', filename='dataset.csv')

            except Exception as e:
                form.add_error(None, str(e))

        return render(request, 'dataset/index.html', {'form': form})

    def validate(self, form: DatasetForm) -> bool:
        validated = True
        try:
            start_date = datetime.datetime.strptime(form['start'].value(), "%Y-%m-%d,%H:%M:%S")
        except ValueError:
            form.add_error('start', 'Voer een waarde in met formaat yyyy-mm-dd,HH:mm:ss')

            return False
        try:
            end_date = datetime.datetime.strptime(form['end'].value(), "%Y-%m-%d,%H:%M:%S")
        except ValueError:
            form.add_error('end', 'Voer een waarde in met formaat yyyy-mm-dd,HH:mm:ss')

            return False

        if start_date > end_date:
            form.add_error('start', 'Eindtijd moet later zijn dan begintijd.')

            return False
        exception_message = 'Ongeldige ids. Alleen cijfers, komma\'s en streepjes toegestaan.'
        ids = form['ids'].value()
        if ids != '':
            for id_sensor in ids.split(','):
                if len(id_sensor.split('-')) > 1:
                    for id_underscore in id_sensor.split('-'):
                        if not id_underscore.isdigit():
                            form.add_error('ids', exception_message)

                            return False
                else:
                    if not id_sensor.isdigit():
                        form.add_error('ids', exception_message)

                        return False

        return validated
