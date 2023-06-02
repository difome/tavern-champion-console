import unittest
from drinking import Drinking

class TestDrinking(unittest.TestCase):
    def setUp(self):
        self.drinking = Drinking()

    def test_drink(self):
        while self.drinking.status_message != "Вы достигли предельного уровня пьянства!":
            self.drinking.drink()
        self.assertEqual("Вы достигли предельного уровня пьянства!", self.drinking.status_message)

if __name__ == '__main__':
    unittest.main()
