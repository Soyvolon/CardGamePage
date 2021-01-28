import os
import pandas as pd
from data.card_game_data_reader import CardGameDataReader as Reader

class GroupAnalyzer:
    def __init__(self, path=None):
        if path == None:
            self.__path = Reader.GetDataPath("GroupData.csv")
        else:
            self.__path = path
        
class GuessAnalyzer:
    def __init__(self, path=None):
        if path == None:
            self.__path = Reader.GetDataPath("GuessData.csv")
        else:
            self.__path = path
        