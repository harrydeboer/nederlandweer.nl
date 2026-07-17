from typing import List
from dashboard_meet_je_stad.models import Measurement


class CleanupService:

    cleanup_default = {'cutoff_temp': {'is_on': True, 'min': -25, 'max': 70},
                       'cutoff_pm25': {'is_on': True, 'min': 0, 'max': 250},
                       'cutoff_pm10': {'is_on': True, 'min': 0, 'max': 250}}

    def clean(self, measurements: List[Measurement], cleanup: dict| None = None) -> List[Measurement]:
        if cleanup is None:
            cleanup = self.cleanup_default
        for measurement in measurements:
            if cleanup['cutoff_temp']['is_on']:
                if not measurement.temperature is None:
                    if (measurement.temperature < cleanup['cutoff_temp']['min']
                            or measurement.temperature > cleanup['cutoff_temp']['max']):
                        measurement.temperature = None
            if cleanup['cutoff_pm25']['is_on']:
                if not measurement.pm25 is None:
                    if (measurement.pm25 < cleanup['cutoff_pm25']['min']
                            or measurement.pm25 > cleanup['cutoff_pm25']['max']):
                        measurement.pm25 = None
            if cleanup['cutoff_pm10']['is_on']:
                if not measurement.pm10 is None:
                    if (measurement.pm10 < cleanup['cutoff_pm10']['min']
                            or measurement.pm10 > cleanup['cutoff_pm10']['max']):
                        measurement.pm10 = None

        return measurements
