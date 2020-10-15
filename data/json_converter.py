import json
from .card_game_grouping import CardGameGrouping
from .card_guess import CardGuess

def get_data_json(data):
    jObject = [x.get_data_dict() for x in data]
    return json.dumps(jObject)

def get_guess_list(guessjson):
    j_obj = json.loads(guessjson)
    guessdata = [CardGuess(
        game_id=x['game'],
        team=x['team'],
        user_id=x['user_id'],
        card=x['card'],
        date=x['date'],
        time=x['time']
    ) for x in j_obj]

    return guessdata

def get_group_list(groupjson):
    j_obj = json.loads(groupjson)
    groupdata = [CardGameGrouping(
        gameId=x['game_id'],
        startDate=x['start_date'],
        endDate=x['end_date'],
        totalDays=x['total_days'],
        uniqueAttempts=x['unique_attempts'],
        totalAttempts=x['total_attempts'],
        repeatedGuesses=x['repeated_guesses'],
        winner=x['winner'],
        firstGuess=x['first_guess'],
        twoRow=x['two_row'],
        threeRow=x['three_row'],
        fourRow=x['four_row'],
        lastCard=x['last_card'],
        cardCounts=x['card_counts']
    ) for x in j_obj]

    return groupdata