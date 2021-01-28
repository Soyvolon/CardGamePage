import csv
import os
from pathlib import Path
from .card_game_grouping import CardGameGrouping
from .card_guess import CardGuess
import pandas as pd

class CardGameDataReader(object):
    @staticmethod
    def GetDataPathFileByName(fileName):
        return os.path.join(os.path.dirname(__file__), "data-files", fileName)

    @staticmethod
    def GetGroupData():
        r = CardGameDataReader(
            CardGameDataReader.GetDataPathFileByName("GroupData.csv"),
            "group"
        )

        return r.read_data()

    @staticmethod
    def GetGuessData():
        r = CardGameDataReader(
            CardGameDataReader.GetDataPathFileByName("GuessData.csv"),
            "guess"
        )

        return r.read_data()

    @staticmethod
    def GetDataPath(fileType = "GroupData.csv"):
        return os.path.join(os.path.dirname(__file__), "data-files", fileType)

    def __init__(self, fileName = "", fileType = ""):
        self.fileName = fileName
        self.fileType = fileType

    def read_data(self):
        if(self.fileType == "group"):
            return self.__read_group_data()
        elif(self.fileType == "guess"):
            return self.__read_tree_data()
 
    def __read_group_data(self):
        data = []
        if not os.path.exists(os.path.dirname(self.fileName)):
            Path('./data/data-files').mkdir(parents=True, exist_ok=True)

        if not os.path.exists(self.fileName):
            # create an csv with the title cols
            tempD = ["#,Start Date,End Date,Total Days,Clubs,,,,,,,,,,,,,Diamonds,,,,,,,,,,,,,Hearts,,,,,,,,,,,,,Spades,,,,,,,,,,,,,Unique Attempts,Total Attempts,Repeated Guesses,Winner,First Guess,Two In A Row,Three In A Row,Four In A Row,52nd Card",
                ",,,,A,2,3,4,5,6,7,8,9,10,J,Q,K,A,2,3,4,5,6,7,8,9,10,J,Q,K,A,2,3,4,5,6,7,8,9,10,J,Q,K,A,2,3,4,5,6,7,8,9,10,J,Q,K,,,,,,,,,",
                ",,,,AC,2C,3C,4C,5C,6C,7C,8C,9C,10C,JC,QC,KC,AD,2D,3D,4D,5D,6D,7D,8D,9D,10D,JD,QD,KD,AH,2H,3H,4H,5H,6H,7H,8H,9H,10H,JH,QH,KH,AS,2S,3S,4S,5S,6S,7S,8S,9S,10S,JS,QS,KS,,,,,,,,,"]
            with open(self.fileName, "w+", newline='') as fs:
                writer = csv.writer(fs, delimiter=",", quotechar='|')
                for row in tempD:
                    writer.writerow(row.split(','))
                # write an empty first game
                group = CardGameGrouping(gameId=1)
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


        with open(self.fileName, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')

            c = 0
            for row in reader:
                # dont move foward if the row is in the 3 start rows
                if(len(row) == 0):
                            continue # looks like a blank line
                if(c >= 3):
                    try:
                        # read the data into a grouping
                        group = CardGameGrouping(
                            int(row[0]),
                            row[1],
                            row[2],
                            row[3],
                            row[56],
                            row[57],
                            row[58],
                            row[59],
                            row[60],
                            row[61],
                            row[62],
                            row[63],
                            row[64],
                            row[4:56]                      
                        )
                        # add the grouping to the final data set
                        data.append(group)
                    except Exception as e:
                        # skip this line, we had an error
                        print(e)
                        c += 1
                        continue

                # move to next row
                c += 1

        return data

    def __read_tree_data(self):
        data = []
        if not os.path.exists(os.path.dirname(self.fileName)):
            Path('./data/data-files').mkdir(parents=True, exist_ok=True)

        if not os.path.exists(self.fileName):
            tempD = ["Game,Team,User,Card,Date,Time",
                    '#,P - D - R - C - U - W - E - N - n/a,User ID,"A, 2-10, J, Q, K + C/D/H/S",Date the Guess was Made,Time the Guess was Made',
                    '1,,,,,']
            with open(self.fileName, "w+", newline='') as fs:
                writer = csv.writer(fs, delimiter=",", quotechar='|')
                for row in tempD:
                    writer.writerow(row.split(','))

        with open(self.fileName, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=",", quotechar='|')

            row_num = 0
            game_num = 0

            for row in reader:
                if(row_num <= 1):
                    # we dont need these line,
                    # they are label lines.
                    row_num += 1
                    continue
                
                try:
                    if(row[0] != ""):
                        # this is a game header, 
                        # so set the game_num value
                        # and go to the next line
                        game_num = int(row[0])
                        continue
                    elif(row[1] != ""):
                        # this is a guess row, 
                        # so read the data.
                        item = CardGuess(
                            game_num,
                            row[1],
                            row[2],
                            row[3],
                            row[4],
                            row[5],
                        )

                        data.append(item)
                    else:
                        # looks like this is the
                        # end of the file, so
                        # return the data
                        return data
                except csv.Error as e:
                    # looks like something broke
                    # so skip this line
                    print(e)
                    continue
                finally:
                    # incriment the row number
                    row_num += 1
        return data