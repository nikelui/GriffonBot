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
* _Dado del destino_ per il gioco di ruolo [Crossdoom](https://www.crossdoom.it/)
* _Dado fantasma_ per il gioco di ruolo [Ghostbusters](https://ghostbusterscities.com/media/ghostbusters-the-roleplaying-game/)
* Risoluzione degli attacchi secondo le regole di [Crossdoom](https://www.crossdoom.it/) [_WORK IN PROGRESS_]
* Dichiara un mazzo di carte e distribuiscile [_COMING SOON_]

## Comandi
Per eseguire un comando, digitare il prefisso `g.` seguito dal nome del comando:

* `  g.help` o `  g.h` -> mostra i comandi disponibili
* `  g.roll` o `  g.r` -> tira dadi usando un'espressione del tipo `NdX`.
* `g.attack` o `g.atk` -> tira dadi (vedi \<roll>) e risolvi attacco secondo regole di Crossdoom
* ` g.ghost` o ` g.gh` -> tira dadi a 6 facce, incluso un dado fantasma, secondo il regolamento di Ghostbusters
* `  g.deal` -> distribuisci carte [COMING SOON]
* `  g.quit` -> disconnetti il bot (solo proprietario)

Per maggiori informazioni su uno specifico comando, digitare `g.help <nome_comando>`

### comando g.r \<espressione>
Tira un dado usando un'espressione del tipo `NdX`:
- **N**: numero di dadi [int]
- **X**: tipo di dado [int o 's']
  - l'espressione `Nds` viene usata per tirare **N** _dadi del destino_.

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
* _Destiny dice_ for [Crossdoom](https://www.crossdoom.it/) rpg
* _Ghost dice_ for Ghostbusters (https://ghostbusterscities.com/media/ghostbusters-the-roleplaying-game/) rpg
* Attack resolution with the rules from [Crossdoom](https://www.crossdoom.it/) rpg [_WORK IN PROGRESS_]
* Prepare a deck and deal cards [_COMING SOON_]

## Commands
To run a command, write the prefix `g.` followed by the command name:

* `  g.help` or `  g.h` -> show available commands
* `  g.roll` or `  g.r` -> roll dices using an expression of the kind `NdX`
* `g.attack` or `g.atk` -> roll dices (see \<roll>) and solve attack using Crossdoom rules
* ` g.ghost` or ` g.gh` -> roll 6-sided dices with a _ghost dice_ using Ghostbuster rules
* `  g.deal` -> deal cards [COMING SOON]
* `  g.quit` -> disconnect the bot (owner only)

For more information about a specific command, write `g.help <command_name>`

### command g.roll \<expression>
Roll dices with an expression of the kind `NdX`:
- **N**: number of dices [int]
- **X**: type of dices [int o 's']
  - the expression `Nds` is used to roll **N** _destiny dice_.

**Return**: single rolls and sum of dices.

For more info on the used syntax:
[https://d20.readthedocs.io/en/latest/start.html#dice-syntax](https://d20.readthedocs.io/en/latest/start.html#dice-syntax)


# Crossdoom BOT [ITA]
Un bot dedicato per il gioco di ruolo [Crossdoom](https://www.crossdoom.it/)

## Tiri di dadi
- `?NdX`: tira N dadi a X facce
- `?Nds`: tira N dadi del destino
- `!NdX`: tira N dadi a X facce e risolve l'attacco secondo le regole di Crossdoom

## Altri comandi
- `c.help`: mostra i comandi disponibili
- `c.quit`: disconnetti il bot (solo proprietario)

# Crossdoom BOT [ENG]
A dedicated bot for the roleplaying game [Crossdoom](https://www.crossdoom.it/)

## Dice rolls
- `?NdX`: roll N dices with X sides
- `?Nds`: roll N _destiny dices_
- `!NdX`: roll N dices with X sides and solve attack using Crossdoom rules

## Altri comandi
- `c.help`: show available commands
- `c.quit`: disconnect the bot (owner only)
