import os
from titlecase import titlecase
import re
directory = "/Users/reed/Library/Mobile Documents/iCloud~md~obsidian/Documents/alpha/"

def get_files(directory, debug): # Get the names of all the files in the directory
    files = []
    for file in os.listdir(directory):
        if file.endswith(".md") and file[0] != '.':
            files.append(file)
    Print("List of files compiled", debug)
    Print(files, debug)
    return files

def titlecase_plus(string): # run the string through titlecase but allow for acronyms
    split_on_space = re.split('\s+', string) # split the string on spaces
    acronyms = []
    for i in range(len(split_on_space)): 
        if split_on_space[i].upper() == split_on_space[i]: # if the word is all caps, add it to the acronyms list
            length = len(split_on_space[i])
            start = string.find(split_on_space[i])
            acronyms.append([start, start + length, split_on_space[i]])
        
    string_titlecase = titlecase(string)
    for i in acronyms: # replace the acronyms with the original capitalization
        string_titlecase = string_titlecase[:i[0]] + i[2] + string_titlecase[i[1]:]

    return string_titlecase

def clear(debug): # Clear the screen if debug is True
    if not debug:
        os.system('clear && printf "\e[3J"')

def user_input(prompt, responses, error_message): # Ask the user a question and return their response
    while True:
        x = input(prompt)
        if x in responses:
            return x
        elif x == 'q':
            quit()
        else:
            print(error_message)
            continue

def _debug(): # Ask the user if they want to run in debug mode
    debug = user_input("Run in debug mode? (Y/n) ", ['y', 'n', ''], 'Please enter a command')
    if debug == 'y' or debug == "":
        return True
    else:
        clear(False)
        return False

def Print(string, debug): # Print the string if debug is True
    if debug:
        print(string)

def make_references(links, files, debug): # Create all files that are referenced but do not exist
    Print("Creating files for all links", debug)
    for link in links:
        link = link + ".md"
        if link not in files:
            with open(directory + link, "w") as f:
                f.write('')
            files.append(link)
            Print(f'Created {link}', debug)
    return files

def standardize_links(files, debug): # Standardize all links to sentence case
    Print("Standardizing links", debug)

    links_master = []
    for i in range(len(files)):
        file = files[i]
        with open(directory + "/" + file, "r") as f:
            contents = f.read()

        links = re.findall(r'\[\[(.*?)\]\]', contents) # find double brackets and list if they contain a pipe
        for link in links:
            standardized = format(link, debug, True)
            pipe = link.find("|")
            if pipe == -1:
                pipe = len(link)
            if link[:pipe] != standardized:
                Print(f'-----{file}----- \n[[{link}]] -----> [[{standardized + link[pipe:]}]]\n', debug)
                contents = contents.replace(link, standardized + link[pipe:], 1)
                with open(directory + "/" + file, "w") as f:
                    f.write(contents)
                
            if standardized not in links_master:
                links_master.append(standardized)
    return links_master

def format(string, debug,capitalization): # Remove pipe, and capitalize if needed
    if string.find("|") != -1:  # Remove pipe and trailing text
        string = string[:string.find('|')]

    if  capitalization:
        string = string.strip()    # Remove whitespace
        string = titlecase_plus(string)
    return string

def normalize_file_names(files, debug): # Normalize all file names to sentence case
    Print("Normalizing file names", debug)
    for i in range(len(files)):
        file = files[i]
        file_formatted = titlecase_plus(file)
        # Remove the .md extension, strip leading and trailing whitespace, then add the .md extension
        file_formatted = file_formatted[:-3].strip() + ".md"

        if file != file_formatted: # Compare the file versus the titlecase_plus file and print if they are different
            Print(f'"{file}" is not sentence case, renaming to {file_formatted}', debug)
            os.rename(directory + file, directory + file_formatted)
            files[i] = file_formatted
    return files

def read_labels(files, debug): # Get all the labels (#)
    Print("Getting labels", debug)
    labels_master = []
    labels_master_count = []
    for file in files:
        with open(directory + "/" + file, "r") as f:
            contents = f.read()
        
        labels = re.findall(r'#(.*?)(\s|\n)', contents) # Find all hashtags and the content after them until a space or newline
        for label in labels:
            label = label[0]
            
            if label not in labels_master: # If the label is not in the master list, add it to the master list and a count of 1 to the master count list
                labels_master.append(label)
                labels_master_count.append(1)
            
            else: # If the label is in the master list, increment the count of that label in the master count list
                labels_master_count[labels_master.index(label)] += 1
 
    # sort the master list by the count of the label by zipping the master list and the master count list together, then sort by the count
    labels_master = sorted(zip(labels_master, labels_master_count), key=lambda x: x[1], reverse=True)
    # print the labels and their counts
    for i in range(len(labels_master)):
        Print(f'{labels_master[i][0]} ({labels_master[i][1]})', debug)
    labels_master = [x[0] for x in labels_master] # Unzip the list and return the master list
    return labels_master

def label(files, debug, labels): # Create all labels that do not exist
    Print("Creating labels", debug)
    for file in files:
        with open(directory + "/" + file, "r") as f:
            contents = f.read()
        
        if contents.find("#") != -1: # Check if the file has any labels
            continue

        if len(contents) == 0: # Label empty files with #todo
            with open(directory + file, "w") as f:
                f.write("#todo\n")
            Print(f'Labeled {file} with #todo', debug)
            continue

        for label in labels:
            choice = user_input(f'{file} \n {contents}\nLabel "{file}" {label}? (Y/n) ', ['y', 'n', ''], 'Please enter a command')
            if choice == 'y' or choice == "": 
                contents = label + "\n" + contents
                with open(directory + file, "w") as f:
                    f.write(contents)
                Print(f'Labeled {file} with {label}', debug)                    


def main():
    print("Welcome to the Obsidian-Fixer program!")

    debug = _debug() # Ask the user if they want to run in debug mode

    files = get_files(directory, debug) # Find the names of all the files in the directory

    normalize_file_names(files, debug) # Normalize file names to sentence case
    
    links = standardize_links(files, debug) # Standardize links to sentence case

    files = make_references(links, files, debug) # Create all files that are referenced but do not exist

    # Add date created to all files without it and add / modify date modified
    #check_dates(files, debug)

 
    labels = read_labels(files, debug)  # Read all files and complie a list of all the labels
    
    # Label all blank files #todo
    # Ask the user to label all blank, unlabaled files
    label(files, debug, labels)

main()