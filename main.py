import os
from google import genai
import Ai
import shutil

def process_uploaded_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

print("Hi! my name is Archibald Thaddeus Montague, Chief Architect of Data Integrity, Grand Curator of Digital Archives, Supreme Analyst of Encrypted Realms, Keeper of the Binary Sanctum, and Vanguard of Organized Information.")
print()

userinput = "y"

while (userinput == "y"):
    # Start by prompting the user for a filepath to the folder they want to organize
    print("Enter a filepath to the folder you want to organize: ")
    folderpath = input().strip()

    while (not os.path.isdir(folderpath)):
        print("Invalid folder path \nPlease input another one: ", end="")
        folderpath = input().strip()
        

    directory = os.fsencode(folderpath)
    prompt = ""
    allfilenames = ""

    # Iterate over all the files in the given folder
    for file in os.listdir(directory):
        if not os.path.isdir(file):
            filename = os.fsdecode(file)
            allfilenames += filename

            # Analyze Text-Based Files
            if filename.endswith(".txt") or filename.endswith(".pdf"):
                file_content = process_uploaded_file(folderpath + "/" + filename)
                prompt = prompt + "\n\n" + filename + ":\n" + file_content
                
            # Anaylze Image-Based Files
            if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".webp"):
                file_content = Ai.analyze_image(folderpath + "/" + filename, r"image.json")
                prompt = prompt + "\n\n" + filename + ":\n" + file_content

    # Adds all the filenames to the top of the prompt so gemini knows what files to sort
    prompt = "Files in this folder are: " + allfilenames + "\nfile contents:\n" + prompt

    # Gives instructions and all the files to the ai
    instructions = process_uploaded_file("instructions.txt")

    # Ask user for additional instructions
    print("Are there any addition instructions for sorting your files? (y / n)")
    extraInstructions = input().strip().lower()
    
    while extraInstructions != "y" and extraInstructions != "n":
        print("Invalid Choice! PLease enter y/n: ", end="")
        extraInstructions = input().strip().lower()    
    
    if extraInstructions == "y":
        print("Input Additional Info: ", end="")
        additionalInfo = input().strip()
        instructions += "Also do these additional instructions (these instructions should take precedent over the previous instructions above): \n" + additionalInfo
        
    
    # Ai gives back its response as a string of all the folder names to create
    response = Ai.get_ai_response(prompt, instructions)

    """
    ----debugging-----
    print("prompt:")
    print(prompt)
    print("instructions:")
    print(instructions)
    print("response:")
    print(response)
    """

    try:
        categories = response.split('\n')
        folders = []
        # Create a list of all the folders and their contents
        # Each element of the list is another list whose first element is the name of the folder and all following elements are the files in that folder
        for index in range(len(categories) - 1):
            categories[index] = categories[index].split()
            folders.append(categories[index][0])

        categories.pop()
    except:
        print("There was an error organizing your files")

    """
    ----debugging----
    print(folders)
    print(categories)
    """

    # Make the folders
    for foldername in folders:
        try:
            os.mkdir(folderpath + "/" + foldername)
        except:
            continue

    try:
        # Move the files into the folders
        for list in categories:
            for fileindex in range(1, len(list)):
                filename = list[fileindex]
                source_path = os.path.join(folderpath, filename)
                destination_path = os.path.join(folderpath, list[0], filename)
                if not (os.path.isdir(source_path)):
                    shutil.move(source_path, destination_path)
    except: 
        continue
    
    print("Would you like to sort another folder? (Enter y/n)")
    userinput = input().lower().strip()
    
    while (userinput != "y" and userinput != "n"):
        print("Invalid input please try again: ", end="")
        userinput = input().lower().strip()
        

print("Bye!")


