
 
"""
 Projet : Finances-Pro-Max
 Directory : API
 Name Of File : User.py
 Author : Thomas Raymond
 Author : Félix Roussin
 Date : 5 mai 2026
 
Description  : Class for managing user's past sessions.
                The Class is call from the frontend (UI) for saving info
"""
import array as arr
import time as t
from typing import Any
import struct
from API.Transaction import Transaction


 
class User:
    def extract_memory_file_information(self, file_name):
     """
     Function to read a memory file. It takes the file name as an input and outputs the bytes in a list of one element(the line)
     """
     try:
        memory_file=open(file_name,"xb") # Try opening the file if it doesn't exist
        liste_pour_binaire=[]
     except FileExistsError:
        memory_file=open(file_name,"rb")
        liste_pour_binaire=[]
        contenu=memory_file.readline() # Read the information
        liste_pour_binaire.append(contenu) # Store it
     memory_file.close()
     return liste_pour_binaire

    def __init__(self):
         """
         Method that is call a constructor and initialize value for the object first 
         """ 
         self.depot_memory = self.extract_memory_file_information("memory_depot_file.bin")
         self.retrait_memory = self.extract_memory_file_information("memory_retrait_file.bin")
         return
    
    def set_depot_historic(self, day, month, year, hour, minute, second, money):
        return self.depot_memory.append(struct.pack(Transaction().information_format(), day, month, year, hour, minute, second, money))
    
    def get_depot_historic(self):
        return self.depot_memory
    
    def set_retrait_historic(self,day, month, year, hour, minute, second, money):
        return self.retrait_memory.append(struct.pack(Transaction().information_format(), day, month, year, hour, minute, second, money))
    
    def get_retrait_historic(self):
        return self.retrait_memory
     
     
         
             
 
