import os

directory = "/Users/reed/Library/Mobile Documents/iCloud~md~obsidian/Documents/alpha"

def get_files(directory):
    files = []
    #add all files in the directory to the list
    for file in os.listdir(directory):
        if file.endswith(".md"):
            files.append(file)
    print("We got the files!")
    print(files)
    return files

def read_files(files, debug):
    data = []
    for i in range(len(files)):
        file = files[i]
        print(f'{i} of {len(files)} files reveiwed\n')
        
        #read the contents of the file and save the variable contents
        with open(directory + "/" + file, "r") as f:
            print(f'Reading    --{file}--')
            contents = f.read()

        #check if the file is labled and continue if it is
        labels = ['#flashcard', '#personal', '#done_no_flashcard', '#todo']
        if check_labels(contents, labels, file):
            continue

        print(f'{file} has no label')
        #present the user with lables one by one until they add one
        user_label(contents, labels, file, debug)

        clear(debug)
            
    return 

def check_labels(contents, labels, file):
    if len(contents) == 0:
        print(f'           --{file}-- is empty, marking as #todo')
        with open(directory + "/" + file, "w") as f:
            f.write('#todo\n')
        return True
    for i in labels:
        if contents.find(i) == 0:
            print(f'           --{file}-- is labled {i}')
            return True
    return False


def user_label(contents, labels, file, debug):
    File_and_contents = f'------------\n{file[:-3]}\n\n{contents}\n\n'
    for i in labels:
        clear(debug)
        answer = user_input(f'{File_and_contents}Label {i}? (Y/n) ', ['y', 'n', ''], 'Please enter a command')
        #if answer is y or blank, add the label to the file
        if answer == 'y' or answer == "":
            with open(directory + "/" + file, "w") as f:
                f.write(f'{i}\n{contents}')
            return
    print(f'No label was added')
    user_label(file, contents)


def clear(debug): 
    if not debug:
        os.system('clear && printf "\e[3J"')


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

    
def main():
    #ask the user if they want to run in debug mode
    debug = user_input("Run in debug mode? (Y/n) ", ['y', 'n', ''], 'Please enter a command')
    if debug == 'y' or debug == "":
        debug = True
    else:
        debug = False
    clear(debug)
    print("Welcome to the Mass Label Notes program!")
    
    #read all the files in the directory
    files = get_files(directory)
    #get work done
    read_files(files, debug)
    return


main()