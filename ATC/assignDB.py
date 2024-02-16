from abaqusGui import *
from abaqusConstants import *
from kernelAccess import mdb, session
import os
# from globalVar import *
import globalVar
globalVar.init_elements()

class AssignDB(AFXDataDialog):
    def __init__(self,form):
    
        AFXDataDialog.__init__(self, form, 'Assign', self.OK |self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        
        self.form=form
        
        doneBtn = self.getActionButton(self.ID_CLICKED_OK)
        doneBtn.setText('Done')
        doneBtn.place=LAYOUT_SIDE_BOTTOM|LAYOUT_SIDE_RIGHT 
        
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK,AssignDB.onCmdDone)

        GroupBox_1 = FXGroupBox(p=self, text='Assign ATC region:', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        
        va=AFXVerticalAligner(self)
 
        vpName = session.currentViewportName
        modelName = session.sessionState[vpName]['modelName']
        cm=mdb.models[modelName].rootAssembly
        inss=mdb.models[modelName].rootAssembly.instances
        num_of_sets=len(cm.sets)
        setnames=inss[inss.keys()[0]].sets.keys()         #keys=['key1','key 2']
        setvalues=inss[inss.keys()[0]].sets.values()       #values=[mdb.models['Model-1'].parts['Part-1'].sets['VSC'], mdb.models['Model-1'].parts['Part-1'].sets['Set-2']]

        list_keys=list(setnames)            #listed 
            
        listVf = FXVerticalFrame(p=GroupBox_1, opts=FRAME_SUNKEN|FRAME_THICK, x=0, y=0, w=0, h=0,pl=0, pr=0, pt=0, pb=0)

        listVf.setSelector(99)
        List_1 = AFXList(p=listVf, nvis=5, tgt=form.selectedSetKw, sel=0, opts=HSCROLLING_OFF|LIST_SINGLESELECT|FRAME_GROOVE|LAYOUT_FILL_X)
        
        for i in list_keys:
            List_1.appendItem(text=i)   
            
            
        
    def onCmdDone(self, sender, sel, ptr):    
        selectedSet=self.form.selectedSetKw.getValue()
        
        vpName = session.currentViewportName
        modelName = session.sessionState[vpName]['modelName']
        cm=mdb.models[modelName].rootAssembly
        inss=mdb.models[modelName].rootAssembly.instances
        
        num_of_sets=len(cm.sets)
        
        no_of_elem=len(inss[inss.keys()[0]].sets[selectedSet].elements)        #in set i
        
        for j in range(0,no_of_elem):
            labelNumber=inss[inss.keys()[0]].sets[selectedSet].elements[j].label
            globalVar.add_to_elements(labelNumber)

        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)


    def hide(self):

        AFXDataDialog.hide(self)

    def deactivate(self):

        AFXForm.deactivate(self.form)


