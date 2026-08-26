 
"""
 Project : Finances-Pro-Max
 Directory : API
 Name Of File : Transaction.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 26 août 2026
 
Description  : Class for the transaction handling with deposit and withdraw.
               The class is called from the frontend (UI) for displaying infos
               and saving them.
"""

import time as t

class Transaction:
    def __init__(self, id:int, montant:str, choix:str, date, raison:str) -> None:
         """
             Initialize values
         """ 
         self.id = id
         self.set_raison(raison = raison)
         self.set_montant(montant, choix)
         self.date = date

 # Methods related to the id
    def get_id(self):
        return self.id
     
 # Methods related to the date ofthe transaction
    def get_date(self) -> str:
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

# Methods related to the transaction type

    def get_type(self) -> str:
        if self.get_montant() > 0:
            return "Dépôt"
        else:
            return "Retrait"

 # Methods related to the reason of the transaction

    def validation_raison(self, raison:str) -> bool:
        if len(raison) == 0:
            print("Vous n'avez pas entré de raison pour votre transaction.")
            self.raison_valide = False
            t.sleep(1)
            return False
        self.raison_valide = True
        return True
    
    def set_raison(self, raison: str) -> str | None:
        if self.validation_raison( raison = raison):
             self.raison: str = raison
    
    def get_raison(self) -> str:
        """
        Method that returns the class variable raison_transaction.
        """
        return self.raison

    # Method regrouping the completion of a validation
    def valid_transaction(self):
        if self.montant_valide and self.raison_valide:
            return True
        return False
