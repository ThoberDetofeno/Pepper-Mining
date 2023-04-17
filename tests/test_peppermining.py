import unittest
from src.peppermining import PepperMining


class TestPepperMining(unittest.TestCase):

    def test_get_pepper_mining(self):
        p = PepperMining()
        p.set_event_data(5)
        self.assertEqual(p.get_event_data(), 5)


if __name__ == '__main__':
    unittest.main()
