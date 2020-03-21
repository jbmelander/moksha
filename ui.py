import curses                                                                   
from curses import wrapper
import yaml                                                                     
import os
from utils import Config
import numpy as np                                                              
import branches
from widgets import warning_popup
# Main session                                                     
class Session:
    def __init__(self,stdscr,tree):
        self.stdscr = stdscr
        self.config = Config()
        self.mainloop(tree)

    def mainloop(self,tree):
        obj = tree.data[0] 
        (pos,tree) = obj.draw(self.stdscr,tree,self.config)
        
        '''
        Obj.Draw is branch-specific
        Return from Obj.Draw of -1 means quit
        '''
        while pos is not -1: 
            if pos == len(obj.children): # If back selected
                if tree.IDX == 0: # If root
                    if warning_popup(self.stdscr,process_description = 'Returning to shell'):
                        if warning_popup(self.stdscr,'Autosaving session'):
                            tree.save()
                        else:
                            pass
                        return 0
                    else:
                        pass
                else: # Change tree index to parent
                    tree.IDX = tree.data[tree.IDX].parent

            elif pos >= 0: # If child selected, change index to that child
                tree.IDX = tree.data[tree.IDX].children[pos]

            else:
                pass
            

            obj = tree.data[tree.IDX] # Get current branch object
            (pos,tree) = obj.draw(self.stdscr,tree,self.config) # Invoke that branchobj's draw method
            
            self.stdscr.clear() #Clear screen

        return 0
 

