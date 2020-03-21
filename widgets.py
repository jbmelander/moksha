import curses
import curses.textpad as textpad
from utils import Config,linedraw
import calendar

def group_popup(screen,tree):
    config = Config()
    P = config.Palette
    KB = config.Bindings
    DISP = config.Display
    CO = config.Coordinates
    
    y,x = screen.getmaxyx()
    screen.clear()
    GroupPopupStart = 6
    dlg = screen.derwin(int(y-GroupPopupStart),int(x/2),GroupPopupStart,int(x/4)+1)

    dlg.bkgd(' ',P.GroupPopupText)
    dlgy,dlgx = dlg.getmaxyx()
    
    out = 0
    group_pos = 0
    while out is not -1:
        (out,tree,group_pos) = tree.group_data[tree.GROUPIDX].draw(dlg,tree,group_pos)
    

    return tree



    
def warning_popup(screen,process_description):
    config = Config()
    P = config.Palette
    KB = config.Bindings
    DISP = config.Display

    y,x = screen.getmaxyx()
    
    dlg = screen.derwin(3,x,int(y/2),0)
    dlg.bkgd(' ',P.WarningPopupBG)
    
    linedraw(dlg,1,1,process_description)
    linedraw(dlg,1,len(process_description)+1,'. Proceed? [y/n]')

    inp = dlg.getkey()

    if inp in ['y','Y']:
        inp = 1
    elif inp in ['n','N']:
        inp = 0
    elif inp == 'KEY_RESIZE':
        return 0
    else: 
        inp = dlg.getkey()
    
    dlg.clear()
    dlg.refresh()
    screen.refresh()
    return inp

def dialog_popup(screen,title,stripe_style=None,text_style=None):
    config = Config()
    P = config.Palette
    KB = config.Bindings
    DISP = config.Display

    maxyx = screen.getmaxyx()
    y = maxyx[0]
    x = maxyx[1]

    screen.clear()
    screen.refresh()
    dlg = screen.derwin(int(y/4),x,int(y/2)-3,0)

    dy,dx = dlg.getmaxyx()     
    
    if stripe_style == None:
        dlg.chgat(1,0,x,P.DialoguePromptStripe)
        dlg.chgat(5,0,x,P.DialoguePromptStripe)
    else:
        dlg.chgat(1,0,x,stripe_style)
        dlg.chgat(5,0,x,stripe_style)
    
    if text_style == None:
        dlg.addstr(0,1,title,P.DialoguePromptText)
    else:
        dlg.addstr(0,1,title,text_style)


    curses.echo()

    inp = dlg.getstr(3,1).decode('utf-8')

    curses.noecho()
     
    dlg.clear()
    dlg.refresh()
    screen.refresh()

    return inp


def return_ascii_title():
    ascii_title = ["   __  ___  ____    __ __   ____   __ __   ___ ",
                   "  /  |/  / / __ \  / //_/  / __/  / // /  / _ |",
                   " / /|_/ / / /_/ / / ,<    _\ \   / _  /  / __ |",
                   "/_/  /_/  \____/ /_/|_|  /___/  /_//_/  /_/ |_|",
                   "                                               "]
    return ascii_title
                                               


