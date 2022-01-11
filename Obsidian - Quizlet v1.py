import os
import pyperclip as pc

directory = "/Users/reed/Library/Mobile Documents/iCloud~md~obsidian/Documents/alpha"

def get_files(directory):
    files = []
    for file in os.listdir(directory):
        if file.endswith(".md") and file[0] != ".":
            files.append(file)
    return files

def get_data(files):
    data = []
    for file in files:
        with open(directory + "/" + file, "r") as f:
            print(f'Reading    --{file}--')
            x = f.read()
            

            #add a sigle space to the end of the file to make it easier to split
            x += " "
            
            # remove the text between "[[" and "|", then remove the characters "[" and "]"
            for i in range(len(x)):
                if x[i:i+2] == "[[":
                    for a in range(len(x[i:])):
                        a = a + i
                        if x[ a:a + 2] == "]]":
                            print(f'brackets found at {i,a}:{x[i:a+2]} in {file}')
                            b = x.find("|",i,a)
                            
                            if b != -1:
                                print(f'| found at {b}')
                                print(f'deleting "{x[i:b]}" from {file} because it contains a pipe')
                                x = x[:i] + x[b+1:]
                            break

            #remove all "[" and "]"
            x = x.replace("[", "")
            x = x.replace("]", "")

            #remove the first line of the file if it starts with "#"
            while x[0] == "#":
                # y exists because f-strings can't contain a backslash
                y = x[:x.find("\n")]
                print(f'deleting "{y}" from "{file}" because it starts with "#"')
                x = x[x.find("\n") + 1:]
            
            # if the file starts with "See", skip it
            if x.find("See") == 0:
                print(f'skipping {file} because x.find("See") produced {x.find("See")}')
                continue
            
            # remove all occurrences of "See" that follow a newline and all text after it    
            x = x[:x.find("See")]
            
            # if the file still has length, add it to the data list
            if len(x) > 0:
                data.append([file, x])
    return data



def create_csv(data):
    print("Copying data to clipboard...")
    sheet = ""
    for i in range(len(data)):
        sheet += f"{data[i][0][:-3]};;{data[i][1]};;;"
    pc.copy(sheet)
    
    with open("data.txt", "w") as f:
        for i in range(len(data)):
            #write the title of the file without the .md suffix and the data of the file
            f.write(data[i][0][:-3] + ";;" + data[i][1] + ";;;")


def main():
    print("Getting files...")
    files = get_files(directory)
    print("Getting data...")
    data = get_data(files)
    print("Creating csv...")
    create_csv(data)
    #print a done message and the location of the csv
    print(f"Done! Data is located at {os.getcwd()}/data.txt")

main()