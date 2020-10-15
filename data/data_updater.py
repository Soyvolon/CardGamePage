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
    if c_group == None or c_group.game_id != len(groupdata):
        return False # don't allow updates unless
            # its for the latest game!
    # get the guesses so far
    guesses = sum([int(x) for x in c_group.card_counts if x != "0" and x != "Y"])
    for guess in new_guesses:
        if(guess.game_id != c_group.game_id):
            return False
        else:
            if(guesses == 0): # first guess? Update start date.
                c_group.start_date = guess.date

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
    card_counts = [int(x) for x in group.card_counts if not (x == "0" or x == 0) and x != "Y"]
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
        last_game = len(groupdata)
        if(json_data['game_id'] != last_game):
            return False # cant update the victory if its
            # not the last game
        
        # the group will not be chaning durring live data reuqests
        c_group =  next((x for x in groupdata if x.game_id == last_game), None)
        if c_group == None or c_group.game_id != last_game:
            return False # don't allow updates unless
                # its for the latest game!

        # find the winning guess object
        guess_list = [x for x in guessdata if x.game_id == last_game]
        guess = next((x for x in guess_list if x.user_id == json_data['user_id']
            and x.card == json_data['card']
            and x.date == json_data['date']), None)

        if(guess == None):
            return False # no matching guess found

        # set the end date equal to the last guess
        c_group.end_date = guess.date

        # get the guesses after the winning guess
        index = guessdata.index(guess)
        to_remove = guessdata[index + 1:]
        # remove any guesses after the winning guess
        for i in to_remove:
            try:
                remove_guess_from_group(i, c_group)
                guessdata.remove(i)
            except ValueError:
                pass
        # assign the winning card id
        c_group.card_counts[guess_converter[guess.card]] = 'Y'
        update_attempts(c_group) # update attempts data

        c_group.winner = guess.user_id
        add_winner_flags(c_group, groupdata)

        # write a new game to the GuessData
        write_new_game(last_game + 1, guess)

        # update the last game group
        write_update_group(c_group)

        # create a new game group
        new_group = GameGroup(gameId=last_game + 1)
        groupdata.append(new_group)

        # write the new game group
        write_new_group(new_group)

        return True
    except Exception:
        return False

def add_winner_flags(group, groupdata):
    index = groupdata.index(group)
    card_counts = [int(x) for x in group.card_counts if x != "0" and x != "Y"]
    if("Y" in group.card_counts):
        card_counts.append(1)
    guess_count = sum(card_counts)
    unique_guess = len(card_counts)

    if(guess_count == 1):
        group.first_guess = 'X'

    if((index-1) > -1 and groupdata[index-1].winner == group.winner):
        if((index-2) > -1 and groupdata[index-2].winner == group.winner):
            if((index-3) > -1 and groupdata[index-3].winner == group.winner):
                group.four_row = 'X'
            else:
                group.three_row = 'X'
        else:
            group.two_row = 'X'

    if(unique_guess == 52):
        group.last_card = 'X'


def remove_guess_from_group(guess, group):
    # update the group data
    g = group.card_counts[guess_converter[guess.card]]
    if(g == 'Y'):
        group.card_counts[guess_converter[guess.card]] = str(0)
    else:
        new_num = int(g) - 1
        if new_num < 0: new_num = 0
        group.card_counts[guess_converter[guess.card]] = str(new_num)


def write_new_game(new_game_id, last_guess):
    path = DataReader.GetDataPathFileByName('GuessData.csv')
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w', newline='') as temp_file:
        writer = csv.writer(temp_file, delimiter=',', quotechar='|')
        with open(path) as old_file:
            reader = csv.reader(old_file, delimiter=',', quotechar='|')
            for row in reader:
                if(len(row) == 0):
                    continue
                if(row[2] == last_guess.user_id and
                    row[3] == last_guess.card and
                    row[4] == last_guess.date):

                    # write this row
                    writer.writerow(row)
                    # write the new game row
                    writer.writerow([
                        new_game_id, # next game id
                        "", "", "", "", "" # blank row
                    ])
                    # break the loop, we are done editing
                    break
                else:
                    writer.writerow(row)
    copymode(path, abs_path)
    remove(path)
    move(abs_path, path)

def write_new_group(group):
    path = DataReader.GetDataPathFileByName('GroupData.csv')
    with open(path, 'a', newline='') as fs:
        writer = csv.writer(fs, delimiter=',', quotechar='|')

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

def update_single_guess(update_info, guessdata, groupdata):
    try:
        if(update_info['new']['game'] != update_info['old']['game']):
            return False # Can't change the game of an editied guess!
        else:
            game = update_info['new']['game']

        # the group will not be chaning durring live data reuqests
        c_group =  next((x for x in groupdata if x.game_id == game), None)
        if c_group == None or c_group.game_id != len(groupdata):
            return False # don't allow updates unless
                # its for the latest game!

        inverted_guesses = guessdata[::-1]
        guesses_for_group = [x for x in inverted_guesses if x.game_id == game]
        c_guess = next((x for x in guesses_for_group if 
            x.card == update_info['old']['card']
            and x.user_id == update_info['old']['user_id']
            and x.date == update_info['old']['date']), None)

        if(c_guess == None):
            return False # can't edit something that does not exsist!

        guess_index = guesses_for_group.index(c_guess)

        update = CardGuess(
            game,
            team = update_info['new']['team'],
            card = update_info['new']['card'],
            date = update_info['new']['date'],
            time = update_info['new']['time'],
            user_id = update_info['new']['user_id']
        )

        # remove the old guess from the group
        remove_guess_from_group(c_guess, c_group)

        # replace card data
        c_guess.user_id = update.user_id
        c_guess.team = update.team
        c_guess.card = update.card
        c_guess.date = update.date
        c_guess.time = update.time

        # update the group data
        if(guess_index == 0): # first guess, update start date
            c_group.start_date = c_guess.date

        g = c_group.card_counts[guess_converter[c_guess.card]]
        if(g == 'Y'):
            return False # game is already completed!
        else:
            new_num = int(g) + 1
            c_group.card_counts[guess_converter[c_guess.card]] = str(new_num)

        write_update_group(c_group)
        write_update_guess(update_info['old'], c_guess)

        return True
    except Exception:
        return False

def write_update_guess(guess, new_data):
    path = DataReader.GetDataPathFileByName('GuessData.csv')
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w', newline='') as temp_file:
        writer = csv.writer(temp_file, delimiter=',', quotechar='|')
        with open(path) as old_file:
            reader = csv.reader(old_file, delimiter=',', quotechar='|')
            for row in reader:
                if(len(row) == 0):
                    continue
                if(row[2] == guess['user_id'] and
                    row[3] == guess['card'] and
                    row[4] == guess['date']):

                    # write the edited data
                    writer.writerow([
                        "", # game col, dont write anything to this.
                        new_data.team,
                        new_data.user_id,
                        new_data.card,
                        new_data.date,
                        new_data.time
                    ])
                else:
                    writer.writerow(row)
    copymode(path, abs_path)
    remove(path)
    move(abs_path, path)