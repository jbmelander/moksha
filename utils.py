import os
import pathlib
import json
import curses

class Config:
    def __init__(self):
        data = self.get_data()

    def get_data(self):
        top_dir = os.path.split(os.path.abspath(__file__))[0]
        json_path= os.path.join(top_dir,'configs/config.json')

        
        with open(json_path,'r') as f:
            data = json.load(f)

        for k,v in data.items():
            setattr(self,k,ConfigType())

            if k == 'Palette':
                obj = getattr(self,k)
                colorpairs = init_colors()
                for style,color in v.items():
                    setattr(obj,style,colorpairs[color])
            else:
                obj = getattr(self,k)
                for attribute, choice in v.items():
                    setattr(obj,attribute,choice)


            

class ConfigType:
    def __init__(self):
        pass

def init_colors():
    colors = ['white','black','red','green','cyan','magenta','yellow','blue']
    colorpairs = {}
    
    counter = 1
    for ci,c_fg in enumerate(colors):
        for cj,c_bg in enumerate(colors):
            if ci != cj:
                fg ='COLOR_{}'.format(c_fg).upper()
                bg ='COLOR_{}'.format(c_bg).upper()
                curses.init_pair(counter,getattr(curses,fg),getattr(curses,bg))
                key = c_fg + '_' + c_bg
                colorpairs[key] = curses.color_pair(counter)
                counter+=1

    return colorpairs

def linedraw(win,*args):
    try:
        win.addstr(*args)

    except curses.error:
        pass
