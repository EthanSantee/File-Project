import os
import Ai
import shutil


# prompts the user to enter the path to the file via the terminal and returns the entered path
# also ensures that the user's enter path is a valid folder
# @pre: none
# @post:
# @returns: a string of the path to the folder on the user's computer
def getPathFromUser():
    print("Enter a filepath to the folder you want to organize: ")
    folderpath = input().strip()

    while (not os.path.isdir(folderpath)):
        print("Invalid folder path \nPlease input another one: ", end="")
        folderpath = input().strip()
   
    return folderpath


# Process uploaded file and extract its content
# @param: the path to the file to be read
# @pre: 
# @post: 
# #returns: 
def extractFileContents(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content


# reads the names of all the files in the given directory and places them in a string with the format
# filename1, filename2, filename3, filename4, ...
# @param: folder - a string of the path to the folder on the user's computer
# @pre: none
# @post: 
# @returns: a string containing all the filenames in the given directory
def compileFileNames(folder):
    directory = os.fsencode(folder)
    allfilenames = ""
    for file in os.listdir(directory):
        if not os.path.isdir(file):
            filename = os.fsdecode(file)
            allfilenames += filename

    return allfilenames


# sorts all the files in the given folder
# @param folder - a string of the path to the folder containing all the files to sort out
# @pre: folder must be a valid complete path to a folder on the user's computer
# @post: the folder should contain several subFolders with all the files sorted into them
# @returns: nothing
def sortFiles(folder):
    #Todo
    filenames = compileFileNames(folder)
    instructions = extractFileContents("instructions.txt")
    prompt = instructions + filenames
    response = Ai.get_ai_response(prompt)

    try:
        categories = response.split('\n')
        folders = []
        # Create a list of all the folders and their contents
        # Each element of the list is another list whose first element is the name of the folder 
        # and all following elements are the files in that folder
        for index in range(len(categories) - 1):
            categories[index] = categories[index].split()
            folders.append(categories[index][0])

        categories.pop()
    except:
        print("There was an error organizing your files")


    # Make the folders
    for foldername in folders:
        try:
            os.mkdir(folder + "/" + foldername)
        except:
            continue

    # Move the files into the folders
    try:
        for list in categories:
            for fileindex in range(1, len(list)):
                filename = list[fileindex]
                source_path = os.path.join(folder, filename)
                destination_path = os.path.join(folder, list[0], filename)
                if not (os.path.isdir(source_path)):
                    shutil.move(source_path, destination_path)
    except:
        print("Error")



def main():
    folderPath = getPathFromUser()
    sortFiles(folderPath)


main()