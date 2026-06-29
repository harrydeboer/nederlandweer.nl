from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.core.handlers.wsgi import WSGIRequest
from dashboard_meet_je_stad.service.meet_je_stad_api_service import MeetJeStadAPIService
from dashboard_meet_je_stad.form.dataset_form import DatasetForm


class DatasetView:

    def __init__(self):
        self.service = MeetJeStadAPIService()

    def index(self, request: WSGIRequest) -> HttpResponse | FileResponse:
        form = DatasetForm(request.GET)

        if form.is_valid():
            self.service.get_data(form['start'].value(), form['end'].value(), 'sensors',
                                  'csv', 'Utrecht')
            return FileResponse('data/tmp/dataset.csv', content_type='text/csv', filename='dataset.csv')

        return render(request, 'dataset/index.html', {'form': form})
