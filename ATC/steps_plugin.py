from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import globalVar


###########################################################################
# Class definition
###########################################################################

class Steps_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='',
            objectName='', registerQuery=False)
        pickedDefault = ''
        self.name_abqKw = AFXStringKeyword(self.cmd, 'name_abq', True, 'buckling')
        # self.tabKw = AFXStringKeyword(self.cmd, 'tab', True, '')
        self.jobfileKw = AFXStringKeyword(self.cmd, 'jobfile', True, '')
        self.scriptKw = AFXStringKeyword(self.cmd, 'script', True, 'abq_get_result.py')
        self.keyword04Kw = AFXTableKeyword(self.cmd, 'keyword04', True)
        self.keyword04Kw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.stepresultKw = AFXStringKeyword(self.cmd, 'stepresult', True, 'abq_result.dat')
        self.name_pyKw = AFXStringKeyword(self.cmd, 'name_py', True, '')
        self.scriptpyKw = AFXStringKeyword(self.cmd, 'scriptpy', True, 'data_proc_funcs')
        self.funcnameKw = AFXStringKeyword(self.cmd, 'funcname', True, 'dakota_postpro')
        self.keyword09Kw = AFXTableKeyword(self.cmd, 'keyword09', True)
        self.keyword09Kw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.keyword09Kw.setColumnType(1, AFXTABLE_TYPE_FLOAT)

        self.othersKw = AFXTableKeyword(self.cmd, 'others', True)
        self.othersKw.setColumnType(0, AFXTABLE_TYPE_INT)
        self.othersKw.setColumnType(1, AFXTABLE_TYPE_INT)
        self.othersKw.setColumnType(2, AFXTABLE_TYPE_INT)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import stepsDB
        return stepsDB.StepsDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
globalVar.init_others()
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='ATC|3.Steps',
    object=Steps_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='',
    applicableModules=ALL,
    version='N/A',
    author='N/A',
    description='N/A',
    helpUrl='N/A'
)
