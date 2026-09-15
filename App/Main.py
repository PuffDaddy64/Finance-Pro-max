
"""
 Projet : Finances-Pro-Max
 Directory : App
 Name Of File : Main.py
 Author : Thomas Raymond
 Author : Félix Roussin 
 Date : 10 septembre 2026

Description : Main Core of the app.

Note: Le fichier possède actuellent deux fonctions de UI, c'est pour isoler le fonctionnement de TUI de SimpleUI. Afin de mener des tests à différents endroits de l'application.

"""

import UI.SimpleUi as Sui
import UI.Tui

if __name__ == "__main__":
    Tui = False
    if Tui:
        UI.Tui.lauch_ui()
    else:
        Sui.simple_ui()
