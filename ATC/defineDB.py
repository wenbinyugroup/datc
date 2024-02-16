from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
import globalVar

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


class DefineDB(AFXDataDialog):

    def __init__(self, form):

        self.form = form
        AFXDataDialog.__init__(self, form, '', self.OK, DIALOG_ACTIONS_SEPARATOR)

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Done')

        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, DefineDB.onCmdDone)
        self.appendActionButton(self.CANCEL)
        VAligner_1 = AFXVerticalAligner(p=self, opts=0, x=5, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)

        GroupBox_1 = FXGroupBox(p=self, text='Define variables', opts=LAYOUT_FILL_X)
        self.iv = globalVar.get_myinitialvalues()

        for i in range(1, len(self.iv)):
            AFXTextField(p=GroupBox_1, ncols=5, labelText='v%s' % self.iv[i], tgt=form.viKw, sel=i, opts=LAYOUT_FILL_X)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # tab1
        TabBook_1 = FXTabBook(p=GroupBox_1, tgt=None, sel=0,
                              opts=TABBOOK_NORMAL,
                              x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                              pt=DEFAULT_SPACING, pb=DEFAULT_SPACING)
        tabItem = FXTabItem(p=TabBook_1, text='Fiber path', ic=None, opts=TAB_TOP_NORMAL,
                            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        TabItem_1 = FXVerticalFrame(p=TabBook_1,
                                    opts=FRAME_RAISED | FRAME_THICK | LAYOUT_FILL_X,
                                    x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                                    pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        vf = FXVerticalFrame(TabItem_1, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X,
                             0, 0, 0, 0, 0, 0, 0, 0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)

        tablecoeff = AFXTable(vf, 6, 4, 100, 4, form.tablecoeffKw, 5, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        tablecoeff.setLeadingRows(1)
        tablecoeff.setPopupOptions(
            AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW | AFXTable.POPUP_CLEAR_CONTENTS | AFXTable.POPUP_READ_FROM_FILE | AFXTable.POPUP_WRITE_TO_FILE)
        tablecoeff.setLeadingColumns(1)
        tablecoeff.setColumnWidth(1, 40)
        tablecoeff.setColumnType(1, AFXTable.TEXT)
        tablecoeff.setColumnWidth(2, 50)
        tablecoeff.setColumnType(2, AFXTable.TEXT)
        tablecoeff.setColumnWidth(3, 45)
        tablecoeff.setColumnType(3, AFXTable.INT)

        tablecoeff.setLeadingRowLabels('Layer\tVariables\tValues')
        tablecoeff.setStretchableColumn(tablecoeff.getNumColumns() - 1)
        tablecoeff.showHorizontalGrid(True)
        tablecoeff.showVerticalGrid(True)
        self.tablecoeff = tablecoeff

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # tab 2
        tabItem = FXTabItem(p=TabBook_1, text='Plies', ic=None, opts=TAB_TOP_NORMAL,
                            x=0, y=0, w=0, h=0, pl=6, pr=6, pt=DEFAULT_PAD, pb=DEFAULT_PAD)

        TabItem_2 = FXVerticalFrame(p=TabBook_1,
                                    opts=FRAME_RAISED | FRAME_THICK | LAYOUT_FILL_X,
                                    x=0, y=0, w=0, h=0, pl=DEFAULT_SPACING, pr=DEFAULT_SPACING,
                                    pt=DEFAULT_SPACING, pb=DEFAULT_SPACING, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)

        vf = FXVerticalFrame(TabItem_2, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X, 0, 0, 0, 0, 0, 0, 0, 0)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        vf.setSelector(99)
        table = AFXTable(vf, 6, 4, 100, 4, form.pliesKw, 0, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        table.setPopupOptions(
            AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW)
        table.setLeadingRows(1)
        table.setLeadingColumns(1)
        table.setColumnWidth(1, 40)
        table.setColumnType(1, AFXTable.INT)
        table.setColumnWidth(2, 50)
        table.setColumnType(2, AFXTable.INT)
        table.setColumnWidth(3, 45)
        table.setColumnType(3, AFXTable.INT)

        table.setLeadingRowLabels('Layer\tVariable\tValues')
        table.setStretchableColumn(table.getNumColumns() - 1)
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)
        self.table = table

    def onCmdDone(self, sender, sel, ptr):
    
        table_IV = []
        table_thickEQN = []
        
        try:
            globalVar.add_coeff(self.form.viKw.getValues())
        except:
            pass
            
        try:
            for i in range(1, self.tablecoeff.getNumRows()):
                table_IV.append([self.tablecoeff.getItemText(i, 1), self.tablecoeff.getItemText(i, 2), int(self.tablecoeff.getItemText(i, 3))])
        except:
            pass
            
        try:
            for i in range(1, self.table.getNumRows()):
                table_thickEQN.append([self.table.getItemText(i, 1), self.table.getItemText(i, 2), int(self.table.getItemText(i, 3))])
        except:
            pass
            
        globalVar.IV_designVar(table_IV)
        globalVar.IV_thickEQN(table_thickEQN)
            
        
            
        # # write design variables and its initial values
        # f = open("DesignVariable_ply.txt", "w")
        # f.write(str(table_IV) + '\n')
        # f.close()
        
        # # write design variables and its initial values
        # f = open("DesignVariable_fp.txt", "w")
        # f.write(str(table_thickEQN) + '\n')
        # f.close()
        

        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):
        AFXDataDialog.hide(self)

    def deactivate(self):
        AFXForm.deactivate(self.form)
