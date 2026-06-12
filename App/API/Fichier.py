"""
 Projet : Finances-Pro-Max
 Directory : API
 Name Of File : Fichier.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 12 juin 2026

Description : Program handling the files.
"""

from io import BufferedWriter, FileIO, BufferedReader
import pickle
import platform
from pathlib import PureWindowsPath, Path # Il manquait PureWindowsPath


if(platform.system() == "Windows"):
    __PATH = str(PureWindowsPath(__file__).parent)+'\\'+'.memory'+'\\'
else:
    __PATH = '.memory'+'/'


"""
    method call when first use so it create the user file
"""
def write_object_binary(file_name,data)-> None:
    Path(__PATH+file_name+'.bin').parent.mkdir(parents=True, exist_ok=True)
    try:
        if(data != None):
            with BufferedWriter(FileIO((__PATH+file_name+'.bin'),"wb")) as writer:
                pickle.dump(data, writer)
        else:
            open((__PATH+file_name+'.bin'),"wb")
    except IOError as e: 
        print(f"An error occurred when writing the files or creating it: {e}")



"""
    Function opens a binary file in append mode to add the new informations that
    came in an argument.
"""    
def add_object_binary(file_name,data)-> None:
     try:
        with BufferedWriter(FileIO((__PATH+file_name+'.bin'),"wb")) as writer:
            pickle.dump(data, writer)
     except IOError as e: 
        print(f"An error occure when wrinting the files")

"""
    look if file exist
"""
def file_exist(file_name) -> bool :
    try: 
        open((__PATH+file_name+'.bin'),"rb")
        
    except FileNotFoundError as e:
        return False
    return True

"""
    Read the files that got passed as an argument and return the content
"""
def read_content(file_name):
    try:
        with open((__PATH+file_name+'.bin'),"rb") as file_content:
            content = BufferedReader(file_content)
            return content.read()
    except FileNotFoundError as e:
        print(f"Le mot de passe entré ne correspond à aucun utilisateur." )
    except IOError as e: 
        print(f"An error occured when reading the files: {e}")

