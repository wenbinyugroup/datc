import json

from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
from assignForm import AssignForm
from defineForm import DefineForm
from showForm import ShowForm
from advanceForm import AdvanceForm
from failure_plugin import Failure_plugin
from advanceThicknessForm import AdvanceThickness_plugin
import globalVar


thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FiberanglesDirDB(AFXDataDialog):
    [
        ID_ASSIGN,
        ID_ADVANCE,
        ID_ADVANCETHICKNESS,
        ID_FAILCR
    ] = range(AFXToolsetGui.ID_LAST, AFXToolsetGui.ID_LAST + 4)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        AFXDataDialog.__init__(self, form, 'Define fiber angles', self.OK | self.APPLY, DIALOG_ACTIONS_SEPARATOR,
                               DECOR_RESIZE)

        self.form = form

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('Done')
        okBtn.setTipText('Okay Done')

        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Apply')
        applyBtn.setTipText('Save the current layer ID and defined fiber angle equation')
        applyBtn.place = LAYOUT_SIDE_BOTTOM | LAYOUT_SIDE_RIGHT

        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_APPLY, FiberanglesDirDB.onCmdApply)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK, FiberanglesDirDB.onCmdDone)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_ASSIGN, FiberanglesDirDB.onCmdAssign)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_ADVANCE, FiberanglesDirDB.onCmdAdvance)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_FAILCR, FiberanglesDirDB.onCmdFAILCR)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_ADVANCETHICKNESS, FiberanglesDirDB.onCmdAdvanceThickness)

        Show_new = getAFXApp().getAFXMainWindow().getPluginToolset()
        self.appendActionButton('Layup', ShowForm(Show_new), AFXMode.ID_ACTIVATE)

        DefineForm_new = getAFXApp().getAFXMainWindow().getPluginToolset()
        dfn = self.appendActionButton('Define', DefineForm(DefineForm_new), AFXMode.ID_ACTIVATE)
        dfn.setTipText("define the design variable values in fiber angle functions")

        agn = self.appendActionButton('Assign', self, self.ID_ASSIGN)
        agn.setTipText('"All predefined sets"\nSelect the one for the defined layup')
        canBtn = self.appendActionButton(self.CANCEL)
        canBtn.setTipText('Close the current window')

        VAligner_1 = AFXVerticalAligner(p=self, opts=0, x=1, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        HFrame_1 = FXHorizontalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Layer Name    ', opts=JUSTIFY_LEFT)
        l.setTipText("Layer Name/ID")
        l.setFont(getAFXFont(FONT_BOLD))
        AFXTextField(p=HFrame_1, ncols=50, labelText='', tgt=form.layer_idKw, sel=0)

        VFrame_1 = FXVerticalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        HFrame_4 = FXHorizontalFrame(p=VFrame_1, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=20, pb=0, opts=LAYOUT_FILL_X)
        l = FXLabel(p=HFrame_4, text='Equation  ', opts=JUSTIFY_LEFT)
        l.setTipText("Orientation angle | One-line expression | From pre-defined scripts")
        l.setFont(getAFXFont(FONT_BOLD))
        self.eq_textbox = AFXTextField(p=HFrame_4, ncols=33, labelText='', tgt=form.eqKw, sel=0, opts=LAYOUT_CENTER_Y)
        FXButton(p=HFrame_4, text='From Scripts', tgt=self, sel=self.ID_ADVANCE, opts=BUTTON_NORMAL | LAYOUT_CENTER_Y,
                 x=0, y=0, w=0, h=0, pl=12, pr=12, pt=4, pb=4)

        VFrame_1 = FXVerticalFrame(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=20, pb=0)
        HFrame_1 = FXHorizontalFrame(p=VFrame_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Thickness  ', opts=JUSTIFY_LEFT)
        l.setTipText("Thickness of ply")
        l.setFont(getAFXFont(FONT_BOLD))
        AFXTextField(p=HFrame_1, ncols=33, labelText='', tgt=form.thicknessKw, sel=0)


        FXButton(p=HFrame_1, text='Advanced', tgt=self, sel=self.ID_ADVANCETHICKNESS,
                 opts=BUTTON_NORMAL | JUSTIFY_LEFT, x=0, y=0, w=0, h=0, pl=12, pr=12, pt=4, pb=4)

        VAligner_4 = AFXVerticalAligner(p=VAligner_1, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=20, pb=0)
        HFrame_1 = FXHorizontalFrame(p=VAligner_4, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        l = FXLabel(p=HFrame_1, text='Material     ', opts=JUSTIFY_LEFT)
        l.setFont(getAFXFont(FONT_BOLD))
        l.setTipText("Material")
        ComboBox_2 = AFXComboBox(p=HFrame_1, ncols=30, nvis=2, text='', tgt=form.mat_nameKw, sel=0, opts=LAYOUT_FILL_X)
        ComboBox_2.setMaxVisible(5)
        FXButton(p=HFrame_1, text='Failure Criterion', tgt=self, sel=self.ID_FAILCR, opts=BUTTON_NORMAL | LAYOUT_CENTER_Y,
                 x=0, y=0, w=0, h=0, pl=12, pr=12, pt=4, pb=4)

        vpName = session.currentViewportName
        modelName = session.sessionState[vpName]['modelName']
        cm = mdb.models[modelName].materials
        # if "lamina" not in cm.keys():
        #     ComboBox_2.appendItem(text="lamina")

        for i in cm.keys():
            ComboBox_2.appendItem(text=i)

        GroupBox_3 = FXGroupBox(p=self, text='Note', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        l = FXLabel(p=GroupBox_3, text='1. Use x, y, z to define the spatial coordinates', opts=JUSTIFY_LEFT)
        l = FXLabel(p=GroupBox_3, text='2. Use v1, v2, v3,...  to define design variables in Equation', opts=JUSTIFY_LEFT)
        l = FXLabel(p=GroupBox_3, text='3. Use From Scripts for fiber paths from external python scripts',
                    opts=JUSTIFY_LEFT)
        self.eqs = globalVar.get_myeqs()
        self.lid = globalVar.get_mylid()
        self.thickness = globalVar.get_mythickness()
        self.initvalue = globalVar.get_myinitialvalues()

        globalVar.flag0()

    def onCmdApply(self, sender, sel, ptr):

        if globalVar.get_plies() == "1":
            addlayer = globalVar.Layer(str(self.form.layer_idKw.getValue()), str(self.form.eqKw.getValue()), float(self.form.thicknessKw.getValue()), str(self.form.mat_nameKw.getValue())).defineFiberAngles()
        else:
            addlayer = globalVar.Layer(str(self.form.layer_idKw.getValue()), str(self.form.eqKw.getValue()), float(self.form.thicknessKw.getValue()), str(self.form.mat_nameKw.getValue())).defineFiberAngles(plies=globalVar.get_plies())

        self.eq_textbox.enable()

        a = self.form.layer_idKw.getValue()

        globalVar.add_to_material(self.form.mat_nameKw.getValue())
        globalVar.add_thickness(self.form.thicknessKw.getValue())

        globalVar.add_to(a, self.form.eqKw.getValue())

        def is_num(s):
            try:
                float(s)
            except ValueError:
                return False
            else:
                return True

        if globalVar.get_Switch() == 0:
            globalVar.flag1()
            if is_num(self.form.eqKw.getValue()):
                globalVar.flag0()

        if globalVar.get_Switch() == 1:  # advance done
            globalVar.flag2()

        if globalVar.get_flag() == 0:
            globalVar.add_to_choicelist(0)

        if globalVar.get_flag() == 1: # expression
            globalVar.add_to_choicelist(1)

        globalVar.switch0()
        # for j in self.eqs:
        #     s = list(j)
        #     for i in range(len(s)):
        #         if s[i] == 'v':
        #             globalVar.add_myinitialvalues(s[i + 1])

        # try:
        globalVar.func_layer_dict(self.form.layer_idKw.getValue(), self.form.eqKw.getValue(), self.form.thicknessKw.getValue(), self.form.mat_nameKw.getValue())
        # except :
        #     pass

        globalVar.flag0()
        globalVar.switch0()
        self.form.layer_idKw.setValue("")
        return True

    def onCmdAssign(self, sender, sel, ptr):
        assignForm_new = getAFXApp().getAFXMainWindow().getPluginToolset()
        agn = AssignForm(assignForm_new)
        AssignForm.activate(agn)
        return 1

    def onCmdAdvance(self, sender, sel, ptr):
        self.eq_textbox.disable()
        advanceForm_new = getAFXApp().getAFXMainWindow().getPluginToolset()
        adv = AdvanceForm(advanceForm_new)
        AdvanceForm.activate(adv)
        # a = self.form.layer_idKw.getValue()
        # if globalVar.get_flag()==1:
        #     if a > 0:
        #         if a in globalVar.get_mylid():
        # #replace
        #             self.eqs[a-1] = (self.form.eqKw.getValue())
        #             self.lid[a-1] = a
        #             self.form.layer_idKw.setValue(self.form.layer_idKw.getValue() + 1)
        #         else:
        #             globalVar.add_to(a, self.form.eqKw.getValue())
        #             self.form.layer_idKw.setValue(self.form.layer_idKw.getValue() + 1)
        #     else:
        #         mainWindow=getAFXApp().getAFXMainWindow()
        #         showAFXErrorDialog(owner=mainWindow, message='Enter positive layer ID.')
        return 1

    def onCmdFAILCR(self, sender, sel, ptr):

        Form_new = getAFXApp().getAFXMainWindow().getPluginToolset()
        failcr = Failure_plugin(Form_new)
        Failure_plugin.activate(failcr)
        return 1

    def onCmdAdvanceThickness(self, sender, sel, ptr):

        Advancethickness_new = getAFXApp().getAFXMainWindow().getPluginToolset()
        myParams = {
            'name': self.form.layer_idKw.getValue()

        }
        advanceThickness_ = AdvanceThickness_plugin(Advancethickness_new, myParams)
        AdvanceThickness_plugin.activate(advanceThickness_)

        return 1

    def onCmdDone(self, sender, sel, ptr):

        # f = open("onCmdDone.txt", "w")
        # f.write(json.dumps(globalVar.Layer().get_defineFiberAngles()) + '\n')
        # f.write(json.dumps((globalVar.get_mylayup())) + '\n')
        # f.close()

        if len(globalVar.get_mylayup()) == 0:
            raise ValueError('Layup is empty')


        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):
        AFXDataDialog.hide(self)

    def deactivate(self):
        AFXForm.deactivate(self.form)
