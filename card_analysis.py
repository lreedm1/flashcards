from re import X
import string as punctuation_list
import timeit

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
    def replace_illegal_and_split(terms_and_defs):
        def count_faster(string):   
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
                    if x-y > 3:
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
        illegal_characters = illegal_characters.replace("'", "")
        illegal_characters = illegal_characters.replace("’", "")
        
        print("Replacing illegal characters...")
        for i in illegal_characters:
            words = words.replace("'", "’")
            words = words.replace(i, " ")
            words = words.replace("’s", "  ")

        words = words.split() # convert y into a list of words by splitting on spaces
        words = [i for i in words if len(i) > 1] # remove words that are 1 character long
        words = count_faster(words) # create a list of all unique words and their counts
        # sort the list by the count of the word
        words.sort(key=lambda x: x[1], reverse=True)
        # convert words to a dictionary
        words = {words[i][0]:i for i in range(len(words))}
        return words
    def write_card_stats(terms, directory, file_name='stats.md'):
        cards_to_print = []
        print_statement = ""
        for i in terms:
            scalar = round(terms[i] * 100)
            print_statement += f"{scalar} - {i}\n"
        
        write(directory + "/" + file_name, print_statement)     
        print("Wrote word statistics to the file 'statistics_filename.md'")

    words = replace_illegal_and_split(x)
    dictionary = find_words_in_dictionary(words, dictionary_path)

    #for i in dictionary:
        #input(f'{i} - {dictionary[i][0]}')
    scores = []
    for i in dictionary:
        x = dictionary[i][0]
        scores.append([dictionary[i][0],i])
    
    scores.sort(key=lambda x: x[0], reverse=True)
    differences = [[i[1],i[0] - dictionary[i[1]][1]] for i in scores]
    differences.sort(key=lambda x: x[1], reverse=True)
    # normalize all scores to be between 0 and 1
    span = differences[0][1] - differences[-1][1]
    min = differences[-1][1]
    for i in range(len(differences)):
        differences[i][1] = (differences[i][1] - min) / span  

    dictionary2 = {i[0]:i[1] for i in differences}
    write_card_stats(dictionary2, directory)

    return True

def find_words_in_dictionary(words, dictionary_path):
    words_in_dictionary = {}
    start = timeit.default_timer()    
    with open(dictionary_path, 'r') as f:
        dictionary_list = f.read().split(',')
    dictionary = {}
    x = 0
    for i in dictionary_list:
        dictionary[i] = x
        x += 1
    for i in words:
        try:
            words_in_dictionary[i] = [dictionary[i], words[i]]
            #input(words_in_dictionary[i][0])
        except KeyError:
            pass
    end = timeit.default_timer()
    print(f"Time taken to find words in the dictionary: {end - start}")
    return words_in_dictionary

def write(filename, statement):
    with open(filename, 'w') as f:
        f.write(statement)
    return None 