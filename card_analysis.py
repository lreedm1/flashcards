import timeit
punctuation_list = '!#$%&()*+,-./:;<=>?@[\]^_`{|}~'

def make_connections(terms):
    def normalize(string, mode):
        string = string.lower()
        string = " " + string + " "
        string = string.replace("/", "or")
        string = string.replace('\\', 'or')
        illegal_characters = punctuation_list.replace('-', '')
        for i in illegal_characters:
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

    #for i in terms:
    #    input(terms[i])

    normalized_terms = {i: [normalize(i,0),normalize(j,1)] for i in terms for j in terms[i]}

    print("Searching for connections...")
    connections = find_connections(normalized_terms)        
    return connections

def weight_words(terms_and_defs, dictionary_path, directory, file_name='word stats.md'):
    words = ''
    for i in terms_and_defs:
        words += i + ' '
        for j in terms_and_defs[i]:
            words += j + ' '
    words = words.lower()
    #import punctuation list as illegal characters but remove the characters "-" and "’" with ""

    illegal_characters = punctuation_list.replace("'", '')
    words = words.replace("'", "’")
    for i in illegal_characters:
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
    words.sort(key=lambda x: x[1], reverse =True)
        
    counts = find_words_in_dictionary(words, dictionary_path)

    counts.sort(key=lambda x: x[1])
    scores = [[j[0],i - j[2]] for i, j in enumerate(counts)]
    scores_dict = {i[0]:i[1] for i in scores}
    max, min = scores[0][1], scores[-1][1]
    scores = [[i[0], (i[1] - min) / (max - min)] for i in scores]
    scores = [[j[0], scores_dict[j[0]] * (j[3])] for j in counts]
    scores.sort(key=lambda x: x[1], reverse=True)
    max, min = scores[0][1], scores[-1][1]
    scores = [[i[0], (i[1] - min) / (max - min)] for i in scores]
    scores.sort(key=lambda x: x[1], reverse=True)

    print_statement = ""
    for i in scores:
        scalar = round(i[1] * 100)
        print_statement += f"{scalar} - {i[0]}\n"
    write(directory + "/" + file_name, print_statement)
    print("Wrote word statistics to the file {file_name}")

    scores_dict = {i[0]:i[1] for i in scores}
    return scores_dict

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

def weight_cards(connections, directory, file_name='card stats.md'):
    card_scores = []
    for i in connections:
        outgoing_count = len(connections[i][0])
        incomming_count = len(connections[i][1])
        score = (outgoing_count + incomming_count) ** .5
        card_scores.append([i,score])
        
    card_scores.sort(key=lambda x: x[1], reverse =True)
    max, min = card_scores[0][1], card_scores[-1][1]
    card_scores = [[i[0], (i[1] - min) / (max - min)] for i in card_scores]
    card_scores = {i[0]:round(i[1] * 100) for i in card_scores}
    print_statement = ''
    for i in card_scores:
        print_statement += f'{card_scores[i]} - [[{i}]]\n'
    write(directory + "/" + file_name, print_statement)
    return card_scores

def write(filename, statement):
    with open(filename, 'w') as f:
        f.write(statement)
    return None 