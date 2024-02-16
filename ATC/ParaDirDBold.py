from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os
import globalVar
from advanceParaForm import AdvanceParaForm

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

###########################################################################
# Class definition
###########################################################################

class ParaDirDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #
        self.form=form
        AFXDataDialog.__init__(self, form, 'Parametric study',self.OK, DIALOG_ACTIONS_SEPARATOR)
        
        self.eqs=globalVar.get_myeqs()

        doneBtn = self.getActionButton(self.ID_CLICKED_OK)
        doneBtn.setText('Done')
        doneBtn.place=LAYOUT_SIDE_BOTTOM|LAYOUT_SIDE_RIGHT
        # advanceParaForm_new = getAFXApp().getAFXMainWindow().getPluginToolset()
        
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_OK,ParaDirDB.onCmdDone)
        # self.appendActionButton('Advanced', AdvanceParaForm(advanceParaForm_new), AFXMode.ID_ACTIVATE)
        self.appendActionButton(self.CANCEL)

        # for i in range(1,len(self.iv)):
        #     GroupBox_1 = FXGroupBox(p=self, text='Variable v%s'%self.iv[i], opts=FRAME_GROOVE|LAYOUT_FILL_X)
        #     HFrame_1 = FXHorizontalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,pl=0, pr=0, pt=0, pb=0)
        #     AFXTextField(p=HFrame_1, ncols=12, labelText='L', tgt=form.LKw, sel=i)
        #     AFXTextField(p=HFrame_1, ncols=12, labelText='U', tgt=form.UKw, sel=i)
        #     AFXTextField(p=HFrame_1, ncols=12, labelText='P', tgt=form.PKw, sel=i)
        VAligner_1 = AFXVerticalAligner(p=self, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=5)
        vf = FXVerticalFrame(VAligner_1, FRAME_SUNKEN | FRAME_THICK | LAYOUT_FILL_X, 0, 0, 0, 0, 5, 5, 0, 0)

        vf.setSelector(99)
        # n = len(globalVar.get_mychoicelist())+1
        tablecoeff = AFXTable(vf, 5, 4, 2, 4, form.tablecoeffKw, 5, AFXTABLE_EDITABLE | LAYOUT_FILL_X)
        tablecoeff.setPopupOptions(
            AFXTable.POPUP_CUT | AFXTable.POPUP_COPY | AFXTable.POPUP_PASTE | AFXTable.POPUP_INSERT_ROW | AFXTable.POPUP_DELETE_ROW | AFXTable.POPUP_CLEAR_CONTENTS | AFXTable.POPUP_READ_FROM_FILE | AFXTable.POPUP_WRITE_TO_FILE)
        tablecoeff.setLeadingRows(1)
        # tablecoeff.setColumnWidth(0, 50)

        tablecoeff.setColumnType(0, AFXTable.TEXT)
        tablecoeff.setColumnType(1, AFXTable.INT)
        tablecoeff.setColumnType(2, AFXTable.INT)
        tablecoeff.setColumnType(3, AFXTable.INT)

        tablecoeff.setLeadingRowLabels('Name \tLower Bound \tUpper Bound \tPartitions ')
        tablecoeff.setStretchableColumn(tablecoeff.getNumColumns() - 1)
        tablecoeff.showHorizontalGrid(True)
        tablecoeff.showVerticalGrid(True)
        self.tablecoeff = tablecoeff

        GroupBox_3 = FXGroupBox(p=self, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        HFrame_3 = FXHorizontalFrame(p=GroupBox_3, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, opts=LAYOUT_FILL_X)
        VAligner_4 = AFXVerticalAligner(p=HFrame_3, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0)
        ComboBox_2 = AFXComboBox(p=VAligner_4, ncols=12, nvis=2, text='Nodal Set  =  ', tgt=form.nodesetKw, sel=0, opts=LAYOUT_FILL_X)
        ComboBox_2.setMaxVisible(5)
        vpName = session.currentViewportName
        modelName = session.sessionState[vpName]['modelName']
        for i in mdb.models[modelName].rootAssembly.sets.keys():
            ComboBox_2.appendItem(text=i)

        # GroupBox_4 = FXGroupBox(p=self, text='', opts=FRAME_GROOVE | LAYOUT_FILL_X)
        # HFrame_4 = FXHorizontalFrame(p=GroupBox_4, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, opts=LAYOUT_FILL_X)
        # fileHandler = BbDBFileHandler(form, 'jobname', '*.inp')
        # fileTextHf = FXHorizontalFrame(p=HFrame_4, opts=0, x=0, y=0, w=0, h=0, pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # # Note: Set the selector to indicate that this widget should not be
        # #       colored differently from its parent when the 'Color layout managers'
        # #       button is checked in the RSG Dialog Builder dialog.
        # fileTextHf.setSelector(99)
        # AFXTextField(p=fileTextHf, ncols=30, labelText='Jobname  =  ', tgt=form.jobnameKw, sel=0, opts=AFXTEXTFIELD_STRING | LAYOUT_CENTER_Y)
        # FXButton(p=fileTextHf, text=' .inp ', tgt=fileHandler, sel=AFXMode.ID_ACTIVATE, opts=BUTTON_NORMAL | LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)

        GroupBox_4 = FXGroupBox(p=self, text='Note:', opts=FRAME_GROOVE| LAYOUT_FILL_X)
        l = FXLabel(p=GroupBox_4, text='L: Lower Bound            U: Upper Bound           P: Partitions', opts=JUSTIFY_LEFT)

    def onCmdDone(self, sender, sel, ptr):

        jobname = globalVar.get_myabq_job()[0]

        globalVar.add_to_mynodeset(self.form.nodesetKw.getValue())
        self.L=globalVar.get_myAdvL()
        self.U=globalVar.get_myAdvU()
        self.P=globalVar.get_myAdvP()
        self.ivname =globalVar.get_myAdvname()
        self.iv =globalVar.get_myinitialvalues()
        self.c=globalVar.get_coeff()
        self.nodeset = self.form.nodesetKw.getValue()

        with open(jobname) as b:
            lines = b.readlines()

        for i in range(0, len(lines)):
            if lines[i] == "*End Part\n":
                lines.insert(i, "*Include, input=shellsections.inp\n")
                break

        with open(jobname, "w") as b:
            b.writelines(lines)
        b.close()


        dict1 = globalVar.get_thisdict()
        choice1 = globalVar.get_mychoicelist()
        mat1=globalVar.get_mymaterial()
        mat=[]
        choice = []
        myeqlist = []
        eq=globalVar.get_myeqs()
        layup=globalVar.get_mylayuplist()
        mylist=[]
        lid1=globalVar.get_mylid()
        lid=[]
        for i in range(0, len(layup)):
            if layup[i] not in mylist:
                mylist.append(layup[i])
                myeqlist.append(eq[i])
                choice.append(choice1[i])
                mat.append(mat1[i])
                lid.append(lid1[i])
            else:
                if layup[i] in mylist:
                    y = mylist.index(str(layup[i]))
                    myeqlist.append(eq[y])
                    choice.append(choice1[y])
                    mat.append(mat1[y])
                    lid.append(lid1[y])

        for i in range(1, self.tablecoeff.getNumRows()):
            globalVar.add_to_advname(self.tablecoeff.getItemText(i, 0))
            globalVar.add_to_advL(self.tablecoeff.getItemText(i, 1))
            globalVar.add_to_advU(self.tablecoeff.getItemText(i, 2))
            globalVar.add_to_advP(self.tablecoeff.getItemText(i, 3))



        #  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        f = open("vs_design.json", "w")            # Write VS_DESIGN.JSON

        f.write('{\n' + '\t' * 1 + '"name": "ts_plate_thm_ps_md",\n')
        f.write('\t' * 1 + '"design": {\n')
        f.write('\t' * 2 + '"layup": {\n' + '\t' * 3 + '"name": "layup1",\n')
        f.write('\t' * 3 + '"symmetry": '+ str(globalVar.get_symmetry()) +',\n' + '\t' * 3 + '"layers": [\n')
        for i in range(0, len(choice)):
            f.write('\t' * 4 + '{\n' + '\t' * 5 + '"name": "')
            f.write(str(lid[i]) + '",\n')
            f.write('\t' * 5 + '"lamina": "')
            if choice[i] == 0:  # angle
                f.write(str(mat[i]) + '",\n')
                f.write('\t' * 5 + '"in-plane_orientation": ')
                mystring = myeqlist[i]
                mystring = mystring.replace('\n', '').replace('\r', '')
                f.write(mystring + '\n')
            elif choice[i] == 2:  # script
                f.write(str(mat[i]) + '",\n')
                f.write('\t' * 5 + '"in-plane_orientation": ')
                f.write('{\n' + '\t' * 6 + '"function": "script",\n')
                f.write('\t' * 6 + '"file_name": "')
                f.write(str(dict1["file"][0]))
                f.write('",\n')
                f.write('\t' * 6 + '"function_name": "')
                f.write(str(dict1["function"][0]))
                f.write('",\n')
                f.write('\t' * 6 + '"coefficients": [\n')
                for j in range(0, len(dict1["coeffname"][0])):#
                    f.write('\t' * 7 + '[' + str(dict1["coeffval"][0][j]) + ', "' + str(dict1["coeffname"][0][j]) + '"],\n')
                f.write('\t' * 7 + '"m": ')
                f.write(str(dict1["m"][0]) + '\n')
                f.write('\t' * 6 + '}\n')
                f.write('\t' * 5 + '}\n')
                dict1['file'].remove(dict1['file'][0])
                dict1['function'].remove(dict1['function'][0])
                dict1['transformation'].remove(dict1['transformation'][0])
                dict1['coeffval'].remove(dict1['coeffval'][0])
                dict1['coeffname'].remove(dict1['coeffname'][0])
                dict1['m'].remove(dict1['m'][0])

            elif choice[i] == 1:  # expression
                f.write(str(mat[i]) + '",\n')
                f.write('\t' * 5 + '"in-plane_orientation": {\n')
                f.write('\t' * 6 + '"function": "expression",\n')
                mystring = myeqlist[i]
                mystring = mystring.replace('\n', '').replace('\r', '')
                f.write('\t' * 6 + '"expression": "' + mystring + '",\n')
                f.write('\t' * 6 + '"coefficients": [\n')

                for j in range(0, len(self.c)):
                    f.write('\t' * 7 + '[{"_' + str(self.ivname[j]) + '": ')
                    f.write(str(self.c[j]) + '}, "v' + str(self.iv[j+1]) + '"]')
                    if j != len(self.c) - 1:
                        f.write(',\n')
                f.write('\n' + '\t' * 6 + ']\n')

                # number of plies
                # number_plies = len(globalVar.get_mylayup())
                number_plies = 1

                f.write('\t' * 5 + '},\n')
                f.write('\t' * 5 + '"number_of_plies": ' + str(number_plies) + '\n')

            if i != len(choice)-1:
                f.write('\t' * 4 + '},\n')
            else:
                f.write('\t' * 4 + '}\n')
        f.write('\t' * 3 + ']\n')
        f.write('\t' * 2 + '},\n')
        f.write('\t' * 2 + '"materials": {\n')
        f.write('\t' * 3 + '"' + globalVar.get_mymaterial()[0] + '": {\n' + '\t' * 4 + '"type": "engineering",\n')
        f.write('\t' * 4 + '"density": 1.0,\n')
        f.write('\t' * 4 + '"elastic": ')

        vpName = session.currentViewportName
        modelName = session.sessionState[vpName]['modelName']
        cm = mdb.models[modelName].materials
        mat = globalVar.get_mymaterial()[0]
        t = []
        for i in cm[mat].elastic.table:
            for j in range(0, len(i)):
                t.append(i[j])
        temp = t[3:6]
        t[3:6] = t[6:9]
        t[6:9] = temp
        f.write(str(t) + ',\n')

        f.write('\t' * 4 + '"specific_heat": 0,\n')

        cte = [] # Coefficient of Thermal Expansion
        for i in cm[mat].expansion.table:
            for j in range(0, len(i)):
                cte.append(i[j])

        f.write('\t' * 4 + '"cte": ' + str(cte) + ',\n')
        f.write('\t' * 4 + '"thickness": ')
        f.write(str(globalVar.get_mythickness()[0]))
        f.write('\n' + '\t' * 3 + '}\n' + '\t' * 2 + '}\n' + '\t' * 1 + '},\n')
        f.write('\t' * 1 + '"model": {\n' + '\t' * 2 + '"structure": {\n' + '\t'*3+'"dimension": 2,\n')
        f.write('\t' * 3 + '"input_file": "')
        a = globalVar.get_myabq_job()[0]
        blocks = a.split('/')
        for i in blocks:
            if '.inp' in i:
                f.write(str(i) + '",\n')
        f.write('\t' * 3 + '"section_prop_file": "shellsections.inp",\n')
        f.write('\t' * 3 + '"solver": "abaqus"\n')
        f.write('\t' * 2 + '},\n')
        f.write('\t' * 2 + '"sg": {\n')
        f.write('\t' * 3 + '"mesh_size": 0,\n')              #
        f.write('\t' * 3 + '"solver": "SwiftComp",\n')
        f.write('\t' * 3 + '"version": "2.2",\n')
        f.write('\t' * 3 + '"physics": "thermoelastic",\n')
        f.write('\t' * 3 + '"print_stdout": false\n' + '\t' * 2 + '}\n' + '\t' * 1 + '},\n\n\n')

        # analysis
        f.write('\t' * 1 + '"analysis": {\n')
        f.write('\t' * 2 + '"steps": [\n')
        f.write('\t' * 3 + '{\n')
        f.write('\t' * 4 + '"name": "generate model input",\n')
        f.write('\t' * 4 + '"class": "general",\n')
        f.write('\t' * 4 + '"function": "genModelInput",\n')
        f.write('\t' * 4 + '"kwargs": {\n')
        f.write('\t' * 5 + '"tol": 1e-6\n')
        f.write('\t' * 4 + '}\n')
        f.write('\t' * 3 + '},\n\n')
        f.write('\t' * 3 + '{\n')
        # f.write('\t' * 4 + '"activate": true,\n')
        f.write('\t' * 4 + '"name": "')
        f.write(str(globalVar.get_myabq_name()[0]) + '",\n')
        f.write('\t' * 4 + '"class": "abaqus",\n')
        f.write('\t' * 4 + '"job_file": "')
        a = globalVar.get_myabq_job()[0]
        # a = str(globalVar.get_myabq_job()[0])
        blocks = a.split('/')
        for i in blocks:
            if '.inp' in i:
                f.write(str(i) + '",\n')
                jobname=i
        # f.write( + '",\n')
        f.write('\t' * 4 + '"args": [\n' + '\t' * 5 + '"interactive"\n' + '\t' * 4 + '],\n')
        f.write('\t' * 4 + '"post_process": [\n')
        f.write('\t' * 5 + '{\n')
        f.write('\t' * 6 + '"script": "')
        f.write(str(globalVar.get_myabq_script()[0]) + '",\n')
        f.write('\t' * 6 + '"args": [\n')
        for i in range(0, len(globalVar.get_myabq_arg())):
            if i != len(globalVar.get_myabq_arg()) - 1:
                f.write('\t' * 7 + '"' + str(globalVar.get_myabq_arg()[i]) + '",\n')
            else:
                f.write('\t' * 7 + '"' + str(globalVar.get_myabq_arg()[i]) + '"\n')
        f.write('\t' * 6 + ']\n')
        f.write('\t' * 5 + '}\n')
        f.write('\t' * 4 + '],\n')
        f.write('\t' * 4 + '"step_result_file": "')
        f.write(str(globalVar.get_myabq_step_result()[0]) + '"\n')
        f.write('\t' * 3 + '}\n')
        f.write('\t' * 2 + ']\n')
        f.write('\t' * 1 + '},\n\n\n')

        # dakota
        f.write('\t'*1+'"dakota": {\n'+'\t'*2+'"method": {\n'+'\t'*3+'"output": "normal",\n')
        f.write('\t'*3+'"multidim_parameter_study": {\n')
        f.write('\t'*4+'"partitions": [')       #[18,18]
        for i in range(0, len(globalVar.get_myAdvP())):
            if i != len(globalVar.get_myAdvP())-1:
                f.write(str(globalVar.get_myAdvP()[i]+', '))
            else:
                f.write(str(globalVar.get_myAdvP()[i]))
        f.write(']\n')
        f.write('\t' * 3 + '}\n' + '\t' * 2 + '},\n')
        f.write('\t' * 2 + '"variables": {\n')
        f.write('\t' * 3 + '"list": [\n')

        for i in range(0, len(globalVar.get_myAdvL())):
            # f.write('\t' * 3 + '"'+ str(globalVar.get_myAdvname()[i]))
            f.write('\t' * 4 + '{\n')
            f.write('\t' * 5 + '"name": "_' + str(globalVar.get_myAdvname()[i]) + '",\n')
            f.write('\t' * 5 + '"type": "continuous",\n')
            f.write('\t' * 5 + '"bounds": [')
            f.write(str(globalVar.get_myAdvL()[i]) + ',' + str(globalVar.get_myAdvU()[i]))
            if i != len(self.L)-1:
                f.write(']\n'+'\t'*4+'},\n')
            else:
                f.write(']\n'+'\t'*4+'}\n')
        f.write('\t'*3+']\n')
        f.write('\t'*2+'},\n')
        #interface
        f.write('\t' * 2 + '"interface": {\n')
        # f.write('\t' * 3 + '"analysis_driver": "python interface.py vs_cyl_bck_design.json",\n')
        f.write('\t' * 3 + '"fork": {\n')
        f.write('\t' * 4 + '"parameters_file": "params.in",\n')
        f.write('\t' * 4 + '"results_file": "results.out",\n')
        f.write('\t' * 4 + '"file_save": true,\n')
        f.write('\t' * 4 + '"work_directory": {\n')
        f.write('\t' * 5 + '"named": "evals/eval",\n')
        f.write('\t' * 5 + '"directory_tag": true,\n')
        f.write('\t' * 5 + '"directory_save": true\n')
        f.write('\t' * 4 + '}\n')
        f.write('\t' * 3 + '},\n')
        f.write('\t' * 3 + '"required_files": [\n')
        # f.write('\t' * 4 + '"vs_cyl_bck_design.json",\n')
        f.write('\t' * 4 + '"model/*"\n')
        # f.write('\t' * 4 + '"scripts/*"\n')
        f.write('\t' * 3 + '],\n')
        f.write('\t' * 3 + '"_asynchronous": {\n')
        f.write('\t' * 4 + '"evaluation_concurrency": 8\n')
        f.write('\t' * 3 + '}\n')
        f.write('\t' * 2 + '},\n\n\n')


        # responses
        f.write('\t' * 2 + '"responses": {\n')
        f.write('\t' * 3 + '"response_functions": [\n')
        f.write('\t' * 4 + '{\n')
        f.write('\t' * 5 + '"descriptor": "eig1"\n')
        f.write('\t' * 4 + '},\n')
        f.write('\t' * 4 + '{\n')
        f.write('\t' * 5 + '"descriptor": "eig2"\n')
        f.write('\t' * 4 + '},\n')
        f.write('\t' * 4 + '{\n')
        f.write('\t' * 5 + '"descriptor": "eig3"\n')
        f.write('\t' * 4 + '},\n')
        f.write('\t' * 4 + '{\n')
        f.write('\t' * 5 + '"descriptor": "eig4"\n')
        f.write('\t' * 4 + '},\n')
        f.write('\t' * 4 + '{\n')
        f.write('\t' * 5 + '"descriptor": "eig5"\n')
        f.write('\t' * 4 + '}\n')
        f.write('\t' * 3 + ']\n')
        f.write('\t' * 2 + '}\n' + '\t' * 1 + '},\n\n')

        #setting
        f.write('\t'*1+'"settings": {\n')
        f.write('\t'*2+'"log_level_cmd": "info",\n')
        f.write('\t'*2+'"log_level_file": "debug",\n')
        f.write('\t'*2+'"log_file_name": "eval.log",\n')
        f.write('\t'*2+'"tolerance": 1e-2\n')
        f.write('\t' * 1 + '}\n')
        f.write('}\n')

        # f.write('\t'*2+'"env_path": {\n')
        # f.write('\t'*3+'"PATH": [\n')
        # f.write('\t'*4+'"C:\\\ProgramData\\\Anaconda3",\n')
        # f.write('\t'*4+'"C:\\\ProgramData\\\Anaconda3\\\Scripts",\n')
        # f.write('\t'*4+'"C:\\\ProgramData\\\Anaconda3\\\Library'+'\\\\bin"\n')
        # f.write('\t'*3+']\n')
        # f.write('\t'*2+'}\n')

        f.close()
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
        import shutil
        if os.path.exists(jobname):
            cwd = os.getcwd()
            src = cwd + '\\' + jobname
            dst = cwd + '\\model\\' + jobname
            shutil.copyfile(src, dst)

        sendCommand('Kernel_Function.ParaFunction()')
        AFXDataDialog.hide(self)
        AFXForm.deactivate(self.form)

    def hide(self):
        AFXDataDialog.hide(self)

    def deactivate(self):
        AFXForm.deactivate(self.form)






###########################################################################
# Class definition
###########################################################################

class BbDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.jobnameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, BbDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):

       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.jobnameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.inp')
       fileDb.create()
       fileDb.showModal()
#