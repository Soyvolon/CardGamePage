import os
import unittest
from data.card_game_data_reader import CardGameDataReader as Reader
from graphs.guess import team_count

class Test_TestComplieGroupGraphs(unittest.TestCase):
    def setUp(self):
        # register the data variable
        try:
            filePath = os.path.join(os.path.dirname(__file__), "test_data\\GuessTestData.csv")
            reader = Reader(
                filePath,
                "guess" 
            )

            self.data = reader.read_data()
        except Exception as ex:
            print(ex)
            self.assertTrue(False, msg="Failed to load data set")

    def test_data_retreival(self):
        print(self.data)
        self.assertTrue(True, msg="Data retrived")

    def test_team_count_graph(self):
        try:
            fig = team_count.get_graph(self.data)
            fig.show()
            self.assertTrue(True, msg="Guess Composite Graph Displayed")
        except Exception as ex:
            print(ex)
            self.assertTrue(False, msg="Failed to display Guess Composite")