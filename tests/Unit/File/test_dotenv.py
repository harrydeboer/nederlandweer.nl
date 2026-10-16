from unittest import TestCase
import dotenv


class TestDotenv(TestCase):

    def test_dotenv(self):
        params = dotenv.dotenv_values()
        params_example = dotenv.dotenv_values(".env.example")
        params_test = dotenv.dotenv_values(".env.test")
        self.assertEqual(params.keys(),params_example.keys())
        self.assertEqual(params.keys(),params_test.keys())
