def get_current_game(guessdata, game_id):
    guesses = [x.get_data_dict() for x in guessdata if x.game_id == game_id]
    json = { "game_id": game_id,
    "guesses": guesses }
    return json