
from io import BufferedWriter, FileIO, BufferedReader
import pickle


"""
    method call when first use so it create the user file
"""
def write_object_binary(file_name,data)-> None:
    file_name.parent.mkdir(parents=True, exist_ok=True)
    try:
        with BufferedWriter(FileIO(file_name,"wb")) as writer:
            pickle.dump(data, writer)
    except IOError as e: 
        print(f"An error occurred when writing the files: {e}")



"""
    Function opens a binary file in append mode to add the new informations that
    came in an argument.
"""    
def add_object_binary(file_name,data)-> None:
     try:
        with BufferedWritter(FileIO(file_name,"wb")) as writter:
            pickle.dump(data, writer)
     except IOError as e: 
        print(f"An error occure when wrinting the files")

"""
    Read the files that got passe as argument and return the content
"""
def read_content(file_name):
    content = None
    try:
        with open(file_name,"rb") as file_content:
            content = BufferedReader(file_content)
            return content.read()
    except FileNotFoundError as e:
        print(f"File dont exist do you want to create one whit this Username?(Y,N) : ")
        aws = input()
        if(aws== "y"):
            write_object_binary(file_name,None)
            return read_content()
        else:
            return None
    except IOError as e: 
        print(f"An error occure when reading the files: {e}")

