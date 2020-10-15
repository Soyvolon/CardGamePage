class CardGuess(object):
    def __init__(self, game_id, team, user_id, card, date, time):
        self.game_id = game_id
        self.team = team
        self.user_id = user_id
        self.card = card
        self.date = date
        self.time = time
    
    def get_data_dict(self):
        return {
            "game": self.game_id,
            "team": self.team,
            "user_id": self.user_id,
            "card": self.card,
            "date": self.date,
            "time": self.time
        }