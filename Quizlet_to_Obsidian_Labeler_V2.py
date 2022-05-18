import timeit
from titlecase import titlecase
from card_analysis import make_connections, weight_cards, write, normalize

dataset = "/Users/reed/Documents/Nightly/bio test set.txt"
directory = "/Users/reed/Library/Mobile Documents/iCloud~md~obsidian/Documents/biology test"

def make_directory(file):
    def titlecase_plus(text):
        text = text.replace('/', ' or ')
        text = text.replace('\\', ' or ')
        split_on_space = text.split(' ')
        acronyms = []
        for i in split_on_space: 
            for j in i:
                if j.isupper():
                    length = len(i)
                    start = text.find(i)
                    acronyms.append([start, start + length, i])
                    break
            
        string_titlecase = titlecase(text)
        for i in acronyms:
            string_titlecase = string_titlecase[:i[0]] + i[2] + string_titlecase[i[1]:]

        return string_titlecase
    with open(file , 'r') as f:
        contents = f.read()
    contents = contents.replace(';;;;;', ';;;  ')
    contents = contents.split(";;;")
    contents = [x.split(';;') for x in contents]
    
    cards = []
    for i in contents:
        try:
            for j in i:
                j = j.strip()
            if len(i[0]) > 1 and len(i[1]) > 1:
                i[0] = titlecase_plus(i[0])
                i[1] = i[1][0].upper() + i[1][1:]
                if i[1][-1] == '.':
                    i[1] = i[1][:-1]
                cards.append(i)
        except IndexError:
            print(f'{i} improperly formatted')
    print("Terms created")
    return cards

def write_cards(cards, directory):
    print("writing cards")
    for i in cards:
        filename = f'{directory}/{i[0]}.md'
        write(filename, i[1])
    print('cards written to disk')

def format_cards(card_pairs, connections, scores):
    def format_definition(outbound_connections, card_pair, card_pairs):
        if len(card_pair[0][1]) != 1:
            statement = '**Definition 1:**\n'
            formatted = statement + card_pair[1][1][0]
            unformatted =  ' ' + ' ' * len(statement) + card_pair[0][1][0]
            for a in range(len(card_pair[0][1])-1):
                statement = f'\n\n**Definition {a+2}:**\n'
                formatted += statement + card_pair[1][1][a+1]
                unformatted += ' ' * len(statement) + card_pair[0][1][a+1]
        else:
            formatted = card_pair[1][1][0]
            unformatted = ' ' + card_pair[0][1][0]
        if len(outbound_connections) == 0:
            return formatted
        sorted_connections = []
        for i in outbound_connections:
            sorted_connections.append([sorted(card_pairs[i][0][0],key = len, reverse = True), card_pairs[i][1][0]])
        sorted_connections = sorted(sorted_connections, key = lambda x: len(x[0][0]), reverse = True)
        
        for i in sorted_connections:    
            for j in i[0]:
                location = unformatted.find(j)
                if location != -1:
                    length = len(j) -2
                    statement = f'[[{i[1]}|{formatted[location:location + length]}]]'
                    formatted = formatted[:location] + statement + formatted[location + length:]
                    unformatted = unformatted[:location] + ' ' * len(statement) + unformatted[location + length:]
        return formatted
    print("formatting cards")
    cards_print = []
    for a, card_pair in enumerate(card_pairs):
        outbound, inbound = connections[a]
        formatted_text = format_definition(outbound, card_pair, card_pairs)
        formatted_text += f'\n\nScore - {scores[a][1]}'
        if len(inbound) != 0:
            inbound_print = []
            for j in inbound:
                inbound_print.append([card_pairs[j][1], scores[j][1]])
            inbound_print = sorted(inbound_print, key=lambda x: x[1], reverse=True)
            for j in inbound_print:
                formatted_text += f'\n[[{j[0][0]}]] - {j[1]}'
        cards_print.append([card_pair[1][0], formatted_text])
    return cards_print
        
def stop_append(stop):
    stop.append(timeit.default_timer())

def print_times(stop):
        for i in range(1, len(stop)):
            print(f'{round(stop[i] - stop[i-1],2)} seconds')
        print(f'total: {round(stop[-1] - stop[0],2)} seconds')

def main():
    stop = []
    stop_append(stop)

    cards = make_directory(dataset)
    stop_append(stop)

    card_pairs = normalize(cards)
    stop_append(stop)
    
    connections = make_connections(card_pairs)
    stop_append(stop)

    scores = weight_cards(connections, card_pairs, directory)
    stop_append(stop)

    cards = format_cards(card_pairs, connections, scores)
    stop_append(stop)

    write_cards(cards, directory)
    stop_append(stop)

    print_times(stop)
main()