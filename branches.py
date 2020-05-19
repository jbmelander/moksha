import curses
import curses.textpad as textpad
import time
from utils import linedraw
from utils import Config
from widgets import dialog_popup,warning_popup,return_ascii_title,group_popup

class Base:
    """Base branch that handles all drawing"""

    def __init__(self,
            main_text,
            parent=None,
            children=None,
            root=False,
            apical=True,
            ID=None,
            group_membership=None):

        # Display message
        self.main_text = main_text
        self.ID = ID

        # Store IDs of hierarchically adjacent leaves
        self.parent = parent
        
        if children == None:
            self.children = []

        if group_membership == None:
            self.group_membership = []

        elif type(group_membership) is not list:
            self.group_membership = [group_membership]

        # Binary flags for top and bottom, respectively
        self.root = root 
        self.apical = True


    def inline_draw(self,screen,x,y,config):
        P = config.Palette
        KB = config.Bindings
        DISP = config.Display
        
        if self.apical:
            linedraw(screen,x,y,DISP.MainDelimiter+self.main_text + DISP.NoChildrenMarker,P.Default)
        else:
            linedraw(screen,x,y,DISP.MainDelimiter+self.main_text + DISP.HasChildrenMarker,P.Default)

    def draw(self,stdscr,tree,config):
        P = config.Palette
        KB = config.Bindings
        DISP = config.Display
        CO = config.Coordinates

        pos = 0
        last_pos = None

        y,x = stdscr.getmaxyx()
        key = None

        while key !='\n':
            stdscr.clear()
            n_children = len(self.children)
            last_pos = pos
            #Draw the group bar

            try:
                stdscr.chgat(CO.GroupBarY,0,x,P.GroupBar)
            except curses.error:
                pass


            y,x = stdscr.getmaxyx()
             
            num_groups = len(tree.group_data)
            current_group = tree.GROUPIDX
            group_name = tree.group_data[tree.GROUPIDX].name

            G_x = 1
            GSTR = 'Groups: |'
            linedraw(stdscr,CO.GroupBarY,G_x,GSTR,P.GroupBar)
            G_x += len(GSTR)

            for g in range(num_groups):
                
                GSTR = 'G'+str(g) 
                if g == current_group:
                    style = P.GroupBarHighlight
                else:
                    style = P.GroupBar
                linedraw(stdscr,CO.GroupBarY,G_x,GSTR,style)

                G_x += len(GSTR)
                linedraw(stdscr,CO.GroupBarY,G_x,'|',P.GroupBar)
                G_x +=1

            group_cur_text = group_name + ' [{} Branches]'.format(len(tree.group_data[tree.GROUPIDX].branches))
            linedraw(stdscr,CO.GroupBarY,x-len(group_cur_text)-2,group_cur_text,P.GroupBarCurrent)

            # Draw Title Bar

            TITLE_STRING = return_ascii_title()
            n_title_lines = len(TITLE_STRING)
            SUBTITLE_STRING = "Free Your Mind"
            
            TitleY = CO.GroupBarY + CO.TitleOffset 
            for nt in range(n_title_lines):
                try:
                    stdscr.chgat(TitleY+nt,0,x,P.TitleBar)
                except curses.error:
                    pass
            SubTitleY = n_title_lines+1
            BranchTextY = CO.BranchTextOffset + SubTitleY + 1
            stdscr.chgat(SubTitleY,0,x,P.SubTitleBar)
            stdscr.chgat(BranchTextY,0,x,P.BranchText)

            TitleX = int(x/2) - int(len(TITLE_STRING[0])/2)
            SubTitleX = int(x/2) - int(len(SUBTITLE_STRING)/2)
    
            for ti,t in enumerate(TITLE_STRING):
                linedraw(stdscr,
                        TitleY+ti,
                        TitleX,
                        t,
                        P.Title)

            linedraw(stdscr,
                    SubTitleY,
                    SubTitleX,
                    SUBTITLE_STRING,
                    P.SubTitle)

            # Draw main text below title 
            linedraw(stdscr, 
                    BranchTextY,
                    CO.BranchTextX,
                    self.main_text,
                    P.BranchText)
            
            
            # Print children
            ChildrenY = BranchTextY + CO.ChildrenOffset + 1
            for i,c in enumerate(self.children):
                # Draw children's inline functions
                child = tree.data[c]

                child.inline_draw(stdscr,
                        ChildrenY+i,
                        CO.ChildrenX,
                        config)
            
                if pos == i:# Draw in Position Marker 
                    MarkerY = ChildrenY + pos
                    linedraw(stdscr,MarkerY,0,DISP.PositionMarker,P.PositionMarker)
                else:
                    pass

            # Draw position marker in empty branhces
            # if n_children == 0:
            #     MarkerY = ChildrenY + CO.BackOffset + n_children - 1
            #     linedraw(stdscr,n_children+CO.BackOffset+CO.ChildrenY-1,0,DISP.PositionMarker,P.PositionMarker)

            # Draw Back text
            BackY = ChildrenY + CO.BackOffset + n_children

            try:
                stdscr.chgat(BackY,0,x,P.BackBG)
            except curses.error:
                pass

            if pos == n_children:# In the case of the back text
                MarkerY = ChildrenY + CO.BackOffset + n_children
                linedraw(stdscr,MarkerY,0,DISP.PositionMarker,P.BackPositionMarker)
            if self.root:
                linedraw(stdscr,BackY,CO.BackX,'Return to Shell'.upper(),P.BackText)
            else:
                if len(tree.data[self.parent].main_text) > 10:
                    backstring = 'Return to {}'.format(tree.data[self.parent].main_text[:10]) + '...'
                else:
                    backstring = 'Return to {}'.format(tree.data[self.parent].main_text)

                linedraw(stdscr,BackY,CO.BackX,backstring.upper(),P.BackText)

            # Draw Status Bar on bottom of screen
            if tree.saved:
                style = P.Saved
                savestring = 'Saved'.upper()

            elif tree.saved == False:
                style = P.Unsaved
                savestring = 'Unsaved'.upper()

            linedraw(stdscr,y-1,x-len(savestring),savestring)
            linedraw(stdscr,y-1,0,'File: {}'.format(tree.filepath))
            
            try:
                stdscr.chgat(y-1,0,x,style)
            except curses.error:
                pass

            # Refresh and get key 
            stdscr.refresh()
            key = stdscr.getkey() # Gets user input

               
            if key == 'KEY_RESIZE':
                y,x = stdscr.getmaxyx()

            elif key in [str(p) for p in range(10)]: # limited to 9
                tree.GROUPIDX = int(key)

            elif  key in KB.Down:
                if pos < n_children:
                    pos += 1
                else: 
                    pos = 0

            elif key in KB.Up:
                if pos > 0:
                    pos += -1
                else:
                    pos = n_children

            elif key in KB.Back:
                return (n_children,tree)

            elif key in KB.AddToGroup:
                item_idx = tree.data[tree.IDX].children[pos]
                ch = stdscr.getch()

                if ch >= ord('0') and ch < ord('9'):
                    group_num = ch - ord('0')
                    tree.group_add(item_idx,group_num)

                elif ch == ord('g'):
                    tree.group_add(item_idx,tree.GROUPIDX)
                
            elif key in KB.OpenGroupPopup:
                tree = group_popup(stdscr,tree)
                return (-2,tree)
                

            elif key in KB.Save:
                if hasattr(tree,'filepath'):
                    tree.save()
                else:
                    inp = dialog_popup(stdscr,'First Save Filepath')
                    tree.save_as(inp)

            elif key in KB.SaveAs:
                inp = dialog_popup(stdscr,'Save As Filepath')
                tree.save_as(inp)
                
            elif key in KB.Load:
                inp=dialog_popup(stdscr,'Load Filepath')
                tree.load(inp)

            elif key in KB.NewBaseBranch:
                inp = dialog_popup(stdscr,'Main Text: ')
                tree.mkbranch(inp)

            elif key in KB.GoToRoot:
                tree.IDX = 0
                return (pos,tree)


            elif key in KB.RmBranch:
                if pos != n_children:
                    if warning_popup(stdscr,process_description='Recursively deleting selected node'):
                            tree.rmrfbranch(self.children[pos])

            elif key in KB.Quit:
                if warning_popup(stdscr,process_description='Returning to shell'):
                    if warning_popup(stdscr,process_description='Autosaving session'):
                        tree.save()
                    else:
                        pass
                    return (-1,tree)
                else:
                    pass
            elif key in KB.QuickQuit:
                tree.save()
                return (-1,tree)
            else:
                pass 
                
        return (pos,tree)


class Calendar(Base):
    def __init__(self,
        main_text,
        parent=None,
        children=[],
        root=False,
        apical=True,
        ID=None,
        date=None,
        time=None):

        super(Calendar,self).__init__(
                main_text = main_text,
                parent = parent,
                children = children,
                root = root,
                apical = apical,
                ID = ID)

        self.due = date + ' ' + time
        # self.time = time
        # self.month = month
        # self.year = year
        # self.day = day
        # self.planned=planned
        # self.finished=finished
        # self.where=where
        # self.who=who
         

    # def inline_draw(self,screen,x,y,config):
    #     P = config.Palette
    #     KB = config.Bindings
    #     DISP = config.Display
    #     CO = config.Coordinates 

    #     if self.apical:
    #         linedraw(screen,x,y,DISP.MainDelimiter+self.main_text,P.Default)
    #         linedraw(screen,x,CO.DueDateX,'Due: {}'.format(self.due),P.CalInline)
        # else:
        #     linedraw(screen,x,y,DISP.MainDelimiter+self.main_text + DISP.HasChildrenMarker,P.Default)
        #     linedraw(screen,x,CO.DueDateX,'Due: {}'.format(self.due),P.CalInline)



