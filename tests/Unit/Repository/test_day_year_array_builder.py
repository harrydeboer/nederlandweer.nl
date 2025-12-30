import unittest
from nederland_weer.repository.knmi_data_repository import KNMIDataRepository
from nederland_weer.model.knmi_data import KNMIData

class TestKNMIDataRepository(unittest.TestCase):

    def testMakeTempArray(self) -> None:

        first_year = 1906
        last_year = 2019
        knmi_data = KNMIData()
        temp_array = KNMIDataRepository().get(knmi_data.array, first_year, last_year, 'mean_temp')

        self.assertEqual(temp_array.shape, (365, last_year - first_year + 1))
#