from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import globalVar

class FiberanglesDir_plugin(AFXForm):
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        AFXForm.__init__(self, owner)
        
        self.radioButtonGroups = {}
        
        self.cmd = AFXGuiCommand(mode=self, method='KernelFunction',objectName='Kernel_Function', registerQuery=False)
        self.layer_idKw = AFXStringKeyword(self.cmd, 'layer_id', True, defaultValue='l1')
        # self.eqKw = AFXStringKeyword(self.cmd, 'eq', True, '2*(v2-v1)*abs(x)/400+v1')
        self.eqKw = AFXStringKeyword(self.cmd, 'eq', True, '')
        self.mat_nameKw = AFXStringKeyword(self.cmd, 'mat_name', True, '')
        self.thicknessKw = AFXFloatKeyword(self.cmd, 'thickness', True, defaultValue=0.127)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import fiberanglesDirDB
        
        
        return fiberanglesDirDB.FiberanglesDirDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        
        return True
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

###########################################################################        
class VisualizationDir_plugin(AFXForm):
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        
        self.radioButtonGroups = {}
        
        self.cmd = AFXGuiCommand(mode=self, method='',objectName='', registerQuery=False)
        pickedDefault = ''
        self.k1Kw = AFXIntKeyword(self.cmd, 'k1', True)



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import VisualizationDirDB
        return VisualizationDirDB.VisualizationDirDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        
        return True
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

globalVar.my_init()                 #initialise L_ID AND EQS
globalVar.my_init_iv()
globalVar.my_init_material()
globalVar.init_choicelist()

globalVar.switch0()
globalVar.init_coeffname()
globalVar.init_coeffval()
globalVar.init_thisdict()
globalVar.init_fun()
globalVar.init_file()
globalVar.init_trans()
globalVar.init_failure()
globalVar.init_strength()

globalVar.init_abq_name()
globalVar.init_abq_job()
globalVar.init_abq_script()
globalVar.init_abq_step_result()
globalVar.init_abq_arg()

globalVar.init_py_name()
globalVar.init_py_script()
globalVar.init_py_func()
globalVar.init_py_arg_name()
globalVar.init_py_arg_val()

globalVar.init_symmetry()


menubar = getAFXApp().getAFXMainWindow().getMenubar()
toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
menu = getWidgetFromText(menubar, 'Plug-ins').getMenu()

dfa = toolset.registerGuiMenuButton(buttonText='ATC|1.Define fiber angles',
        object=FiberanglesDir_plugin(toolset),
        messageId=AFXMode.ID_ACTIVATE,
        icon=None,
        kernelInitString='import Kernel_Function',
        applicableModules=ALL,
        version='N/A',
        author='N/A',
        description='N/A',
        helpUrl='N/A')


# toolset.registerGuiMenuButton(buttonText='ATC|6.Visualization',
#         object=VisualizationDir_plugin(toolset),
#         messageId=AFXMode.ID_ACTIVATE,
#         icon=None,
#         kernelInitString='',
#         applicableModules=ALL,
#         version='N/A',
#         author='N/A',
#         description='N/A',
#         helpUrl='N/A')
