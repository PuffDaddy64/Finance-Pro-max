 
"""
 Project : Finances-Pro-Max
 Directory : API
 Name Of File : Transaction.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 17 octobre 2026
 
Description  : Class describing a transaction.
               The class is called from the User module to manage the information related to a particular transaction.
"""

import time as t
import datetime

class Transaction:

    ID = 0

    def __init__(self,choix:str, raison:str, montant:str, year:int | None, month:int | None, day:int | None) -> None:
         """
             Initialize values
         """ 

         self.id:int = Transaction.ID
         Transaction.ID += 1
         self.set_raison(raison = raison)
         self.set_montant(montant, choix)
         self.set_date(year = year, month = month, day = day)

 # Methods related to the id
    # The ID does not have a set method in the transaction module because it is set by the user because of the need of a memory controlled by the user.

    def get_id(self):
        """
        Method returning the ID of the transaction
        """
        return self.id

# Methods related to the reason of the transaction
    def validation_raison(self, raison:str) -> bool:
        """
        Method validating the reason of the transaction
        """
        if len(raison) == 0:
            print("Vous n'avez pas entré de raison pour votre transaction.")
            self.raison_valide = False
            t.sleep(1)
            return False
        self.raison_valide = True
        return True
    
    def set_raison(self, raison: str) -> None:
        """
        Method setting the reason of the transaction
        """
        if self.validation_raison(raison = raison):
             self.raison: str = raison
    
    def get_raison(self) -> str:
        """
        Method that returns the class variable raison_transaction.
        """
        return self.raison

# Methods related to the amount of the transaction
    def validation_montant(self, montant_entre:str) -> bool:
         """
             Validates the new amount (montant_entre) before it's added to the array of transaction
         """
         # Valider si le montant entré est un nombre
         try:
             montant:float = float(montant_entre)
         except ValueError:
             print("Le montant doit être un nombre.")
             t.sleep(1)
             self.montant_valide:bool = False
             return False

         # Valider si le montant entré est positif
         if montant > 0:
             self.montant_valide:bool = True
             return True
         else:
             print("Le nombre doit être supérieur à 0.")
             if montant < 0:
                print("Le sytème s'occupe lui-même de gérer le concept l'ajout ou la soustraction du nombre.")
             t.sleep(1)
         self.montant_valide:bool = False
         return False

    def set_montant(self, montant:str, choix:str) -> None:
         """
         Method setting the value of the amount of the transaction.
         """    
         if self.validation_montant(montant):
             self.montant : float = float(montant) if choix == "d" else (float(montant) * -1)
         else:
             print("Le montant n'est pas valide.")
             t.sleep(2)

    def get_montant(self):
        """
            Method tat returns the amount (montant)
        """
        return self.montant

 # Methods related to the date ofthe transaction
    def set_date(self, year: int | None, month: int | None, day: int | None) -> None:
        if year == None or month == None or day == None:
            self.date: datetime.date = datetime.datetime.now().date()
            
        else:
            self.date: datetime.date = datetime.datetime(year = year, month = month, day = day).date()

    def get_date(self) -> datetime.date:
        """
            Method that returns the date
        """
        return self.date

# Methods related to the transaction type
 

    # Method regrouping the completion of a validation
    def valid_transaction(self):
        """
        Method regrouping the completion of a validation
        """
        if self.montant_valide and self.raison_valide:
            return True
        return False

    # Method related to the printing of a transaction
    def print(self, format) -> None:
        """
        Method printing one particular transaction
        """
        widget = f"Transaction:\n"
        widget += f"{'ID':^{format['ID']}}{'Raison':^{format['Raison']}}{'Montant':^{format['Montant']}}{'Date':^{format['Date']}}\n"
        widget += f"{self.get_id():^{format['ID']}}{self.get_raison():^{format['Raison']}}{self.get_montant():^{format['Montant']}.2f}{str(self.get_date()):^{format['Date']}}"

        print(widget)

    def change_transaction(self, new_raison:str |None, new_montant:str | None, new_choix:str, new_year:int | None, new_month:int | None, new_day:int | None) -> None:
        if(new_raison != None):
            self.set_raison(raison = new_raison)
        if new_montant is not None:
            self.set_montant(new_montant, new_choix)
        
        self.set_date(year = new_year if new_year is not None else self.date.year, month = new_month if new_month is not None else self.date.month, day = new_day if new_day is not None else self.date.day)
        