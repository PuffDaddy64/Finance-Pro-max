
 
"""
 Projet : Finances-Pro-Max
 Directory : API
 Name Of File : User.py
 Author : Thomas Raymond
 Author : Félix Roussin
 Date : 7 août 2026
 
Description  : Class for managing user's past sessions.
                The Class is call from the frontend (UI) for saving info
"""
import array as arr
import API.Fichier as fichier
from API.Transaction import Transaction
import pickle
import datetime
import hashlib


def prRed(s): return "\033[91m {}\033[00m".format(s)
def prGreen(s): return "\033[92m {}\033[00m".format(s)
 
class User:
    def __init__(self,name:str,pwd: str)->None:
            self.name = name
            self.key = self.get_hash(pwd)
            historic = self.retreive_info(self.key)
            self.types_de_transaction = {}
            if(historic!=None):   
                self.solde = historic
            else:
                self.solde = []
                return None
    
    def retreive_info(self, name):
        memory_content = None
        try:
            memory_content = fichier.read_content(name)
        except EOFError as e :
            return  None
        except TypeError as e:
            return None
        if isinstance(memory_content, bytes):
            transaction = pickle.loads(memory_content)
            return transaction

    def get_hash( self, psw : str ):
        hash_obj = hashlib.sha256((self.name+psw).encode())
        return hash_obj.hexdigest()

    def save_info(self)->None:
        fichier.write_object_binary(self.key,self.solde)


    def add_transaction(self, montant, choix, type_de_transaction)->None:
        now = datetime.datetime.now()
        wanted_transaction = Transaction(montant, choix, now.date(), type_de_transaction)
        if wanted_transaction.valid_transaction():
            transaction = wanted_transaction 
            self.solde.append(transaction)
        else:
            del wanted_transaction
            
        
 
    def get_depot(self):
        return [t for t in self.solde if t.get_montant() >= 0]
    
    def get_retrait(self):
        return [t for t in self.solde if t.get_montant() < 0] 
        
    def get_solde(self):
        return self.solde

    def get_types_de_transaction(self):
        return  self.types_de_transaction

        
            
    def print_historic(self)->str:
        historic_widget :str = ""
        if(len(self.solde) > 0 ):
            historic_widget += "Votre historique : \n"
            depot = self.get_depot()
            if(len(depot)!=0):
                historic_widget += "Vos dépôts: \n"
                for i in depot:
                    historic_widget += prGreen(f"{i.get_raison_transaction()} : {i.get_montant():.2f}$, {i.get_date()}") # .2f permet d'écrire deux chiffres après la virgule
                    historic_widget += "\n"
            retrait = self.get_retrait()
            if(len(retrait)!=0):
                historic_widget += "Vos retraits: \n"
                for i in retrait:
                    historic_widget += prRed(f"{i.get_raison_transaction()} : {i.get_montant():.2f}$, {i.get_date()}")
                    historic_widget += "\n"
        return historic_widget
            

    def __str__(self)->str:
        solde=total = sum(t.get_montant() for t in self.solde)
        if solde < 0:
            return f"Vous êtes : {self.name}\nVotre solde est de :"+prRed(f"{solde:.2f}")+"$ \n"
        return f"Vous êtes : {self.name}\nVotre solde est de : {solde:.2f}$ \n"
        
     
     
         
             
 
