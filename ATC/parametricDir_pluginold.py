from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import globalVar
###########################################################################

class ParaDir_plugin(AFXForm):
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        
        self.radioButtonGroups = {}
        self.iv =globalVar.get_myinitialvalues()
        self.cmd = AFXGuiCommand(mode=self, method='ParaFunction',objectName='Kernel_Function', registerQuery=False)
        pickedDefault = ''
        # self.LKw=[]
        # self.UKw=[]
        # self.DKw=[]
        # self.UKw = AFXTupleKeyword(self.cmd, 'U', True,len(self.iv))
        # self.LKw = AFXTupleKeyword(self.cmd, 'L', True,len(self.iv))
        # self.PKw = AFXTupleKeyword(self.cmd, 'P', True,len(self.iv))
        self.tablecoeffKw = AFXTableKeyword(self.cmd, 'tablecoeff', True)
        self.tablecoeffKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.tablecoeffKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        # self.jobnameKw = AFXStringKeyword(self.cmd, 'jobname', True,'')
        self.nodesetKw = AFXStringKeyword(self.cmd, 'nodeset', True,'')

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import ParaDirDB
        return ParaDirDB.ParaDirDB(self)

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
globalVar.my_init_para()
globalVar.init_jobname()
globalVar.init_nodeset()
globalVar.advpara()
toolset = getAFXApp().getAFXMainWindow().getPluginToolset()       
toolset.registerGuiMenuButton(buttonText='ATC|5.Parametric study',
        object=ParaDir_plugin(toolset),
        messageId=AFXMode.ID_ACTIVATE,
        icon=None,
        kernelInitString='',
        applicableModules=ALL,
        version='N/A',
        author='N/A',
        description='N/A',
        helpUrl='N/A'
        )
