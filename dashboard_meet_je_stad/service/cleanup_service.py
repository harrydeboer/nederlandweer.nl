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
                temperature = measurement.get_temperature()
                if not temperature is None:
                    if (temperature < cleanup['cutoff_temp']['min']
                            or temperature > cleanup['cutoff_temp']['max']):
                        measurement.set_temperature(None)
            if cleanup['cutoff_pm25']['is_on']:
                pm25 = measurement.get_pm25()
                if not pm25 is None:
                    if (pm25 < cleanup['cutoff_pm25']['min']
                            or pm25 > cleanup['cutoff_pm25']['max']):
                        measurement.set_pm25(None)
            if cleanup['cutoff_pm10']['is_on']:
                pm10 = measurement.get_pm10()
                if not pm10 is None:
                    if (pm10 < cleanup['cutoff_pm10']['min']
                            or pm10 > cleanup['cutoff_pm10']['max']):
                        measurement.set_pm10(None)

        return measurements
