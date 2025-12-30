from nederland_weer.model.curve import Curve
from nederland_weer.model.knmi_data import KNMIData
from nederland_weer.repository.knmi_data_repository import KNMIDataRepository
import numpy as np
import json

class CurveService:

    def __init__(self, knmi_data:KNMIData):
        self.knmi_repository = KNMIDataRepository()
        self.knmiData = knmi_data

    def get_curve(self, column_name: str, axis: int, first_year: int, last_year: int) -> Curve:
        array = self.knmi_repository.get(self.knmiData.array, first_year, last_year, column_name)
        y = array.mean(axis=axis)
        return Curve(y, bool(axis), first_year, last_year)

    def curve_to_json(self, curve: Curve) -> str:
        data_array = np.array([curve.x, curve.y, curve.y_smooth])
        return json.dumps(np.transpose(data_array).tolist())