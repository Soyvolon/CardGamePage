import os
import unittest
from data.card_game_data_reader import CardGameDataReader as Reader
from graphs.group import attempts, winners, game_length

class Test_TestComplieGroupGraphs(unittest.TestCase):
    def setUp(self):
        # register the data variable
        try:
            filePath = os.path.join(os.path.dirname(__file__), "test_data", "GroupTestData.csv")
            reader = Reader(
                filePath,
                "group" 
            )

            self.data = reader.read_data()
        except Exception as ex:
            print(ex)
            self.assertTrue(False, msg="Failed to load data set")

    def test_data_retreival(self):
        print(self.data)
        self.assertTrue(True, msg="Data retrived")

    def test_attempts_grpah(self):
        try:
            fig = attempts.get_graph(self.data)
            fig.show()
            self.assertTrue(True, msg="Attempts Graph Displayed")
        except Exception as ex:
            print(ex)
            self.assertTrue(False, msg="Failed to display attempts")
    
    def test_winners_graph(self):
        try:
            fig = winners.get_graph(self.data)
            fig.show()
            self.assertTrue(True, msg="Winners Graph Displayed")
        except Exception as ex:
            print(ex)
            self.assertTrue(False, msg="Failed to display Winners")

    def test_game_length_graph(self):
        try:
            fig = game_length.get_graph(self.data)
            fig.show()
            self.assertTrue(True, msg="Game Length Graph Displayed")
        except Exception as ex:
            print(ex)
            self.assertTrue(False, msg="Failed to display Game Length")

if(__file__ == "__main__"):
    unittest.main()