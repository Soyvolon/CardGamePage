import csv
import os
from .card_game_grouping import CardGameGrouping
from .card_guess import CardGuess

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