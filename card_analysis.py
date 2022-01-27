import timeit
punctuation_list = '!#$%&()*+,-./:;<=>?@[\]^_`{|}~'

def make_connections(terms):
    def normalize(string, mode):
        string = string.lower()
        string = " " + string + " "
        string = string.replace("/", "or")
        string = string.replace('\\', 'or')

        for i in punctuation_list:
            string = string.replace(i, " ")
        if mode == 0: #term
            string = string.lower()
            if "(" in string:
                x = [string.find("("), string.find(")")]
                string = [" " + string[:x[0]].strip() + " " + string[x[1]+1:].strip() + " ",
                " " + string[x[0]+1:x[1]].strip() + " "]
            return [string]
        elif mode == 1: #definition
            return string
    def find_connections(dictionary):
        connections = {i:[[],[]] for i in dictionary}
        for i in dictionary:
            terms = dictionary[i][0]
            for j in dictionary:
                if i == j: continue
                for k in terms:
                    if k in dictionary[j][1]:
                        connections[j][0].append(i)
                        connections[i][1].append(j)
                        break
        return connections
    print("Making connections...")
    normalized_terms = {i: [normalize(i,0),normalize(terms[i],1)] for i in terms}

    print("Searching for connections...")
    term_connections = find_connections(normalized_terms)

    print("Writing connections to terms...")
    for i in terms:
        definition = terms[i]
        outbound_connections, inbound_connections = term_connections[i]
        if outbound_connections != []:
            definition += "\n\nOutbound Connections:"
            for j in outbound_connections:
                definition += "\n[[" + j + "]]"
        if inbound_connections != []:
            definition += "\n\nInbound Connections"
            for j in inbound_connections:
                definition += "\n[[" + j + "]]"
        terms[i] = definition
    return terms, normalized_terms

def weight_words(terms_and_defs, dictionary_path, directory, file_name='stats.md'):
    words = ''
    for i in terms_and_defs:
        words += i + ' ' + terms_and_defs[i] + ' '
    words = words.lower()
    illegal_characters = punctuation_list.replace("’", " ")
    for i in illegal_characters:
        words = words.replace("'", "’")
        words = words.replace(i, " ")

    words = words.split(" ")
    words = [i for i in words if len(i) > 1]
    print("Counting...")
    counted = {}
    for i in words:
        try:
            counted[i] += 1
        except KeyError:
            counted[i] = 1
    words = [[i[0], i[1]] for i in counted.items() if i[1] > 1]
    words.sort(key=lambda x: x[1])
        
    counts = find_words_in_dictionary(words, dictionary_path)

    counts.sort(key=lambda x: x[1])
    scores = [[j[0],j[2] - i] for i, j in enumerate(counts)]
    scores.sort(key=lambda x: x[1])

    max, min = scores[0][1], scores[-1][1]
    scores = [[i[0], (i[1] - min) / (max - min)] for i in scores]
    scores_dict = {i[0]: i[1] for i in scores}
    scores = [[j[0], scores_dict[j[0]] * (j[3]**.5)] for j in counts]
    scores.sort(key=lambda x: x[1], reverse=True)
    max, min = scores[0][1], scores[-1][1]
    scores = [[i[0], (i[1] - min) / (max - min)] for i in scores]
    scores.sort(key=lambda x: x[1], reverse=True)

    print_statement = ""
    for i in scores:
        scalar = round(i[1] * 100)
        print_statement += f"{scalar} - {i[0]}\n"
    write(directory + "/" + file_name, print_statement)
    print("Wrote word statistics to the file 'statistics_filename.md'")
    return scores

def find_words_in_dictionary(words, dictionary_path):
    start = timeit.default_timer()    
    with open(dictionary_path, 'r') as f:
        dictionary = {j:i for i,j in enumerate(f.read().split(','))}
    stop = timeit.default_timer()
    print(f'time to read dictionary: {stop - start}')
    words_in_dictionary = []
    for i in range(len(words)):
        try:
            word = words[i][0]
            count = words[i][1]
            words_in_dictionary.append([word,dictionary[word], i, count])
        except KeyError:
            pass
    return words_in_dictionary

def write(filename, statement):
    with open(filename, 'w') as f:
        f.write(statement)
    return None 