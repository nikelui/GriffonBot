# GriffonBot [ITA]
Un bot multi-funzione in Python, sviluppato per il server Discord della [Gilda del Grifone](http://www.gildadelgrifonetorino.it/).  
[Vienici a trovare](https://www.facebook.com/LaGildadelGrifone)  

## Dipendenze
- Discord.py (https://github.com/Rapptz/discord.py)
- d20 (https://pypi.org/project/d20/)
- dotenv (https://pypi.org/project/python-dotenv/)

**Nota**: per autenticare il bot, copiare il token di accesso in un file chiamato `.env` nella stessa cartella degli script. Il file deve contenere una riga del tipo:
```
BOT_TOKEN=<token_segreto_qui>
```

## Funzionalità
* Tira dadi, mediante la libreria d20 ([sintassi dei dadi](https://d20.readthedocs.io/en/latest/start.html#dice-syntax))
* _Dado semaforo_ per il gioco di ruolo [Crossdoom](https://www.crossdoom.it/)
* Risoluzione degli attacchi secondo le regole di [Crossdoom](https://www.crossdoom.it/) [_WORK IN PROGRESS_]
* Dichiara un mazzo di carte e distribuiscile [_WORK IN PROGRESS_]

## Comandi
Per eseguire un comando, digitare il prefisso `g.` seguito dal nome del comando:

* `  g.help` -> mostra i comandi disponibili
* `  g.roll` -> tira dadi usando un'espressione del tipo `NdX`.
* `g.attack` -> tira dadi (vedi \<roll>) e risolvi attacco secondo regole di Crossdoom
* `  g.deal` -> distribuisci carte [work in progress]
* `  g.quit` -> disconnetti il bot (solo per sviluppatore)

Per maggiori informazioni su uno specifico comando, digitare `g.help <nome_comando>`

### comando g.roll \<espressione>
Tira un dado usando un'espressione del tipo `NdX`:
- **N**: numero di dadi [int]
- **X**: tipo di dado [int o 's']
  - l'espressione `Nds` viene usata per tirare **N** _dadi semaforo_.

**Restituisce**: singoli valori dei dadi e somma dei tiri

Per maggiori informazioni sulla sintassi utilizzata:
[https://d20.readthedocs.io/en/latest/start.html#dice-syntax](https://d20.readthedocs.io/en/latest/start.html#dice-syntax)


# GriffonBot [ENG]
A multi-purpose RPG companion bot in Python, developed for the discord server of la [Gilda del Grifone](http://www.gildadelgrifonetorino.it/).  
[Visit us](https://www.facebook.com/LaGildadelGrifone)  

**Note**: To authenticate the bot, you need to place your discord token in a file called `.env` in the same directory as the scripts, containing the following line:
```
BOT_TOKEN=<secret_token_here>
```

## Dependencies
- Discord.py (https://github.com/Rapptz/discord.py)
- d20 (https://pypi.org/project/d20/)
- dotenv (https://pypi.org/project/python-dotenv/)

## Features
* Dice roller using d20 library ([dice syntax](https://d20.readthedocs.io/en/latest/start.html#dice-syntax))
* Dado semaforo for [Crossdoom](https://www.crossdoom.it/) rpg
* Attack resolution with the rules from [Crossdoom](https://www.crossdoom.it/) rpg [_WORK IN PROGRESS_]
* Prepare a deck and deal cards [_WORK IN PROGRESS_]

## Commands
To run a command, write the prefix `g.` followed by the command name:

* `  g.help` -> show available commands
* `  g.roll` -> roll dices using an expression of the kind `NdX`
* `g.attack` -> roll dices (see \<roll>) and solve attack using Crossdoom rules
* `  g.deal` -> deal cards [work in progress]
* `  g.quit` -> disconnect the bot (developer only)

For more information about a specific command, write `g.help <command_name>`

### command g.roll \<expression>
Roll dices with an expression of the kind `NdX`:
- **N**: number of dices [int]
- **X**: type of dices [int o 's']
  - the expression `Nds` is used to roll **N** _dadi semaforo_.

**Return**: single rolls and sum of dices.

For more info on the used syntax:
[https://d20.readthedocs.io/en/latest/start.html#dice-syntax](https://d20.readthedocs.io/en/latest/start.html#dice-syntax)
