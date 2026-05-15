
 
"""
 Projet : Finances-Pro-Max
 Directory : API
 Name Of File : User.py
 Author : Thomas Raymond
 Author : Félix Roussin
 Date : 15 mai 2026
 
Description  : Class for managing user's past sessions.
                The Class is call from the frontend (UI) for saving info
"""
import array as arr
import API.Fichier as fichier
from API.Transaction import Transaction
import pickle
import datetime
from pathlib import Path, PureWindowsPath
import os


def prRed(s): return "\033[91m {}\033[00m".format(s)
def prGreen(s): return "\033[92m {}\033[00m".format(s)
 
class User:


    
    # def extract_memory_file_information(self, file_name):
    #  """
    #  Function to read a memory file. It takes the file name as an input and outputs the bytes in a list of one element(the line)
    #  """
     # 
     # try:
     #    memory_file=open(file_name,"xb") # Try opening the file if it doesn't exist
     #    liste_pour_binaire=[]
     # except FileExistsError:
     #    memory_file=open(file_name,"rb")
     #    liste_pour_binaire=[]
     #    contenu=memory_file.readline() # Read the information
     #    liste_pour_binaire.append(contenu) # Store it
     # memory_file.close()
     # return liste_pour_binaire

        

    
    def retreive_info(self,name):
        transactions = []
        try:
            memory_content=fichier.read_content(name) 
            transaction = pickle.loads(memory_content)
        except EOFError as e :
            return  None
        except TypeError as e:
            return None
        
        
        return transaction

    def save_info(self)->None:
        fichier.write_object_binary(self.name,self.solde)

    def add_transaction(self,montant,choix)->None:
        now = datetime.datetime.now()
        self.solde.append(Transaction(montant,choix,now.date()))
 
    def get_depot(self)-> arr.array:
        return [t for t in self.solde if t.get_montant() >= 0]
    
    def get_retrait(self)-> arr.array:
        return [t for t in self.solde if t.get_montant() < 0] 
        
    def get_solde(self):
        return self.solde

    def __init__(self,name:str)->None:
        self.name = name
        historic = self.retreive_info(name)
        if(historic!=None):       
            self.solde = historic
        else:
            self.solde = []

        
            
    def print_historic(self)->str:
        historic_widget :str = ""
        if(len(self.solde) > 0 ):
            historic_widget += "Votre historique : \n"
            depot = self.get_depot()
            if(len(depot)!=0):
                historic_widget += "Vos depot: \n"
                for i in depot:
                    historic_widget += prGreen(f"{i.get_montant():.2f}$, {i.get_date()}") # .2f permet d'écrire deux chiffres après la virgule
                    historic_widget += "\n"
            retrait = self.get_retrait()
            if(len(retrait)!=0):
                historic_widget += "Vos retrait: \n"
                for i in retrait:
                    historic_widget += prRed(f"{i.get_montant():.2f}$, {i.get_date()}")
                    historic_widget += "\n"
        return historic_widget
            

    def __str__(self)->str:
        solde=total = sum(t.get_montant() for t in self.solde)
        if solde < 0:
            return f"Vous êtes : {self.name}\nVotre solde est de :"+prRed(f"{solde:.2f}")+"$ \n"
        return f"Vous êtes : {self.name}\nVotre solde est de : {solde:.2f}$ \n"
        
     
     
         
             
 
