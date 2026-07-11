from django.db import models
from django.contrib.auth.models import User
from dashboard_meet_je_stad.model.sensor import Sensor


class DashboardUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
