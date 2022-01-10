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

def read_files(files):
    data = []
    for i in range(len(files)):
        file = files[i]
        print(f'{i} out of {len(files)} files reveiwed')
        with open(directory + "/" + file, "r") as f:
            contents = f.read()
            if contents.find("#todo") == 0:
                print(f'{file} already has #todo at the beginning')
                continue
            elif contents.find("#flashcard") == 0:
                print(f'{file} already has #flashcard at the beginning')
                continue
            
        input("Press enter to continue")  
        with open(directory + "/" + file, "w") as f:
            if len(contents) == 0:
                print(contents)
                x = input(f'{file} is empty, adding to the todo list')
                print(contents)
                f.write(f'#todo\n{contents}')
                input(contents)
                continue
            print(f'now reading {contents}')
            f.write(contents)    
            #present the user with the file and ask if they want to add it to the todo list and if they do, add it
            File_and_contents = f'File:\n{file[:-3]}\n\nContents:\n{contents}\n\n'
            y = user_input(f'{File_and_contents}Add to the flashcard list? (y/n) ', ['y', 'n'], 'Please enter a command')
            if y == 'y':
                f.write("#flashcard\n{contents}")

            else:
                #clear()
                y = user_input(f'{File_and_contents}Add file to todo list? (y/n) ', ['y', 'n'], 'Please enter a command')
                if y == 'y':
                    f.write(f'#todo\n{contents}')
            
    return 

def clear():
    os.system('clear')


def user_input(prompt, responses, error_message):
    while True:
        x = input(prompt)
        #clear()
        if x in responses:
            return x
        elif x == 'q':
            quit()
        else:
            print(error_message)
            continue

def main():
    #lear()
    print("Welcome to the Todo List Maker")
    files = get_files(directory)
    read_files(files)
    return

main()