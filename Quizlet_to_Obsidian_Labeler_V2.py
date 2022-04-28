import timeit
from titlecase import titlecase
from card_analysis import make_connections, weight_cards, write

dataset = "/Users/reed/Documents/Nightly/bio test set.txt"
dictionary = "/Users/reed/Documents/Nightly/punc_free_dictionary.txt"
directory = "/Users/reed/Library/Mobile Documents/iCloud~md~obsidian/Documents/biology test"

def user_input(prompt, responses, error_message):
    while True:
        x = input(prompt)
        if x in responses:
            return x
        elif x == 'q':
            quit()
        else:
            print(error_message)
            continue

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
    
    cards = {}
    for i in contents:
        try:
            for j in i:
                j = j.strip()
                if len(i[0]) > 1 and len(i[1]) > 1:
                    i[0] = titlecase_plus(i[0])
                    i[1] = i[1][0].upper() + i[1][1:]
                    if i[1][-1] == '.':
                        i[1] = i[1][:-1]
                    cards[i[0]] = i[1]
        except IndexError:
            print(f'{i} improperly formatted')
    print("Terms created")
    return cards

def write_cards(cards, directory):
    print("writing cards")
    for i in cards:
        filename = f'{directory}/{i}.md'
        write(filename, cards[i])
    print('cards written to disk')
 
def remove_duplicates(cards):
    no_duplicates = {}
    for i in cards:
        if i not in no_duplicates:
            no_duplicates[i] = [cards[i]]
        else:
            no_duplicates[i].append(cards[i])
    return no_duplicates

def format_cards(cards, connections, scores):
    def format_outbound(outbound, formatted_text, card):
        formatted_sections = [[0,0]]
        if outbound == []:
            return formatted_text
        outbound = sorted(outbound, key=lambda x: len(x), reverse=True)
        formatted_text_static = formatted_text.lower()
        #input(f'connections: {outbound}')
        for i in outbound:
            #input(f'i: {i}')
            start = formatted_text_static.find(i.lower())
            if start == -1:
                print(f'{i} not found in {formatted_text}')
                continue
            end = start + len(i)
            x = 0
            for j in range(len(formatted_sections)):
                if start >= formatted_sections[j][0] and start <= formatted_sections[j][1]:
                    print(f'{i} overlaps with {formatted_text[formatted_sections[j][0]:formatted_sections[j][1]]}, {card}')
                    x = 1
            if x == 1:
                continue
            formatted_sections.append([start, end])
            start = formatted_text.lower().find(i.lower())
            end = start + len(i)
            insertion = "[[" + i + "|" + formatted_text[start:end] + "]]"
            formatted_text = formatted_text[:start] + insertion + formatted_text[end:]
        return formatted_text

    print("formatting cards")
    for card in cards:
        text = cards[card]
        definitions = len(text)
        if definitions != 1:
            x = 1
            for definition in text:
                formatted_text = f'Definition {x}:\n{definition}'
                x += 1
        else:
            formatted_text = text[0]
        outbound, inbound = connections[card]
        formatted_text = format_outbound(outbound, formatted_text, card)
        formatted_text += f'\n\nScore - {scores[card]}'
        if len(inbound) != 0:
            for a,i in enumerate(inbound):
                inbound[a] = [scores[i], i]
            inbound = sorted(inbound, key=lambda x: x[0], reverse=True)
            for i in inbound:
                formatted_text += f'\n[[{i[1]}]] - {i[0]}'
        
        cards[card] = formatted_text
    return cards
        
def stop_append(stop):
    stop.append(timeit.default_timer())

def main():
    stop = []
    stop_append(stop)

    cards = make_directory(dataset)
    stop_append(stop)

    cards = remove_duplicates(cards)
    stop_append(stop)

    connections = make_connections(cards)
    stop_append(stop)

    scores = weight_cards(connections, directory)
    stop_append(stop)
    
    cards = format_cards(cards, connections, scores)

    write_cards(cards, directory)
    stop_append(stop)
    for i in range(1, len(stop)):
        print(f'{round(stop[i] - stop[i-1],2)} seconds')
    print(f'total: {round(stop[-1] - stop[0],2)} seconds')
    
main()