




def weight(x, dictionary_path, directory): 
    words = ''
    for i in x:
        for j in i:
            words += j + ' '
    words = words.lower()
    # replace all punctuation with a space except for "–" and "'"
    illegal_characters = punctuation_list.punctuation
    illegal_characters = illegal_characters.replace("–", "")
    illegal_characters = illegal_characters.replace("'", "")
    illegal_characters = illegal_characters.replace("’", "")
    
    print("Replacing illegal characters...")
    for i in illegal_characters:
        words = words.replace("'", "’")
        words = words.replace(i, "")
        words = words.replace("’s", "")

    words = words.split() # convert y into a list of words by splitting on spaces
    words = [i for i in words if len(i) > 1] # remove words that are 1 character long
    words = count_faster(words) # create a list of all unique words and their counts
    words = [i for i in words if i[1] != 1] # remove all words with a count of 1
    words.sort(key=lambda x: x[1], reverse=True) # sort the list of words by their counts
    #  if the second to last    


    # read the dictionary and save it to a variable called dictionary using pandas
    # it is a text file with one word per line and the number of times the word appears in the text seperated by ","
    dictionary = pd.read_csv(dictionary_path, sep=',', header=None)
    # seperate the words and their counts into two tuples
    dictionary_words = dictionary[0].tolist()
    dictionary_words = [str(i).lower() for i in dictionary_words]
    dictionary_counts = dictionary[1].tolist()
   
    

    words_in_dictionary = []
    # if the word is in the dictionary, save it to words_in_dictionary in the fomrat [word, count, dictionary count, dictionary index]
    for i in range(len(words)):
        try:
            x = dictionary_words.index(words[i][0])
            words_in_dictionary.append([words[i][0], words[i][1], dictionary_counts[x], x])
        except ValueError:
            continue

    # create a list called sorted by card count that contains 
    # the words in words_in_dictionary sorted by their counts
    # frequency is used to provide the freqency of each word
    # more efficiently than sorting the list of words_in_dictionary again
    words_in_dictionary.sort(key=lambda x: x[1])
    sorted_by_card_count = []
    frequency = []
    for i in range(len(words_in_dictionary)):
        sorted_by_card_count.append(words_in_dictionary[i][0])
        frequency.append(words_in_dictionary[i][1])


    # for the terms which exist with a trailing s and without a traling s
    # add the count of their counterpart to the count of the term
    # this is to account for the fact that the dictionary counts the s as a different word
    for i in range(len(words_in_dictionary)):
        if words_in_dictionary[i][0][-1] == 's':
            try:
                x = sorted_by_card_count.index(words_in_dictionary[i][0][:-1])
                words_in_dictionary[i][1] += words_in_dictionary[x][1]
                words_in_dictionary[x][1] += words_in_dictionary[i][1]
            except ValueError:
                continue

    words_in_dictionary.sort(key=lambda x: x[2])
    sorted_by_dictionary_count = []
    for i in range(len(words_in_dictionary)):
        sorted_by_dictionary_count.append(words_in_dictionary[i][0])

    
    
    difference = []
    for i in range(len(words_in_dictionary)):
        card_count = sorted_by_card_count[i]
        for j in range(len(words_in_dictionary)):
            if sorted_by_dictionary_count[j] == card_count:
                difference.append([card_count,(j-i)*-1])
                break

    
    
    
    
    
    difference.sort(key=lambda x: x[1], reverse=True)
    
    # set all scores that are less than 0 to 0
    # if the term contains a trailing s and it has a counterpart
    # set the score of both to be the highest score
    # if the term or the counterpart has a negative score, set the score to 0
    for i in range(len(difference)):
        if difference[i][1] < 0:
            difference[i][1] = 0
        if difference[i][0][-1] == 's':
            try:
                x = sorted_by_card_count.index(difference[i][0][:-1])
                if difference[i][1] > difference[x][1] and difference[x][1] > 0:
                    difference[i][1] = difference[x][1]
                else:
                    difference[x][1] = difference[i][1]
            except ValueError:
                continue
    for i in range(len(difference)):
        print(i)
        print(difference[i])

    # normalize all scores to be between 0 and 1
    max = difference[0][1]
    for i in range(len(difference)):
        difference[i][1] = difference[i][1]/max    


    # print the terms and their weights to a file
    # if the term contains a trailing s, try to find the counterpart without a trailing s
    cards_to_print = []
    for i in range(len(difference)):
            if difference[i][0][-1] == 's':
                try:
                    print("try")
                    x = sorted_by_card_count.index(difference[i][0][:-1])
                except ValueError:
                    print("value error")
                    cards_to_print.append([difference[i][0], difference[i][1]])
            else:
                print("else")
                cards_to_print.append([difference[i][0], difference[i][1]])
            
    cards_to_print.sort(key=lambda x: x[1], reverse=True)
    with open(directory + '/' + 'card_statistics.md', 'w') as f:
        for i in cards_to_print:
            print(i)
            f.write(str(round(i[1] / 100)) + ' - ' + i[0] + '\n')

            
    print("Wrote word statistics to the file 'card_statistics.md'")

    input("Press enter to continue...")


    return None