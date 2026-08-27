
 
"""
 Projet : Finances-Pro-Max
 Directory : API
 Name Of File : User.py
 Author : Thomas Raymond
 Author : Félix Roussin
 Date : 27 août 2026
 
Description  : Class for managing user's past sessions.
                The Class is call from the frontend (UI) for saving info
"""
import API.Fichier as fichier
from API.Transaction import Transaction
import pickle
import hashlib
import time as t


def prRed(s): return "\033[91m{}\033[00m".format(s)
def prGreen(s): return "\033[92m{}\033[00m".format(s)
 
class User:
    def __init__(self, name:str, pwd: str) -> None:
            self.name:str = name
            self.key:str = self.get_hash(pwd)
            info_user = self.retrieve_info(self.key)
            if info_user is not None:
                self.next_transaction_id = info_user['id']
                self.column_format = info_user['column_format']
                self.transactions = info_user['transactions']
            else:
                self.transactions = {}
                self.next_transaction_id = 1
                self.raisons_transaction = {} # Variables inutilisée pour l'instant elle servira à trier les transactions selon leur raison
                self.column_format = {"ID":len('ID') + 1, 'Raison':len('Raison') + 2, 'Montant':len('Montant') + 2, 'Date':len('Date') + 2}
                return None

    # Methods related to the hash of the user
    def get_hash( self, psw : str ):
            hash_obj = hashlib.sha256((self.name+psw).encode())
            return hash_obj.hexdigest()

    # Methods related to the me mory of the user
    def retrieve_info(self, file_name:str):
        """
        Method to retrieve the informations contained the user's file
        """
        # Validation du contenu du fichier de l'utilisateur
        try:
            file_content = fichier.read_content(file_name)
        except EOFError:
            return None
        except TypeError:
            return None

        # Récupération des informations de l'utilisateur
        if isinstance(file_content, bytes):
            info_user = pickle.loads(file_content)
            return info_user

    def save_info(self) -> None:
        """
        Method saving user's informations
        """
        fichier.write_object_binary(self.key, {"transactions":self.transactions, "id":self.next_transaction_id, "column_format":self.column_format})

    # Methods related to its transactions
    def add_transaction(self, montant:str, choix:str, raison:str) -> None:
        """
        Method adding a transaction to the user
        """
        # Obtenir les informations de la transaction
        id:int = self.get_new_transaction_id()
        wanted_transaction:Transaction = Transaction(choix = choix, id = id, raison = raison, montant = montant)

        # Valider la transaction
        if wanted_transaction.valid_transaction():
            # Créer la transaction
            transaction:Transaction = wanted_transaction 
            self.transactions[transaction.get_id()] = transaction
            self.next_transaction_id += 1
            self.column_format["ID"] = max(self.column_format["ID"], len(str(transaction.id)) + 2)
            self.column_format["Raison"] = max(self.column_format["Raison"], len(transaction.raison) + 2)
            self.column_format["Montant"] = max(self.column_format["Montant"], len(str(transaction.montant)) + 2)
            self.column_format["Date"] = max(self.column_format["Date"], len(str(transaction.date)) + 2)
        else:
            # Détruire la transaction
            del wanted_transaction
 
    def get_depots(self) -> list:
        """
        Method getting all deposits
        """
        return [self.transactions[id] for id in self.transactions if self.transactions[id].get_montant() >= 0]
    
    def get_retraits(self):
        """
        Method getting all withdraws
        """
        return [self.transactions[id] for id in self.transactions if self.transactions[id].get_montant() < 0]
        
    def get_transactions(self):
        """
        Method getting all transactions of the user
        """
        return self.transactions

    def validation_id_transaction(self, id_entre:str) -> bool:
        try:
            id:int = int(id_entre)
        except ValueError:
            print("Le montant doit être un nombre.")
            t.sleep(1)
            return False
        # Valider si l'ID entré est positif
        if id > 0:
            if id in self.get_transactions().keys():
                return True
            else:
                print("Aucune transaction n'a cette ID")
                t.sleep(1)
                return False
        else:
            print("Le nombre doit être supérieur à 0.")
            t.sleep(1)
            return False
        
        
    def get_transaction(self, id:int) -> Transaction:
        return self.get_transactions()[int(id)]

    def get_raisons_transaction(self):
        """
        Method returning all reasons for a transaction that the user has created
        """
        return  self.raisons_transaction

    def get_new_transaction_id(self) -> int:
        """
        Method getting the new transactions ID
        """
        return self.next_transaction_id

    # Methods related to the printing of the user's informations 
    def print_historic(self)->str:
        """
        Method printing the historic of the user
        """
        # Create the string to print
        historic_widget:str = f""

        # Adding to the string, if there are, all transactions
        if len(self.transactions) > 0:
            historic_widget += "Votre historique :\n"

            # Adding to the string, if there are, all deposits
            depots:list = self.get_depots()
            if len(depots) != 0:
                historic_widget += "Vos dépôts: \n"
                historic_widget += f"{'ID':^{self.column_format['ID']}}{'Raison':^{self.column_format['Raison']}}{'Montant':^{self.column_format['Montant']}}{'Date':^{self.column_format['Date']}}\n"
                for i in depots:
                    historic_widget += prGreen(f"{i.get_id():^{self.column_format['ID']}}{i.get_raison():^{self.column_format['Raison']}}{i.get_montant():^{self.column_format['Montant']}.2f}{str(i.get_date()):^{self.column_format['Date']}}")
                    historic_widget += "\n"
            
            # Adding to the string, if there are, all withdraws
            retraits:list = self.get_retraits()
            if len(retraits) != 0:
                historic_widget += "\nVos retraits: \n"
                historic_widget += f"{'ID':^{self.column_format['ID']}}{'Raison':^{self.column_format['Raison']}}{'Montant':^{self.column_format['Montant']}}{'Date':^{self.column_format['Date']}}\n"
                for i in retraits:
                    historic_widget += prRed(f"{i.get_id():^{self.column_format['ID']}}{i.get_raison():^{self.column_format['Raison']}}{i. get_montant():^{self.column_format['Montant']}.2f}{str(i.get_date()):^{self.column_format['Date']}}")
                    historic_widget += "\n"

        return historic_widget
    
    
    def __str__(self) -> str:
        """
        Method printing the solde when the user is an argument of a string
        """
        # Calculate the solde
        solde:float = sum(self.transactions[id].get_montant() for id in self.transactions)

        # Printing the solde according to its sign
        if solde < 0:
            return f"Vous êtes : {self.name}\nVotre solde est de :"+prRed(f"{solde:.2f}")+"$ \n"
        return f"Vous êtes : {self.name}\nVotre solde est de : {solde:.2f}$ \n"
        
     
     
         
             
 
