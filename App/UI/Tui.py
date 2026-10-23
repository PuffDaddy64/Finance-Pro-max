"""
 Projet : Finances-Pro-Max
 Directory : UI
 Name Of File : TUi.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 17 ocotbre 2026

Description : UI handler whic appearsin the terminal. This UI is built with a library called Textual.
"""
# Imports to use during the creation of UIs with Textual
import os
import sys
import re
from textual.app import App,ComposeResult
from textual.containers import  Container, Horizontal, Vertical
from textual.widgets import DataTable, Button, Input, Label, ListView , ListItem, Tabs, Tab
from textual.events import InputEvent
from textual.validation import Length
from textual.binding import Binding
from rich.text import Text
from typing import ClassVar
from API.User import User
from API.Transaction import Transaction
import API.Fichier as fichier
import pickle
import API.Validation as Validation


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Classes modified for our App
# Class for a button
class End(Button):
    """
    Button class for eventual usages of buttons.
    """
    num : int  = 0 


    def action_press(self):
        self.num += 1
        
        if(self.num%2 != 0):
            self.label = "press"
            self.add_class("press")
        else:
            self.label = "ass"
            self.remove_class("press")

# Class related to the actual lauching of the APP
class Login(App):

    """
    Manages the APP, it's the most important class
    """
    try_pwd:int = 3 # 3 tries for the pwd

    # Path related to the CSS file wich determines the format appearance of each widget represented in that file
    CSS_PATH = "TCSS/login.tcss"


    BINDINGS: ClassVar[list[Binding]] = [ # type: ignore[override] # Ne pas enlever le commentaire, il retire une erreur relié à un override volontaire de notre part sur BINDINGS
        Binding("ctrl+q", "save_and_quit", "Quit", show = True, priority = True),
    ]

###########################   Bindings Method   ############################


    def action_save_and_quit(self):
        global user
        if user != None:
            user.save_info()
        self.exit()


###################################################################################

###########################   Compose Method (Event)   ############################
    

    def compose(self) -> ComposeResult:
        """
        Method related to the lauch of the App
        """
        # Calling global variables useful in the function
        global users, names, user
        
        # Reading users et usernames files to be able to verify in the inputs corresponds to an exxisting user
        info_users = fichier.read_content("users_list")
        info_names = fichier.read_content("names")
        
        # Decode binary information and update variables
        if info_users is not None: # Update all users present
            users = pickle.loads(info_users)
        if info_names is not None: # update all usernames present
            names = pickle.loads(info_names)

        # Lauches the main features
        yield Vertical(Label("$$$$$$$\\  $$\\   $$\\ $$$$$$$\\   $$$$$$\\  $$$$$$$$\\ $$$$$$$$\\ \n$$  __$$\\ $$ |  $$ |$$  __$$\\ $$  __$$\\ $$  _____|\\__$$  __|\n$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ /  \\__|$$ |         $$ |\n$$$$$$$\\ |$$ |  $$ |$$ |  $$ |$$ |$$$$\\ $$$$$\\       $$ |\n$$  __$$\\ $$ |  $$ |$$ |  $$ |$$ |\\_$$ |$$  __|      $$ |\n$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |         $$ |\n$$$$$$$  |\\$$$$$$  |$$$$$$$  |\\$$$$$$  |$$$$$$$$\\    $$ |\n\\_______/  \\______/ \\_______/  \\______/ \\________|   \\__|", id = "title")
                       ,
            Vertical(
                Horizontal(
                        Container(
                                Input(
                                    id="user",
                                    type="text",
                                    valid_empty=False,
                                    validators=[Length(5)],
                                ),
                            ), 
                        Container(
                            Input(id="pwd",
                                password=True,
                                valid_empty=False,
                                validators=[Length(4)]
                            ),
                        ), 
                        id = "inputs",),
                Horizontal(
                    Container(
                        id="errorMessage",
                    ),
                    Vertical(
                        id="buttonBox",
                    ),
                    id="errorBox"
                ),
                id="messageBox",
            ),
            id = "login",
        )

        yield Container(
                Tabs(
                    Tab(
                        "Add/Modify transactions",
                        id = "add"
                    ),
                    Tab(
                        "Analysis",
                        id = "analysis"
                    ),
                    id = "tabs"
                    ),
                Container(
                    Horizontal(
                        Container(
                            ListView(
                                ListItem(Label("Depot"),id="d",name="Depot"),
                                ListItem(Label("Retrait"),id="r",name="Retrait"),
                                ListItem(Label("Modifier"),id="m",name="Modifier"),
                                id = "options",
                            ),
                        id="menu",
                        ),    
                        Horizontal(
                            Input(
                                type="integer",
                                id="ID",
                                classes="no_display"
                            ),
                            Input(
                                type="number",
                                id="chiffre",
                            ),
                            Input(
                                type="text",
                                id="raison"
                            ),
                            Input(
                                type="text",
                                validators=[Length(10)],
                                max_length=10,
                                id="date",
                               
                            ),
                            Input(
                                type="text",
                                id="categorie",
                            ),
                            id="montant",
                        ),
                        id="top",
                        ),
                    Horizontal(
                        Vertical(
                            Container(
                                Label(""),
                                Label(""),
                            id="info",
                            ),
                            id="left"
                        ),
                        DataTable(
                            id="table",
                        ),
                        id="middle"
                    ),
                    id = "AddModify"
                ),
                Container(
                    id = "AnalysisPage"
                ),
                id="body",
            ) 
        self.state = 0


###################################################################################






###########################   User Method  ############################


    def activate_user(self, username:str, pwd:str):
        global user
        user = User(username, pwd)

    def connect(self, username:str , pwd:str) -> None:
        """
        Method to connect the user to the app
        """
        # Calling global variables useful in the function
        global users, names, user
            # Check if the user exists
        if username in names:
            # Check if the password is correct
            if username + pwd in users:
                self.query_one("#login", Vertical).remove()
                self.activate_user(username, pwd)
                self.second_page()
                self.state += 1
            else:
                self.try_pwd -= 1
                if self.try_pwd > 0:
                    messages = self.query_one("#errorMessage")
                    self.query_one("#pwd",Input).action_select_all()
                    self.query_one("#pwd",Input).action_end
                    if self.try_pwd == 1:
                        self.query_one(".invalid", Label).remove()
                    messages.mount(Label(f"Mot de passe erroné, il reste {self.try_pwd} tentatives pour le mot de passe.", classes = "invalid",))
                else:
                        messages = self.query_one("#login", Vertical).remove()
                        self.mount(Label("Entrée refusée",classes="invalid"))
                        
        elif self.query_one_optional("#mkuser") == None:
            
            messages = self.query_one("#errorMessage")
            butttonBox = self.query_one("#buttonBox")
            error_label = self.query_one_optional(".invalid", Label)
            if error_label != None :
                error_label.remove() 
            messages.mount(Label("Utilisateur inexistant. Voulez-vous créer cet utilisateur?",id="mkuser"))
            butttonBox.mount(Button("OUI",id="yes",))
            butttonBox.mount(Button("NON",id="no",))

    def makeUser(self):

        global users, names, user

        username = self.query_one("#user", Input).value
        pwd = self.query_one("#pwd", Input).value
        new_user = User(username, pwd)
        user = new_user
        users.append(username + pwd)
        names.append(username)
        fichier.add_object_binary("users_list", users)
        fichier.add_object_binary("names", names)
        self.connect(username, pwd)


###################################################################################





###########################   DATA TABLE Methods   ############################


    def style_ROW(self, ROW: list[str], transaction:Transaction) -> list[Text]:
        """
        Method to style a row of the table
        """
        #Pour le montant
        style_montant = "#53C88B" if transaction.get_montant() >= 0 else "#D9AD54"
        style_texte = "#D2D5CC"
        style_ROW = []
        for cells in ROW:
            if cells == str(transaction.get_montant()):
                style_ROW.append(Text(cells,style=style_montant))           
            else:
                style_ROW.append(Text(cells,style=style_texte))           
            
        return style_ROW
                


    def make_rows(self, user:User):
        """
        Method to make the rows of the table
        """

        table_transactions = self.query_one("#table", DataTable)
        table_transactions.add_column("ID",key="id")
        table_transactions.add_column("Raison",key="raison")
        table_transactions.add_column("Montant",key="montant")
        table_transactions.add_column("Date",key="date")
        historic_transactions = user.get_transactions()
        for transaction in historic_transactions:
            ROW = [str(transaction), str(historic_transactions[transaction].get_raison()) , str(historic_transactions[transaction].get_montant()), str(historic_transactions[transaction].get_date())] 
            style_ROW = self.style_ROW(ROW, historic_transactions[transaction])
            table_transactions.add_row(*(style_ROW),key=str(historic_transactions[transaction].get_id()))

    def make_row(self, transaction:Transaction):
        table_transactions = self.query_one("#table", DataTable)
        ROW = [str(transaction.get_id()),str(transaction.get_raison()) , str(transaction.get_montant()), str(transaction.get_date())]
        style_ROW = self.style_ROW(ROW, transaction)
        table_transactions.add_row(*style_ROW,key=str(transaction.get_id()))

    def changes_cells(self,transaction:Transaction):
        table_transactions = self.query_one("#table", DataTable)
        style = "#53C88B" if transaction.get_montant() >= 0 else "#D9AD54"
        table_transactions.update_cell(str(transaction.get_id()),"raison", Text(str(transaction.get_raison())))
        table_transactions.update_cell(str(transaction.get_id()), "montant", Text(str(transaction.get_montant()),style=style))
        table_transactions.update_cell(str(transaction.get_id()), "date", Text(str(transaction.get_date())))

    async def add_transaction(self):
        global user
        montant = self.query_one("#chiffre", Input)
        raison = self.query_one("#raison", Input)
        date = self.query_one("#date", Input)
        raison_value = raison.value if raison.value != "" else "Aucune raison"
        
        if user is not None:
            if(montant.value != ""):
                if(montant.has_class("invalid")):
                    montant.border_subtitle = "Montant"
                    montant.remove_class("invalid",update=True)

                menu = self.query_one("#options", ListView)
                choix = menu.highlighted_child
                if(re.search(r"^\d{4}\\\d{2}\\\d{2}$", date.value)):
                    year, month, day = date.value.split("\\")
                    if(Validation.IsYear(year) and Validation.IsMonth(month) and Validation.IsDay(day)):
                        date.border_subtitle = "Date (Invalid Date)"
                        date.add_class("invalid",update=True)
                        return
                    else:    
                        date.border_subtitle = "Date"
                        date.remove_class("invalid",update=True)
                elif date.value == "":
                    year, month, day = 0, 0, 0
                    date.border_subtitle = "Date"
                    date.remove_class("invalid",update=True)
                else:
                    date.border_subtitle = "Date (Invalid Date)"
                    date.add_class("invalid",update=True)
                    return
                montant_value = abs(float(montant.value)) if choix.id == "r" else float(montant.value)
                
                new_transaction = Transaction(montant = montant_value, choix = choix.id, raison = raison_value, year = int(year) if Validation.IsYear(year) else None, month = int(month) if Validation.IsMonth(month) else None, day = int(day) if Validation.IsDay(day) else None)
                user.add_transaction(new_transaction)
                self.make_row(new_transaction)
                self.query_one("#solde",Label).update(f"Solde: {sum(user.get_transactions()[id].get_montant() for id in user.get_transactions())}")
                user.save_info()
                raison.action_end()
                raison.action_delete_left_all()
                montant.action_end()
                montant.action_delete_left_all()
                date.action_end()
                date.action_delete_left_all()
            else : 
                montant.border_subtitle = "Montant (Invalid Montant)"
                montant.add_class("invalid",update=True)
                

            
        else:
            raise ValueError("The user hasn't been set and we are yet on second page")

    async def modify_transaction(self):

        global user

        #  Get all informations from the inputs
        id_transaction = self.query_one("#ID", Input)

        montant = self.query_one("#chiffre", Input)
        montant_value = montant.value if montant.value != "" else None

        raison = self.query_one("#raison", Input)
        raison_value = raison.value if raison.value != "" else None

        date = self.query_one("#date", Input)

        year, month, day = date.value.split("\\") if date.value != "" else (None, None, None)


        if user is not None:
            if int(id_transaction.value) <= user.get_last_transaction().get_id() and int(id_transaction.value) >= 0:
                if montant_value is not None:
                    choix = "d" if float(montant.value) >= 0 else "r"
                    if choix == "r":
                        montant_value = str(abs(float(montant_value)))
                else:
                    choix = None
                transaction_to_modify: Transaction = user.get_transactions()[int(id_transaction.value)]
                transaction_to_modify.change_transaction(new_raison = raison_value, new_montant = montant_value, new_choix = choix, new_year = int(year) if Validation.IsYear(year) else None, new_month =int(month) if Validation.IsMonth(month) else None, new_day = int(day) if Validation.IsDay(day) else None)
                user.save_info()
                self.changes_cells(transaction_to_modify)
                self.query_one("#solde",Label).update(f"Solde: {sum(user.get_transactions()[id].get_montant() for id in user.get_transactions())}")
                raison.action_end()
                raison.action_delete_left_all()
                montant.action_end()
                montant.action_delete_left_all()
                date.action_end()
                date.action_delete_left_all()
               
                if(id_transaction.has_class("invalid")):
                    id_transaction = self.query_one('#ID', Input)
                    id_transaction.border_subtitle = "ID"
                    id_transaction.remove_class("invalid",update=True)
                id_transaction.action_end()
                id_transaction.action_delete_left_all() 
            else:
                id_transaction.border_subtitle = "ID (Invalid ID)"
                id_transaction.add_class("invalid",update=True)
        else:
         raise ValueError("The user hasn't been set and we are yet on second page")


###################################################################################






###########################   Stage the page method  ############################


    def on_mount(self)-> None:
        """
        Method called when a mount function is called
        """
        global user
        user = None
        self.query_one("#body").display = False
        # Username
        inputUsername = self.query_one('#user', Input) 
        inputUsername.border_subtitle = "Username"

        # Password
        inputPassword = self.query_one('#pwd', Input) 
        inputPassword.border_subtitle = "Password"
  
    def login_page_treatment(self):
        """Method treating the information entered on the login page"""             
        # Get the information entred
        self.username, self.pwd = self.query_one("#user", Input), self.query_one("#pwd", Input)
        
        if((self.username.is_valid)==False ):
            self.username.border_title = "Username needs to be at least 5 characters"
            self.username.add_class("invalid",update=True)
        else:
            self.username.remove_class("invalid",update=True)
            self.username.border_title = ""
        
        if((self.pwd.is_valid)==False ):
            self.pwd.border_title = "Password needs to be at least 4 characters"
            self.pwd.add_class("invalid",update=True)
        else:
            self.pwd.remove_class("invalid",update=True)
            self.pwd.border_title = ""
        
        if((self.username.is_valid) and (self.pwd.is_valid)):
            self.connect(self.username.value, self.pwd.value)

    def second_page(self):
        """
        Method to display the second page of the app
        """

        global user

        if user is not None:
            self.query_one("#body", Container).display = True
            self.query_one("#AddModify", Container).display = True
            self.make_rows(user)
            labels = self.query_one( "#info")
            labels.remove_children()
            labels.mount(Label(user.get_name()))
            labels.mount(Label(f"Solde: {sum(user.get_transactions()[id].get_montant() for id in user.get_transactions())}",id="solde"))
        # Montant 
        inputChiffre = self.query_one('#chiffre', Input) 
        inputChiffre.border_subtitle = "Montant"

        # Raison
        inputRaison = self.query_one('#raison', Input) 
        inputRaison.border_subtitle = "Raison"
        
        # ID
        inputID = self.query_one('#ID', Input) 
        inputID.border_subtitle = "ID"

        #DATE
        inputDate = self.query_one('#date', Input)
        inputDate.border_subtitle = "Date"
        inputDate.border_title = "AAAA\\MM\\DD"
        if((inputDate.is_valid)==False ):
            inputDate.add_class("invalid",update=True)
        else:
            inputDate.remove_class("invalid",update=True)

        #categorie
        inputCategorie = self.query_one('#categorie', Input)
        inputCategorie.border_subtitle = "Categorie"




        
###################################################################################









###########################   ON_ Method (Event)   ############################
    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        active_tab = event.tab
        if active_tab.id == "add":
            self.query_one("#AddModify", Container).display = True
        elif active_tab.id == "analysis":
            self.query_one("#AddModify", Container).display = False
            self.query_one("#AnalysisPage", Container).display = True
            


    async def on_input_changed(self, event:Input.Changed):
        ##For the date Input:
        input_date = self.query_one("#date",Input)
        string_date = input_date.value

        if re.search(r"^\d{5}$",string_date) or re.search(r"^\d{4}\\\d{3}$", string_date) and input_date.value[-1] != "\\":
            input_date.action_end()
            input_date.action_cursor_left()
            input_date.insert_text_at_cursor("\\")
            input_date.action_end()

        ##For dynamique depot and retrait
        input_montant = self.query_one("#chiffre",Input)
        if input_montant.value != "":
            if input_montant.value[0] == "-" and not self.query_one("#r",ListItem).display:
                self.query_one("#options", ListView).action_cursor_down()
        elif self.query_one("#r", ListItem).display and input_montant.value != "-":
            self.query_one("#options", ListView).action_cursor_up()


        

    async def on_list_view_highlighted(self, event: ListView.Highlighted):
        choice = event.item
        if choice is not None:
            if choice.id == "m":
                choice.display = True
                self.query_one("#r",ListItem).display = False
                self.query_one("#d",ListItem).display = False;


                self.query_one("#ID",Input).display = True
                self.query_one("#chiffre",Input).styles.max_width = '25%'
                self.query_one("#raison",Input).styles.max_width = '25%'
                self.query_one("#date",Input).styles.max_width = '25%'
            else:
                if choice.id == "d":
                    choice.display = True
                    self.query_one("#r",ListItem).display = False
                    self.query_one("#m",ListItem).display = False
                else:
                    choice.display = True
                    self.query_one("#m",ListItem).display = False
                    self.query_one("#d",ListItem).display = False
                self.query_one("#ID",Input).display = False
                self.query_one("#chiffre",Input).styles.max_width = '33%'
                self.query_one("#raison",Input).styles.max_width = '33%'
                self.query_one("#date",Input).styles.max_width = '33%'


        
    async def on_input_submitted(self, event: Input.Submitted):
        """
        Method called by textual when the enter key is pushed on an input
        """
        input_id = str(event.control.id)
        if input_id == "user" or input_id == "pwd": # Login page
            self.login_page_treatment()

        elif (event.control.id == "chiffre" or event.control.id == "raison" or event.control.id == "ID" or event.control.id == "date") and self.query_one("#ID",Input).display == False : # Second page
            await self.add_transaction()
        elif self.query_one("#ID",Input).display == True and (self.query_one("#chiffre",Input).value != "" or self.query_one("#ID",Input).value != ""):
            await self.modify_transaction()
     

    def on_button_pressed(self,event:Button.Pressed):
        button_pressed = event.button.id
        global users, names,user

        if(button_pressed == "yes"):
           self.makeUser()
        elif(button_pressed == "no"):
            txt = self.query_one("#errorMessage")
            buttons = self.query_one("#buttonBox")
            for Label in txt.children:
                Label.remove()
            for button in buttons.children:
                button.remove()
            name = self.query_one("#user",Input)
            pwd = self.query_one("#pwd",Input)
            pwd.action_end()
            pwd.action_delete_left_all()
            name.action_end()
            name.action_delete_left_all()
            name.action_home()


###################################################################################









# Global variables
names = []
users = []

def lauch_ui():
    """
    Method lauching the TUI app
    """
    app = Login()
    app.run()

# Testing environnement of the file
if __name__ == "__main__":
    app = Login()
    app.run()
