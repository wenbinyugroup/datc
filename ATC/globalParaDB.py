from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

import globalVar

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class GlobalParaDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #
        self.form = form
        AFXDataDialog.__init__(self, form, 'Global Parameters',
            self.OK|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Done')

        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, GlobalParaDB.onCmdDone)
            
        vf = FXVerticalFrame(self, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X, 0, 0, 0, 0, 0, 0, 0, 0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table = AFXTable(vf, 5, 3, 4, 3, form.keyword01Kw, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X)
        table.setPopupOptions(AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_PASTE|AFXTable.POPUP_INSERT_ROW|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS)
        table.setLeadingRows(1)
        table.setLeadingColumns(1)
        table.setColumnWidth(1, 80)
        table.setColumnType(1, AFXTable.TEXT)
        table.setColumnWidth(2, 120)
        table.setColumnType(2, AFXTable.FLOAT)
        table.setLeadingRowLabels('Name\tValue')
        table.setStretchableColumn( table.getNumColumns()-1 )
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)
        self.table=table

    def onCmdDone(self, sender, sel, ptr):

        for i in range(1,self.table.getNumRows()):
            globalVar.add_to_globalname(self.table.getItemText(i,1))
            globalVar.add_to_globalval(self.table.getItemText(i,2))
        globalVar.switch_globalpara1()
        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):
        AFXDataDialog.hide(self)

    def deactivate(self):
        AFXForm.deactivate(self.form)
