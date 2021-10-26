import os
import random
import pandas as pd
from operator import itemgetter
from openpyxl import load_workbook

file = '/Users/reed/Documents/Flashcard Terms.xlsx'
xslx = pd.ExcelFile(file)
sheets = []

for sheet in xslx.sheet_names:
    sheets += [sheet]

commands = ["n - New card", "e - Edit card", "t - Test me", "b - Back", "q - Quit"]
letters = []
for command in commands:
    letters.append(command[0])


def edit(row, term, definition, df):
    clear()
    print(f'{df.iat[row, term]}\n{df.iat[row, definition]}\n')
    df.iat[row, term] = input("New term: ")
    df.iat[row, definition] = input("New definition: ")
    return ()


def subject_loop(source, location):
    while True:

        raw_ints = []
        raw_strings = []
        selected_units = []

        for i in range(0, df.shape[1]):
            if str(df.columns[i]).endswith("Terms"):  # finds units for user to select
                raw_strings.append(df.columns[i])
                raw_ints.append(i)

        # ask for units user wants to be quizzed on and removes duplicates
        units = select(raw_strings, 'Select a unit or multiple using commas:')
        if units == 'b':
            return
        # determine if user will be quizzed on terms, definitions, or both and if columns are valid
        for i in str(units):
            i = int(raw_ints[int(i)])
            for row in range(df.shape[0] - 1, 0, -1):
                if not pd.isnull(df.iat[row, i]):

                    if df.columns[i + 2].startswith("Term Score"):
                        selected_units.append([i, i + 1, row, i + 2])

                        if df.columns[i + 3].startswith("Definition Score"):
                            selected_units.append([i + 1, i, row, i + 3])
                        break
                    elif df.columns[selected_units + 2].startswith("Definition Score"):
                        selected_units.append([i + 1, i, row, i + 2])
                        break
                    else:
                        print(f"Column {selected_units + 2} is not named 'Term Score' or  'Definition Score', "
                              f"it is equal to {df.columns[selected_units + 2]}")
                        quit()

            else:
                print(f'Unit {i} is blank')  # if unit is blank, panic and notify user
                quit()

        cards = []
        for unit in selected_units:  # build list of cards excluding blanks
            for row in range(0, unit[2]):
                # skip if term or definition is blank
                if pd.isnull(df.iat[row, unit[0]]) or pd.isnull(df.iat[row, unit[1]]):
                    continue
                # set score to zero if  blank
                elif pd.isnull(df.iat[row, unit[3]]):
                    cards.append([row, unit[0], unit[1], unit[3], 0])
                else:
                    cards.append([row, unit[0], unit[1], unit[3], df.iat[row, unit[3]]])

        # save nulls as zeroes to reduce computation next time
        with pd.ExcelWriter(source, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=location, index=False)

        # quizzing loop
        clear()
        positive_increment = 1
        negative_increment = -1
        median_percent = 5  # must be value between 0 and 100
        expovar = 100 / (len(cards) * median_percent)  # calculate the value for expovariate

        while True:
            # sort the list
            cards.sort(key=itemgetter(4))
            # exponentially distribute cards with min @ lowest value
            knowledge_level = cards[int(random.expovariate(expovar))][4]

            potential_cards = []

            # randomly select card within knowledge level
            for i in range(0, len(cards)):
                if cards[i][4] == knowledge_level:
                    potential_cards.append(i)
                elif cards[i][4] > knowledge_level:
                    break

            x = random.randint(potential_cards[0], potential_cards[-1])

            card = cards[random.randint(potential_cards[0], potential_cards[-1])]

            input(f'{df.iat[card[0], card[1]]}\n')  # print first term.
            clear()
            print(f'{df.iat[card[0], card[1]]} - {round(int(card[4]))}\n{df.iat[card[0], card[2]]}')
            # print("\nDid you know that term?\ny - Yes\nn - No")
            key = input()  # print both terms & ask for input
            clear()

            if key == "e":
                edit(card[0], card[1], card[2], df)
            elif key == "y":  # TODO: Detect keys using tkinter
                score(card[0], card[3], positive_increment, df)  # TODO: Tkinter application???
            elif key == "n":
                score(card[0], card[3], negative_increment, df)
            elif key == "q":
                quit()
            elif key == "b":
                clear()
                return ()
            else:
                continue

            # save changes
            with pd.ExcelWriter(source, mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=location, index=False)


def score(row, column, increment, df):
    if pd.isnull(df.iat[row, column]):
        df.iat[row, column] = int(0)
    df.iat[row, column] = int(df.iat[row, column]) + increment


def clear():
    os.system('clear')


def get_ints(first, last, source, prompt, length):
    while True:
        # print selected commands
        print(prompt, "\n")

        for i in range(first, last):
            print(f'{i} - {source[i]}')
        numbers = set(input("\n").split(","))
        clear()

        # check for length
        if len(numbers) > length:
            print(f'Too many values')
        # check if each input is a number
        else:
            for i in numbers:
                if i.isdigit() and first <= int(i) <= last:
                    return int(i)
                elif i == "b":
                    return "b"
                elif i == "q":
                    quit()
                else:
                    print(f'{i} is not a valid number')


def select(selection, input_statement):
    while True:
        selected = get_ints(0, len(selection), selection, input_statement, 1)
        clear()
        if selected == "b":
            return "b"
        else:
            return selected


while True:
    sheet = select(sheets, "Select a sheet:")
    clear()
    if sheet == "b":
        continue
    else:
        df = pd.read_excel(file, sheet)
        if df.shape == (0, 0):
            print("Sheet is blank!")
        else:
            subject_loop(file, sheets[sheet])
