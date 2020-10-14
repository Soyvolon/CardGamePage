import os
import csv
import json

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

from .card_guess import CardGuess
from .card_game_grouping import CardGameGrouping as GameGroup
from .card_game_data_reader import CardGameDataReader as DataReader

guess_converter = { "AC":0, "2C":1, "3C":2, "4C":3, "5C":4, "6C":5, "7C":6, "8C":7, "9C":8, "10C":9, "JC":10, "QC":11, "KC":12, "AD":13, "2D":14, "3D":15, "4D":16, "5D":17, "6D":18, "7D":19, "8D":20, "9D":21, "10D":22, "JD":23, "QD":24, "KD":25, 
"AH":26, "2H":27, "3H":28, "4H":29, "5H":30, "6H":31, "7H":32, "8H":33, "9H":34, "10H":35, "JH":36, "QH":37, "KH":38, "AS":39, "2S":40, "3S":41, "4S":42, "5S":43, "6S":44, "7S":45, "8S":46, "9S":47, "10S":48, "JS":49, "QS":50, "KS":51 }

def save_new_guesses(json_data, guessdata, groupdata):
    try:
        # we are assuming the JSON is valid
        # and will return false if an error
        # occours.
        new_guesses = []
        for guess in json_data:
            # take it one guess at a time
            new_guesses.append(CardGuess(
                game_id= guess['game'],
                user_id= guess['user_id'],
                team= guess['team'],
                card= guess['card'],
                date= guess['date'],
                time= guess['time']
            ))

        return update_live_data(new_guesses, guessdata, groupdata)
    except Exception:
        return False

def update_live_data(new_guesses, guessdata, groupdata):
    guessdata.extend(new_guesses)
    # the group will not be chaning durring live data reuqests
    c_group =  next((x for x in groupdata if x.game_id == new_guesses[0].game_id), None)
    if c_group.game_id != len(groupdata):
        return False # don't allow updates unless
            # its for the latest game!
    for guess in new_guesses:
        if(c_group == None or guess.game_id != c_group.game_id):
            return False
        else:
            # update the group data
            g = c_group.card_counts[guess_converter[guess.card]]
            if(g == 'Y'):
                return False # game is already completed!
            else:
                new_num = int(g) + 1
                c_group.card_counts[guess_converter[guess.card]] = str(new_num)
            
            update_attempts(c_group)
    
    write_update_group(c_group)
    write_new_guesses(new_guesses)
    return True

def update_attempts(group):
    card_counts = [int(x) for x in group.card_counts if x != "0" and x != "Y"]
    if("Y" in group.card_counts):
        card_counts.append(1)
    group.unique_attempts = len(card_counts)
    group.total_attempts = sum(card_counts)
    group.repeated_guesses = group.total_attempts - group.unique_attempts

def write_update_group(group):
    path = DataReader.GetDataPathFileByName('GroupData.csv')
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w', newline='') as temp_file:
        writer = csv.writer(temp_file, delimiter=',', quotechar='|')
        with open(path) as old_file:
            reader = csv.reader(old_file, delimiter=',', quotechar='|')
            for row in reader:
                if(len(row) == 0):
                    continue
                try:
                    if(int(row[0]) == group.game_id):
                        # replace this line
                        data = [
                            group.game_id,
                            group.start_date,
                            group.end_date,
                            group.total_days,
                        ]
                        
                        data.extend(group.card_counts)

                        data.extend([
                            group.unique_attempts,
                            group.total_attempts,
                            group.repeated_guesses,
                            group.winner,
                            group.first_guess,
                            group.two_row,
                            group.three_row,
                            group.four_row,
                            group.last_card
                        ])
                        
                        writer.writerow(data)
                    else:
                        writer.writerow(row)
                except:
                    writer.writerow(row)

    copymode(path, abs_path)
    remove(path)
    move(abs_path, path)

def write_new_guesses(new_guesses):
    path = DataReader.GetDataPathFileByName('GuessData.csv')
    with open(path, 'a', newline='') as fs:
        writer = csv.writer(fs, delimiter=',', quotechar='|')
        for line in new_guesses:
            writer.writerow([
                "", # game col, dont write anything to this.
                line.team,
                line.user_id,
                line.card,
                line.date,
                line.time
            ])

def update_victory(json_data, guessdata, groupdata):
    # assume the json is correct
    try:
        
        return False
    except Exception:
        return False

def remove_guess_from_group(guess, group):
    return False

def write_new_game(game_id, last_guess):
    path = DataReader.GetDataPathFileByName('GuessData.csv')
    with open(path, 'a', newline='') as fs:



        # write the new game row
        writer = csv.writer(fs, delimiter=',', quotechar='|')
        writer.writerow([
            game_id, # next game id
            "", "", "", "", "" # blank row
        ])

def write_new_group(new_group):
    return False