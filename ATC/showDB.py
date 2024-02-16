from abaqusConstants import *
from abaqusGui import *
from globalPara_plugin import GlobalPara_plugin
from kernelAccess import mdb, session
import os
import globalVar

class ShowDB(AFXDataDialog):
    [
        ID_Para
    ] = range(AFXToolsetGui.ID_LAST, AFXToolsetGui.ID_LAST + 1)

    def __init__(self, form):
        self.form = form
        AFXDataDialog.__init__(self, form, 'Defined layup ', self.OK, DIALOG_ACTIONS_SEPARATOR)
        
        self.eqs = globalVar.get_myeqs()
        self.lid = globalVar.get_mylid()

        dict = globalVar.get_myfun()
        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Done')
        okBtn.setTipText('Submit Layup')

        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, ShowDB.onCmdDone)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_Para, ShowDB.onCmdParameter)

        gp = self.appendActionButton('Parameter', self, self.ID_Para)
        gp.setTipText('"Define"\nglobal parameters')

        GroupBox_1 = FXGroupBox(p=self, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X | LAYOUT_FILL_Y)
        VAligner_1 = AFXVerticalAligner(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        vf = FXVerticalFrame(VAligner_1, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X, 0, 0, 0, 0, 0, 0, 0, 0)
        n = len(globalVar.get_mylid())+1
        table = AFXTable(vf, n, 3, n, 3, form.layuptabKw, 4, LAYOUT_FILL_X)
        # table.setPopupOptions(
        #     AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW | AFXTable.POPUP_CLEAR_CONTENTS | AFXTable.POPUP_READ_FROM_FILE | AFXTable.POPUP_WRITE_TO_FILE)
        table.setPopupOptions(AFXTable.POPUP_COPY)
        table.setLeadingRows(1)
        table.setColumnWidth(0, 15)
        table.setColumnWidth(1, 80)
        table.setColumnWidth(2, 220)
        table.setColumnType(0, AFXTable.INT)
        table.setColumnType(1, AFXTable.TEXT)
        table.setLeadingRowLabels('\tName\tFiber Angle Expression')
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)
        for i in range(1, n):
            table.setItemValue(i, 0, str(i))
        j=0
        for i in range(1, n):
            table.setItemValue(i, 1, str(globalVar.get_mylid()[i-1]))

            if globalVar.get_mychoicelist()[i-1] == 1 or globalVar.get_mychoicelist()[i-1] == 0:
                table.setItemValue(i, 2, str(globalVar.get_myeqs()[i-1]))

            else:
                # table.setItemValue(i, 2, str("From Scripts"))

                table.setItemValue(i, 2, str(dict[j]))
                j=j+1
                # dict['function'].remove(dict['function'][0])

        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=AFXTEXTFIELD_STRING, x=0, y=0, w=0, h=0, pl=5, pr=0, pt=2, pb=0)
        l = FXLabel(p=HFrame_1, text='Layup      ', opts=JUSTIFY_LEFT)
        l.setTipText("Layup-[layer name 1/ layer name 2/...]")
        AFXTextField(p=HFrame_1, ncols=40, labelText='', tgt=form.layupKw, sel=0)

        canBtn = self.appendActionButton(self.CANCEL)
        canBtn.setTipText('Close the current window')
        # globalVar.init_layup()
        
        # GroupBox_1 = FXGroupBox(p=self, text='', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        #
        # tmp = ''
        #
        # for i in range(len(self.eqs)):
        #     tmp = tmp +'Layer ' +str(self.lid[i]) + ': ' + str(self.eqs[i]) + '\n'
        # message =tmp

        # l = FXLabel(p=GroupBox_1, text=message, opts=JUSTIFY_LEFT)

    def onCmdParameter(self, sender, sel, ptr):

        Form_new = getAFXApp().getAFXMainWindow().getPluginToolset()
        globalp = GlobalPara_plugin(Form_new)
        GlobalPara_plugin.activate(globalp)
        return 1

    def onCmdDone(self, sender, sel, ptr):

        layup_string = self.form.layupKw.getValue()
        symmetry = 0
        globalVar.symmetry0()
        if layup_string[-1].lower() == 's':
            symmetry = 1
            globalVar.symmetry1()
            globalVar.add_to_layup(layup_string[:-1])
        else:
            globalVar.add_to_layup(layup_string)

        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):
        AFXDataDialog.hide(self)

    def deactivate(self):
        AFXForm.deactivate(self.form)
