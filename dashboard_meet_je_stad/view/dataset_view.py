from django.shortcuts import render
import os
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.core.handlers.wsgi import WSGIRequest
import datetime
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.form.dataset_form import DatasetForm


class DatasetView:

    def __init__(self):
        self.service = MeetJeStadAPIService()

    def index(self, request: WSGIRequest) -> HttpResponse | FileResponse:
        if not request.user.is_authenticated or not request.user.is_superuser:
            return HttpResponseRedirect('inloggen')
        form = DatasetForm(request.GET)

        if form.is_valid():
            start = form['start'].value()
            end = form['end'].value()
            try:
                datetime.datetime.strptime(start, "%Y-%m-%d,%H:%M:%S")
                datetime.datetime.strptime(end, "%Y-%m-%d,%H:%M:%S")

                self.service.get_data(start, end, 'sensors',
                                      'csv', 'Utrecht')
                path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                parent_path = os.path.dirname(path)
                file = open(parent_path + '/data/tmp/dataset.csv', "rb")

                return FileResponse(file, content_type='text/csv', filename='dataset.csv')
            except ValueError:
                form.add_error('start', 'Voer een waarde in met formaat yyyy-mm-dd,HH:mm:ss')
            except Exception as e:
                form.add_error('start', str(e))

        return render(request, 'dataset/index.html', {'form': form})
