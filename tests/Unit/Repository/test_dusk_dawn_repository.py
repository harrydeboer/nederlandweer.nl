import unittest
from nederland_weer.repository.dawn_dusk_repository import DawnDuskRepository
from nederland_weer.models import DawnDusk


class TestDawnDuskRepository(unittest.TestCase):

    def testFindAll(self) -> None:
        dawn_dusks = DawnDuskRepository().find_all()

        self.assertIsInstance(dawn_dusks, list)
        self.assertIsInstance(dawn_dusks[0], DawnDusk)
#