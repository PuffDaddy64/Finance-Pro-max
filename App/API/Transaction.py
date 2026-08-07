 
"""
 Project : Finances-Pro-Max
 Directory : API
 Name Of File : Transaction.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 7 août 2026
 
Description  : Class for the transaction handling with deposit and withdraw.
               The class is called from the frontend (UI) for displaying infos
               and saving them.
"""

import time as t

class Transaction:
    def __init__(self, montant:str, choix:str, date, raison_transaction:str) -> None:
         """
             Initialize values
         """ 
         self.set_montant(montant, choix) 
         self.date = date
         self.set_raison_transaction(raison = raison_transaction)

 # Methods related to the date ofthe transaction
    def get_date(self):
        """
            Method that returns the date
        """
        return self.date
 
 # Methods related to the amount of the transaction
    def validation_montant(self, montant_entre:str) -> bool:
         """
             Validates the new amount (montant) before its added to the array of transaction
         """
         try:
             montant:float = float(montant_entre)
         except ValueError:
             print("Saisie invalide.")
             t.sleep(1)
             self.montant_valide = False
             return False
         if montant > 0:
             self.montant_valide = True
             return True
         else:
             print("Le nombre n'est pas positif.")
             t.sleep(1)
         self.montant_valide = False
         return False

    def set_montant(self, montant:str, choix:str) -> Transaction | int | None:         
         if montant == "I":
            return 0
         if self.validation_montant(montant):
             self.montant : float  = float(montant) if choix == "d" else (float(montant) * -1)
             return self
         else:
             print("Le montant n'est pas valide.")
             t.sleep(2)
             del self

    def get_montant(self):
        """
            Method tat returns the amount (montant)
        """
        return self.montant

 # Methods related to the reason of the transaction

    def validation_raison_transaction(self, raison:str) -> bool:
        if len(raison) == 0:
            print("Vous n'avez pas entré de raison pour votre transaction.")
            self.raison_valide = False
            t.sleep(1)
            return False
        self.raison_valide = True
        return True
    
    def set_raison_transaction(self, raison: str) -> str | None:
        if self.validation_raison_transaction( raison = raison):
             self.type_de_transaction: str = raison
    
    def get_raison_transaction(self) -> str:
        """
        Method that returns the class variable raison_transaction.
        """
        return self.type_de_transaction

    # Method regrouping the completion of a validation
    def valid_transaction(self):
        if self.montant_valide and self.raison_valide:
            return True
        return False
