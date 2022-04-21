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

    normalized_terms = {i: [normalize(i,0),normalize(j,1)] for i in terms for j in terms[i]}

    print("Searching for connections...")
    connections = find_connections(normalized_terms)        
    return connections

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