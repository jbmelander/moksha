import os
import yaml
from utils import linedraw, Config
from widgets import dialog_popup,warning_popup,return_ascii_title,group_popup
class Base:
    def __init__(self,groupname):
        self.name = groupname
        self.branches = []

    def draw(self,screen,tree,pos=0):
        config = Config()
        P = config.Palette
        KB = config.Bindings
        DISP = config.Display
        

        pos = pos
        last_pos = None
        y,x = screen.getmaxyx()
        key = None

        while key != '\n':
            screen.clear()
            n_branches = len(self.branches)
            last_pos = pos
            y,x = screen.getmaxyx()
            
            linedraw(screen,0,0,'Group # {}: {}'.format(tree.GROUPIDX,self.name),P.GroupPopupTitle)

            itemize_start = 3
            g_y = itemize_start
            for i,b in enumerate(self.branches):
                branch = tree.data[b]
                linedraw(screen,g_y,3,'{}. '.format(i+1) + branch.main_text,P.GroupPopupText)
            
                if pos == i:# Draw in Position Marker 
                    MarkerY = itemize_start + pos
                    linedraw(screen,MarkerY,0,DISP.GroupPopupPositionMarker,P.GroupPositionMarker)
                else:
                    pass
                g_y += 1

             
            key = screen.getkey()
            
            if key == 'KEY_RESIZE':
                y,x = screen.getmaxyx()

            elif key in [str(p) for p in range(10)]: # limited to 9
                tree.GROUPIDX = int(key)
                screen.clear()
                return (0,tree,pos)

            elif  key in KB.Down:
                if pos < n_branches-1:
                    pos += 1
                else: 
                    pos = 0

            elif key in KB.Up:
                if pos > 0:
                    pos += -1
                else:
                    pos = n_branches-1

            elif key in KB.GroupReset:
                if warning_popup(screen,process_description='Resetting current group'):
                    tree.group_reset()
                    return (0,tree,pos)
                
            elif key in KB.GroupRename:
                self.name = dialog_popup(screen,'New Group Name',P.GroupDialogStripe,P.GroupDialogText)
                return (0,tree,pos)

            elif key in KB.GroupRmRf:
                if warning_popup(screen,'Recursively deleting selected branch'):
                    tree.rmbranch(self.branches[pos])
                    return (0,tree,pos-1)

            elif key in KB.GroupRemove:
                tree.group_rm(self.branches[pos],tree.GROUPIDX)
                return (0,tree,pos-1)

            elif key in KB.Quit:
                break

            elif key in KB.GroupGoTo:
                tree.IDX = tree.group_data[tree.GROUPIDX].branches[pos]
                break

            elif key in KB.NewBaseBranch:
                temp = tree.IDX
                tree.IDX = 0
                root_branches = tree.data[0].children

                ug_exists = False
                ug_id = None

                for rb in root_branches:
                    if tree.data[rb].main_text == 'Ungrouped':
                        ug_id = rb
                        ug_exists = True

                if not ug_exists:
                    tree.mkbranch('Ungrouped')
                    ug_id = tree.MAX

                tree.IDX = ug_id
                txt = dialog_popup(screen,'New Branch (Ungrouped)',P.GroupDialogStripe,P.GroupDialogText)
                tree.mkbranch(txt)
                tree.group_add(tree.MAX,tree.GROUPIDX)
                tree.saved = False
                tree.IDX = temp

                return(0,tree,pos)



        return (-1,tree,pos)





