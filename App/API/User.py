
 
"""
 Projet : Finances-Pro-Max
 Directory : API
 Name Of File : User.py
 Author : Thomas Raymond
 Author : Félix Roussin
 Date : 26 août 2026
 
Description  : Class for managing user's past sessions.
                The Class is call from the frontend (UI) for saving info
"""
import API.Fichier as fichier
from API.Transaction import Transaction
import pickle
import datetime
import hashlib


def prRed(s): return "\033[91m{}\033[00m".format(s)
def prGreen(s): return "\033[92m{}\033[00m".format(s)
 
class User:
    def __init__(self,name:str,pwd: str)->None:
            self.name = name
            self.key = self.get_hash(pwd)
            historic = self.retreive_info(self.key)
            if historic is not None:
                self.transaction_id = historic['id']
                self.column_lenght = historic['column_format']
                self.solde = historic['solde']
            else:
                self.solde = []
                self.transaction_id = 1
                self.types_de_transaction = {}
                self.column_lenght = {"ID":len('ID') + 1, 'Raison':len('Raison') + 2, 'Montant':len('Montant') + 2, 'Date':len('Date') + 2}
                return None
    
    def retreive_info(self, file_name):
        memory_content = None
        try:
            memory_content = fichier.read_content(file_name)
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
        fichier.write_object_binary(self.key, {"solde":self.solde, "id":self.transaction_id, "column_format":self.column_lenght})


    def add_transaction(self, montant, choix, raison)->None:
        now = datetime.datetime.now().date()
        id = self.get_new_transaction_id()
        wanted_transaction = Transaction(id, montant, choix, now, raison) # Create the first transaction id

        if wanted_transaction.valid_transaction():
            transaction = wanted_transaction 
            self.solde.append(transaction)
            self.transaction_id += 1
            self.column_lenght["ID"] = max(self.column_lenght["ID"], len(str(transaction.id)) + 2)
            self.column_lenght["Raison"] = max(self.column_lenght["Raison"], len(transaction.raison) + 2)
            self.column_lenght["Montant"] = max(self.column_lenght["Montant"], len(str(transaction.montant)) + 2)
            self.column_lenght["Date"] = max(self.column_lenght["Date"], len(str(transaction.date)) + 2)
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

    def get_new_transaction_id(self) -> int:
        return self.transaction_id # Create the first transaction id
            
    def print_historic(self)->str:
        historic_widget :str = f""
        if(len(self.solde) > 0 ):
            historic_widget += "Votre historique : \n"
            depot = self.get_depot()
            if(len(depot)!=0):
                historic_widget += "Vos dépôts: \n"
                historic_widget += f"{'ID':^{self.column_lenght['ID']}}{'Raison':^{self.column_lenght['Raison']}}{'Montant':^{self.column_lenght['Montant']}}{'Date':^{self.column_lenght['Date']}}\n"
                for i in depot:
                    historic_widget += prGreen(f"{i.get_id():^{self.column_lenght['ID']}}{i.get_raison():^{self.column_lenght['Raison']}}{i.get_montant():^{self.column_lenght['Montant']}.2f}{str(i.get_date()):^{self.column_lenght['Date']}}")
                    historic_widget += "\n"
            retrait = self.get_retrait()
            if(len(retrait)!=0):
                historic_widget += "Vos retraits: \n"
                historic_widget += f"{'ID':^{self.column_lenght['ID']}}{'Raison':^{self.column_lenght['Raison']}}{'Montant':^{self.column_lenght['Montant']}}{'Date':^{self.column_lenght['Date']}}\n"
                for i in retrait:
                    historic_widget += prRed(f"{i.get_id():^{self.column_lenght['ID']}}{i.get_raison():^{self.column_lenght['Raison']}}{i. get_montant():^{self.column_lenght['Montant']}.2f}{str(i.get_date()):^{self.column_lenght['Date']}}")
                    historic_widget += "\n"
        return historic_widget
            

    def __str__(self)->str:
        solde=total = sum(t.get_montant() for t in self.solde)
        if solde < 0:
            return f"Vous êtes : {self.name}\nVotre solde est de :"+prRed(f"{solde:.2f}")+"$ \n"
        return f"Vous êtes : {self.name}\nVotre solde est de : {solde:.2f}$ \n"
        
     
     
         
             
 
