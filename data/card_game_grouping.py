class CardGameGrouping(object):
    def __init__(self, gameId = 0, startDate = "", endDate = "", totalDays = 0, 
        uniqueAttempts = 0, totalAttempts = 0, repeatedGuesses = 0, 
        winner = 0, 
        firstGuess = "", twoRow = "", threeRow = "", 
        fourRow = "", lastCard = "", cardCounts = ['0'] * 52):
        self.game_id = gameId
        self.start_date = startDate
        self.end_date = endDate
        self.total_days = totalDays
        self.unique_attempts = uniqueAttempts
        self.total_attempts = totalAttempts
        self.repeated_guesses = repeatedGuesses
        self.winner = winner
        self.first_guess = firstGuess
        self.two_row = twoRow
        self.three_row = threeRow
        self.four_row = fourRow
        self.last_card = lastCard
        self.card_counts = cardCounts

    def get_data_dict(self):
        return {
            "game_id": self.game_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_days": self.total_days,
            "unique_attempts": self.unique_attempts,
            "total_attempts": self.total_attempts,
            "repeated_guesses": self.repeated_guesses,
            "winner": self.winner,
            "first_guess": self.first_guess,
            "two_row": self.two_row,
            "three_row": self.three_row,
            "four_row": self.four_row,
            "last_card": self.last_card,
            "card_counts": self.card_counts
        }