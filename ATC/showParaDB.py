from abaqusConstants import *
from abaqusGui import *
from globalPara_plugin import GlobalPara_plugin
from kernelAccess import mdb, session
import os
import globalVar

class ShowParaDB(AFXDataDialog):

    def __init__(self, form):
        self.form = form
        AFXDataDialog.__init__(self, form, 'Selected variables ', self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
        
        self.eqs = globalVar.get_myeqs()
        self.lid = globalVar.get_mylid()

        dict = globalVar.get_myfun()


        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, ShowParaDB.onCmdDone)

        VFrame_1 = FXVerticalFrame(p=self, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)

        GroupBox_1 = FXGroupBox(p=VFrame_1, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        VFrame_2 = FXVerticalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        if len(globalVar.get_mylaminamat()) != 0:
            l = FXLabel(p=VFrame_2, text='Selected lamina material:', opts=JUSTIFY_LEFT|FONT_BOLD)
        for i in globalVar.get_mylaminamat():
            l = FXLabel(p=VFrame_2, text=str(i) + " ", opts=JUSTIFY_LEFT)


        # ~~~~~~~~~~~~~~~~~~~
        GroupBox_3 = FXGroupBox(p=VFrame_1, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        VFrame_2 = FXVerticalFrame(p=GroupBox_3, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        if len(globalVar.get_myinclusionmat()) != 0:
            l = FXLabel(p=VFrame_2, text='Selected inclusion material: ', opts=JUSTIFY_LEFT|FONT_BOLD)
        for i in globalVar.get_myinclusionmat():
            l = FXLabel(p=VFrame_2, text=str(i) + " ", opts=JUSTIFY_LEFT)
        if len(globalVar.get_mymatrixmat()) != 0:
            l = FXLabel(p=VFrame_2, text='Selected matrix material: ', opts=JUSTIFY_LEFT|FONT_BOLD)
        for i in globalVar.get_mymatrixmat():
            l = FXLabel(p=VFrame_2, text=str(i) + ' ', opts=JUSTIFY_LEFT)
        # ~~~~~~~~~~~~~~~~~~~

        canBtn = self.getActionButton(self.ID_CLICKED_CANCEL)
        canBtn.setText('Done')
        canBtn.setTipText('Close the current window')
        globalVar.init_layup()
        
        # GroupBox_1 = FXGroupBox(p=self, text='', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        #
        # tmp = ''
        #
        # for i in range(len(self.eqs)):
        #     tmp = tmp +'Layer ' +str(self.lid[i]) + ': ' + str(self.eqs[i]) + '\n'
        # message =tmp

        # l = FXLabel(p=GroupBox_1, text=message, opts=JUSTIFY_LEFT)

    def onCmdDone(self, sender, sel, ptr):

        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):
        AFXDataDialog.hide(self)

    def deactivate(self):
        AFXForm.deactivate(self.form)
