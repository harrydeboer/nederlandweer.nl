from nederland_weer.model.curve import Curve
from nederland_weer.repository.measurement_repository import MeasurementRepository
import numpy as np
import json

class CurveService:

    def __init__(self):
        self.measurement_repository = MeasurementRepository()

    def get_curve(self, measurements: np.ndarray, column_name: str, axis: int, first_year: int, last_year: int) -> Curve:
        array = self.measurement_repository.get(measurements, first_year, last_year, column_name)
        y = array.mean(axis=axis)
        return Curve(y, bool(axis), first_year, last_year)

    def curve_to_json(self, curve: Curve) -> str:
        data_array = np.array([curve.x, curve.y, curve.y_smooth])
        return json.dumps(np.transpose(data_array).tolist())