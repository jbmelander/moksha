import os
import curses
import yaml

import branches
import groups
from utils import Config

class Tree:
    def __init__(self):
        # Current branch and current leaf ID counter
        self.IDX = 0
        self.GROUPIDX = 1
        self.MAX = 0
    
        # Initialize data dictionary
        self.data = {}
        self.data[0] = branches.Base(main_text='Root',
                parent=None,
                children = None,
                root=True,
                apical=False,
                ID=0)
        
        # Some default branches for the frist-time user
        self.mkbranch('This is the first leaf')
        self.mkbranch('You can delete these and add your own.')
        self.mkbranch('Enjoy!')

        # Initialize empty group container
        self.group_data = []
        self.num_groups = 0
        
        self.mkgroup('Urgent')
        self.mkgroup('Today')
        self.mkgroup('Tomorrow')
        self.mkgroup('Upcoming')
        self.mkgroup('Random Thoughts')
        self.mkgroup('Misc')
        self.mkgroup('Misc')
        self.mkgroup('Misc')
        self.mkgroup('Misc')
        self.mkgroup('Misc')

        self.saved=False
# Self groups
    def mkgroup(self,params,group_type='Base'):
        if type(params) == str:
            temp = params
            params = {}
            params['groupname'] = temp
        
        group_obj = getattr(groups,group_type)
        g = group_obj(**params)
        self.group_data.append(g)

    
    def group_add(self,branch_idx,group_idx):#idxs
        if branch_idx not in self.group_data[group_idx].branches:
            self.group_data[group_idx].branches.append(branch_idx) # Add to group.branches
            self.data[branch_idx].group_membership.append(group_idx) # Add membership flag to branch

    def group_reset(self):
        for b in self.group_data[self.GROUPIDX].branches:
            branch = self.data[b]
            branch.group_membership.remove(self.GROUPIDX)

        self.group_data[self.GROUPIDX].branches = []

    def group_rm(self,branch_idx,group_idx):#idxs
        self.group_data[group_idx].branches.remove(branch_idx)
        self.data[branch_idx].group_membership.remove(group_idx)



    def save(self):
        if hasattr(self,'filepath'):
            self.saved = True
            with open(self.filepath,'w') as f:
                yaml.dump(self,f)
        else:
            pass
            
    def save_as(self,fpath):
        self.filepath = fpath
        self.saved=True
        with open(self.filepath,'w') as f:
            yaml.dump(self,f)


    def load(self,fpath):
        
        with open(fpath,'r') as f:
            load_tree=yaml.load(f,Loader=yaml.FullLoader)

        for k,v in load_tree.__dict__.items():
            if hasattr(self,k):
                delattr(self,k)
            setattr(self,k,v)

        self.IDX = 0
        
        
    def mkbranch(self,params,branch_type='Base'):
        # Increment leaf count and assign new ID self.MAX += 1
        if type(params) is not dict:
            temp = params
            params = {}
            params['main_text'] = temp
            print('P')

            
        self.MAX += 1

        branch_obj = getattr(branches,branch_type)

        # Add leaf_id to current branch's children and change root flag
        self.data[self.IDX].children.append(self.MAX)
        self.data[self.IDX].apical = False


        # Create leaf object
        self.data[self.MAX] = branch_obj(**params,
                parent = self.IDX,
                ID = self.MAX)

        self.saved=False

    def rmbranch(self,IDX):
        # Remove from parent's children list
        parent_id = self.data[IDX].parent
        self.data[parent_id].children.remove(IDX)
        
        for g in self.data[IDX].group_membership:
            self.group_rm(IDX,g)
        # Delete object
        del self.data[IDX]
        
        # If all are deleted, restore terminal status
        if len(self.data[parent_id].children) == 0:
            self.data[parent_id].apical = True

    def rmrfbranch(self,IDX):
        # Recursively index into the most apical leaf
        while self.data[IDX].apical is False:
            self.rmbranch(self.data[IDX].children[0])
        
        # Delete leaf
        self.rmbranch(IDX)

        self.saved=False

