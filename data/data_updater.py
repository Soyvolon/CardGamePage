import os
import csv
import json

from .card_guess import CardGuess as Guess
from .card_game_data_reader import CardGameDataReader as DataReader
from index import guessdata, groupdata

def save_new_guesses(json_data):
    print(json_data)
    # the items getting sent here should be guess updates.

def update_victory(json_data):
    print(json_data)