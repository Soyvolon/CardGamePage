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