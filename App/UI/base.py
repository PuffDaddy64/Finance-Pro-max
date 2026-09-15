

from textual import on
from textual.app import App,ComposeResult
from textual.containers import Container, Horizontal,Vertical
from textual.widgets import Collapsible, Header, Footer, Button, Input, Label,Pretty,ListItem, ListView,DataTable
from textual.validation import Length, Validator


import sys
import os



# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from API.User import User
import API.Transaction as Transaction
import API.Fichier as fichier
import time as t


user = User("Felix", "1234")
historic_transactions = user.get_transactions()
formated_transactions = [("ID", "Raison", "Montant", "Date")]
for transaction in historic_transactions:
    formated_transactions.append((str(transaction), str(historic_transactions[transaction].get_raison()) , str(historic_transactions[transaction].get_montant()), str(historic_transactions[transaction].get_date())))
ROWS = formated_transactions




class body(App):

    CSS_PATH="TCSS/body.tcss"



    

    def compose(self) -> ComposeResult:
        yield Container(
            
            Horizontal(
                Container(
                    Collapsible(
                        ListView(
                            ListItem(Label("Item 1")),
                            ListItem(Label("Item 2")),
                            ListItem(Label("Item 3")),
                        ),
                title = "Menu",
                id="menu",
                ),  ),  
                Horizontal(
                    Input(
                        id="ID"
                    ),
                    Input(
                        
                    id="chiffre"  
                    ),
                    id="montant"
                ),
                id="top",
                ),
            Horizontal(
                Container(
                    Label(user.get_name()),
                    Label(f"Solde: {sum(user.get_transactions()[id].get_montant() for id in user.get_transactions())}"),
                    id="info",
                ),
                DataTable(
                    id="table",
                ),
                id="middle",
            ),
            id="body",
        ) 
        
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

        inputMontant = self.query_one('#chiffre', Input) 
        inputMontant.border_subtitle = "Montant"

        inputID = self.query_one('#ID', Input)
        inputID.border_subtitle = "ID"




if __name__ == "__main__":
    app = body()
    app.run()

