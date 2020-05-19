# Moksha
## To Start:
1. Edit `../moksha/configs/config.json` so that the last entry in the json, called `PathDef` points to the directory and filename that you would like to use for your save file.
2. Make sure you have python's `curses` library installed
3. In a __full-screen__ terminal, `cd` to the `moksha/` directory and run:
``python3 main.py``

__Moksha__ is an extensible, customizable CLI (written with a __Python 3__ and __ncurses__ backend) that aims to embed the user's redundant, fleeting and high-dimensional mental-processes into a single hierarchical and archival data-structure. _In other words, it's a todo/calendar/journaling/note-taking/organizer for your terminal._

# Config
* Colors, draw coordinates, and keybindings can be modified in /moksha/configs/config.json

# Key Bindings

* `n` = New branch
* `d` = Delete selected branch
* `#` - Change active group
* `gg` - Add current item to active group
* `g#` = Add current item to group #

* `SPACE` - Enter group menu. __In Group Menu:__
    * `R` - Reset group
    * `r` - Rename group
    * `d` - Remove from group
    * `D` - Remove from group and delete from tree
    * `m` = Go to item in tree
    *
* `s` = Save
* `S` = Save As
* `L` - Load
* `j,k` or `ARROW KEYS` - Move up and down
* `q` - Quit
* `Q` - QuickQuit


