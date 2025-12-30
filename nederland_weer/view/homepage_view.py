from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


class HomepageView:

    def index(self, request: WSGIRequest) -> HttpResponse:
        return render(request, 'homepage/index.html', {'data': [[]], 'text_output': ''})