from calendar import c
import string as punctuation_list
import pandas as pd

def make_connections(terms, scores):
    def normalize(string, mode):
        if mode == 0: #term
            string = string.lower()
            # split the string if it contaiins text within parentheses
            if "(" in string:
                x = [string.find("("), string.find(")")]
                string = [string[:x[0]] + string[x[1]+1:], string[x[0]+1:x[1]]]
            else:
                string = [string]
        if mode == 1: #definition
            string = string.lower()
            string = " " + string + " "
            string = string.replace("/", "or")
            string = string.replace('\\', 'or')
            # replae all punctuation with a space
            for i in punctuation_list.punctuation:
                string = string.replace(i, " ")
        return string
    def find_connections(len,terms, definitions):
        connections = []
        for i in len:
            definition = definitions[i]
            for j in len:
                if i == j:
                    continue
                term = terms[j][0]
                term_no_s = f' {term} '
                term_s = f' {term}s '
                if term_no_s in definition or term_s in definition:
                    connections.append([i,j])
        return connections
    def format_connections(connections, mode, length):
        if mode == "inbound":
            mode = 1
        elif mode == "outbound":
            mode = 0
        mode2 = 1 - mode
        connections.sort(key=lambda x: x[mode])
        formatted_connections = [[connections[0][mode], [connections[0][mode2]]]]
        for i in range(1, len(connections)):
            current = connections[i][mode]
            previous = connections[i-1][mode]
            if current == previous:
                formatted_connections[-1][1].append(connections[i][mode2])
            else:
                formatted_connections.append([connections[i][mode], [connections[i][mode2]]])
        # create emtpty lists for the connections that are not in the list
        for i in length:
            try:
                if formatted_connections[i][0] != i:
                    formatted_connections.insert(i, [i, []])
            except IndexError:
                formatted_connections.append([i, []])
        for i in length:
            formatted_connections[i] = formatted_connections[i][1]
        return formatted_connections
        
    print("Making connections...")
    normalized_terms_list, normalized_definitions_list = [],[]
    length = range(len(terms))
    for i in length:
        normalized_terms_list.append(normalize(terms[i][0], 0))
        normalized_definitions_list.append(normalize(terms[i][1], 1))


    print("Searching for connections...")
    term_connections = find_connections(length, normalized_terms_list, normalized_definitions_list)
    inbound_connections = format_connections(term_connections, "inbound", length)
    outbound_connections = format_connections(term_connections, "outbound", length)
    print("Writing connections to terms...")
    for i in range(len(terms)):
        terms[i][1] += "\n\nOutbound connections:"
        for j in outbound_connections[i]:
            j = "\n[[" + terms[j][0] +  "]]"
            terms[i][1] += j
        terms[i][1] += "\n\nInbound connections:"
        for j in inbound_connections[i]:
            j = "\n[[" + terms[j][0] +  "]]"
            terms[i][1] += j
    return terms

def weight(x, dictionary_path, directory): 
    words = replace_illegal_and_split(x)
    words_in_dictionary = find_words_in_dictionary(words, dictionary_path)
    
    # create a list called sorted by card count that contains 
    # the words in words_in_dictionary sorted by their counts
    # frequency is used to provide the freqency of each word
    # more efficiently than sorting the list of words_in_dictionary again
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

    write_card_stats(difference, sorted_by_card_count, directory)

    return True

def find_words_in_dictionary(words, dictionary_path):
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

    words_in_dictionary.sort(key=lambda x: x[1])
    return words_in_dictionary


def rescore_trailing_s(terms, scores):
    for i in range(len(terms)):
        if terms[i][0][-1] == 's':
            try:
                x = terms.index(terms[i][0][:-1])
                scores[i] += scores[x]
                scores[x] += scores[i]
            except ValueError:
                continue
    return scores


def write_card_stats(terms, sorted_terms, directory, file_name='stats.md'):
     # print the terms and their weights to a file
    # if the term contains a trailing s, try to find the counterpart without a trailing s
    cards_to_print = []
    for i in range(len(terms)):
            if terms[i][0][-1] == 's':
                try:
                    sorted_terms.index(terms[i][0][:-1])
                except ValueError:
                    cards_to_print.append([terms[i][0], terms[i][1]])
            else:
                cards_to_print.append([terms[i][0], terms[i][1]])
            
    cards_to_print.sort(key=lambda x: x[1], reverse=True)
    
    # convert the list of cards to a string for writing
    print_statement = ""
    for i in range(len(cards_to_print)):
        scalar = round(cards_to_print[i][1] * 100)
        print_statement += f"{scalar} - {cards_to_print[i][0]}\n"
    
    print(print_statement)
    write(directory + "/" + file_name, print_statement)     
    print("Wrote word statistics to the file 'statistics_filename.md'")


def replace_illegal_and_split(terms_and_defs):
    def count_faster(string):   
        print("Sorting...")
        string.sort()
        print("Counting...")
        x = 0
        counted = []
        while True:
            y = x
            try:
                while string[y] == string[x+1]:
                    x += 1
                x += 1
                counted.append([string[x-1], x-y])
            except IndexError:
                return counted   
    # combine terms_and_defs with spaces
    words = ''
    for i in terms_and_defs:
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

    return words


def write(filename, statement):
    with open(filename, 'w') as f:
        f.write(statement)
    return None