import os
import unittest
from data.card_game_data_reader import CardGameDataReader as Reader
import pandas as pd

class Test_TestBuildMLData(unittest.TestCase):
    def setUp(self):
        try:
            group_path = os.path.join(os.path.dirname(__file__), "test_data", "GroupTestData.csv")
            guess_path = os.path.join(os.path.dirname(__file__), "test_data", "GuessTestData.csv")
            
            self.group_frame = pd.read_csv(group_path)
            self.guess_frame = pd.read_csv(guess_path)
        except Exception as ex:
            print(ex)
            self.assertTrue(False, msg="Failed to load data sets.")

    def test_print_heads(self):
        print()
        print(self.group_frame.head())
        print(self.guess_frame.head())
        self.assertTrue(True, msg="Heads printed.")

    def test_print_describe(self):
        print()
        print(self.group_frame.describe())
        print(self.guess_frame.describe())
        self.assertTrue(True, msg="Descriptions printed.")

    