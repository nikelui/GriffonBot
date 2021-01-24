help_dict = {
'roll':{
'ITA':"""Sintassi: `g.roll <espressione>`
Tira un dado usando un'espressione del tipo `NdX`:
- N: numero di dadi [int]
- X: tipo di dado [int o 's']
     l'espressione `Nds` viene usata per tirare N **dadi del destino** (verde, giallo rosso).

Restituisce: singoli valori e somma dei tiri

Per maggiori informazioni sulla sintassi utilizzata:
https://d20.readthedocs.io/en/latest/start.html#dice-syntax
""",
'ENG':"""Syntax: `g.roll <expression>`
Roll a dice using an expression of the kind `NdX`:
- N: number of dices [int]
- X: type of dices [int or 's']
     the expression `Nds` is used to roll N **destiny dice** (green, yellow, red).

Returns: single values and sum of rolls

Fore more info on the dice syntax:
https://d20.readthedocs.io/en/latest/start.html#dice-syntax
"""},

'attack':{
'ITA':"""Sintassi: `g.attack <espressione>`
Tira un dado usando un'espressione (vedi `g.help roll`) e calcola il risultato dell'attacco secondo il regolamento di Crossdoom.

Restituisce: singoli valori e risultato dell'attacco

Per maggiori informazioni sulla sintassi utilizzata:
https://d20.readthedocs.io/en/latest/start.html#dice-syntax
Per il regolamento di Crossdoom:
https://www.crossdoom.it/
""",
'ENG':"""Syntax: `g.attack <expression>`
Roll a dice using an expression (see `g.help roll`) and resolve the attack using the rules from Crossdoom rpg.

Returns: single values and attack result.

For more info on the dice syntax:
https://d20.readthedocs.io/en/latest/start.html#dice-syntax
About Crossdoom (ITA):
https://www.crossdoom.it/
"""
},

'quit':{
'ITA':"""Sintassi: `g.quit`
[Solo per sviluppatore] Disconnette il bot dal server e lascia una citazione random. Punti extra se si indovina la fonte.""",
'ENG':"""Syntax: `g.quit`
[developer only] Disconnect the bot from the server and gives a random quote (Italian only). Extra points if you can guess the source."""
},

'deal': {
'ITA':"""Sintassi: `g.deal N`
Pesca N carte da un mazzo preesistente nel canale e le assegna all'autore del comando.
[**WORK IN PROGRESS**]""",
'ENG':"""Syntax: `g.deal N`
Draw N cards from a pre-existing deck in the channel and assign them to the author of the command.
[**WORK IN PROGRESS**]"""
},

'help': {
'ITA':"""`g.help` -> mostra una lista dei comandi disponibili
`g.help <comando>` -> mostra informazioni dettagliate su un signolo comando.""",
'ENG':"""`g.help` -> show a list of the available commands.
`g.help <command>` -> show detailed help about a command."""
},

'ghost': {
'ITA':"""Sintassi: `g.ghost N`
Tira N-1 dadi a 6 facce, più un _dado fantasma_, usando il regolamento del gioco di ruolo di [Ghostbusters](https://ghostbusterscities.com/media/ghostbusters-the-roleplaying-game/).""",
'ENG':"""Syntax: `g.ghost N`
Roll N-1 6-sided dices plus a _ghost die_, according to the rules of [Ghostbusters rpg](https://ghostbusterscities.com/media/ghostbusters-the-roleplaying-game/)."""
}

}