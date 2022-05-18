punctuation_list = '!#$%&()*+,-./:;<=>?@[\]^_`{|}~'

def normalize(dictionary):
    def remove_duplicates(pairs):
        for a in range(len(pairs)):
            if pairs[a] == 0:
                continue
            for j in pairs[a][0]:
                for c in range(len(pairs)):
                    if pairs[c] == 0 or c == a:
                        continue
                    if j not in pairs[c][0]:
                        continue
                    for d, l in enumerate(pairs[a][0]):
                        if l not in pairs[c][0]:
                            pairs[c] = (pairs[c][0] + [l], pairs[c][1] + [pairs[a][1][d]])
                    pairs[a] = 0
                    a = c
        pairs = [i for i in pairs if i != 0]
        return pairs
    def split_alternates(string):
        if "(" in string:
            x = [string.find("("), string.find(")")]
            string = [" " + string[:x[0]].strip() + " " + string[x[1]+1:].strip() + " ",
            " " + string[x[0]+1:x[1]].strip() + " "]
            string.append('')
        else:
            string = [string, '']
        return string
    def normalize_spelling(input):
        string = input.lower().strip()
        string = " " + string + " "
        illegal_characters = punctuation_list.replace('-', '')
        for j in illegal_characters:
            string = string.replace(j, " ")
        return string
    print("Normalizing terms...")
    card_pairs = []
    for a, i in enumerate(dictionary):
        new_terms = split_alternates(i[0])
        new_terms[-1] = i[1] + "~"
        new_terms = ([normalize_spelling(j) for j in new_terms], new_terms)
        card_pairs.append(new_terms)
    card_pairs = remove_duplicates(card_pairs)
    for a, i in enumerate(card_pairs):
        new_i = [[[],[]],[[],[]]]
        for b, j in enumerate(i[1]):
            if j[-1] == "~":
                new_i[0][1].append(" " + i[0][b].strip() + " ")
                new_i[1][1].append(" " + i[1][b][:-1] + " ")
            else:
                new_i[0][0].append(i[0][b])
                new_i[1][0].append(i[1][b])
        card_pairs[a] = new_i
    for a, i in enumerate(card_pairs):
            if len(i[1][0]) == 1:
                i[1][0] = i[1][0][0]
                continue
            formatted_uncombined = sorted(i[1][0], key = len, reverse = True)
            card_pairs[a][1][0] = formatted_uncombined[0].strip()
            for i in formatted_uncombined[1:]:
                card_pairs[a][1][0] += f' ({i.strip()})'
    return card_pairs

def make_connections(terms):
    print("Searching for connections...")
    connections = [[(),()] for i in range(len(terms))]
    term_chunks = tuple("".join(i[0][0] + i[0][1]) for i in terms)
    titles = tuple(i[0][0] for i in terms)
    for a, i in enumerate(term_chunks):
        for b, j in enumerate(titles):
            for k in j:
                if a != b and k in i:
                    connections[a][0] += (b,)
                    connections[b][1] += (a,)
                    break
    return connections

def weight_cards(connections, terms, directory, file_name='card stats.md'):
    card_scores = sorted([(a,len(i[0]) *.1 + len(i[1])) for a,i in enumerate(connections)], key=lambda x: x[1], reverse=True)
    max, min = card_scores[0][1], card_scores[-1][1]
    card_scores = [[i[0],(i[1] - min) * 100 / (max - min)] for i in card_scores]
    print_statement = ''
    for a,i in enumerate(card_scores):
        i = (i[0],round(i[1], 1)) if i[1] < 1 else (i[0],round(i[1]))
        card_scores[a] = i
        print_statement += f'{i[1]} - [[{terms[i[0]][1][0]}]]\n'
    write(directory + "/" + file_name, print_statement)
    card_scores.sort(key = lambda x: x[0])
    return card_scores

def write(filename, statement):
    with open(filename, 'w') as f:
        f.write(statement)