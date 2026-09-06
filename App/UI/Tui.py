from textual import on
from textual.app import App,ComposeResult
from textual.containers import Container, Horizontal,Vertical
from textual.widgets import Header, Footer, Button, Input, Label,Pretty
from textual.validation import Length, Validator







class End(Button):

    num : int  = 0 


    def action_press(self):
        self.num += 1
        
        if(self.num%2 != 0):
            self.label = "press"
            self.add_class("press")
        else:
            self.label = "ass"
            self.remove_class("press")
            





class Login(App):
    CSS_PATH="TCSS/login.tcss"


    #BINDINGS[]


    def compose(self) -> ComposeResult:
        yield Vertical(

            Label("$$$$$$$\\  $$\\   $$\\ $$$$$$$\\   $$$$$$\\  $$$$$$$$\\ $$$$$$$$\\ \n$$  __$$\\ $$ |  $$ |$$  __$$\\ $$  __$$\\ $$  _____|\\__$$  __|\n$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ /  \\__|$$ |         $$ |\n$$$$$$$\\ |$$ |  $$ |$$ |  $$ |$$ |$$$$\\ $$$$$\\       $$ |\n$$  __$$\\ $$ |  $$ |$$ |  $$ |$$ |\\_$$ |$$  __|      $$ |\n$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |         $$ |\n$$$$$$$  |\\$$$$$$  |$$$$$$$  |\\$$$$$$  |$$$$$$$$\\    $$ |\n\\_______/  \\______/ \\_______/  \\______/ \\________|   \\__|"),
                Horizontal(
                  Container(
                        Input(
                            id="user",
                             ),
                        
                    ), 
                  Container(
                    Input(id="pass",
                        password=True,),
                    
                    ), 
                ),
        )
    def on_mount(self)-> None:
        inputUser = self.query_one(('#user')) 
        inputUser.border_subtitle = "Username"
        inputUser = self.query_one(('#pass')) 
        inputUser.border_subtitle = "Password"       


if __name__ == "__main__":
    app = Login()
    app.run()
