from abaqusGui import *
from abaqusConstants import ALL
import osutils, os

##########################################################  
class StructuralDir_plugin(AFXForm):
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        
        self.radioButtonGroups = {}
        
        self.cmd = AFXGuiCommand(mode=self, method='StructuralFunc',objectName='Kernel_Function', registerQuery=False)
        pickedDefault = ''
        self.jobnameKw = AFXStringKeyword(self.cmd, 'jobname', True,'')


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):
        
        import StructuralDirDB
        return StructuralDirDB.StructuralDirDB(self)

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
      
toolset = getAFXApp().getAFXMainWindow().getPluginToolset()       
      
toolset.registerGuiMenuButton(buttonText='ATC|2.Structural analysis',
        object=StructuralDir_plugin(toolset),
        messageId=AFXMode.ID_ACTIVATE,
        icon=None,
        kernelInitString='',
        applicableModules=ALL,
        version='N/A',
        author='N/A',
        description='N/A',
        helpUrl='N/A',
        )