from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import globalVar

###########################################################################
# Class definition
###########################################################################

class Failure_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='',
            objectName='', registerQuery=False)
        pickedDefault = ''
        self.xtKw = AFXFloatKeyword(self.cmd, 'xt', True,2.999e5)
        self.ytKw = AFXFloatKeyword(self.cmd, 'yt', True,1.925e4 )
        self.ztKw = AFXFloatKeyword(self.cmd, 'zt', True,1.925e4)
        self.xcKw = AFXFloatKeyword(self.cmd, 'xc', True,1.680e5)
        self.ycKw = AFXFloatKeyword(self.cmd, 'yc', True,2.898e4)
        self.zcKw = AFXFloatKeyword(self.cmd, 'zc', True,2.898e4)
        self.RKw = AFXFloatKeyword(self.cmd, 'R', True,1.688e4)
        self.TKw = AFXFloatKeyword(self.cmd, 'T', True,1.688e4)
        self.SKw = AFXFloatKeyword(self.cmd, 'S', True, 1.206e4)
        self.fcriteriaKw = AFXStringKeyword(self.cmd, 'fcriteria', True)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import failureDB
        return failureDB.FailureDB(self)

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
globalVar.switch_failure0()
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)
#
# toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
# toolset.registerGuiMenuButton(
#     buttonText='failure',
#     object=Failure_plugin(toolset),
#     messageId=AFXMode.ID_ACTIVATE,
#     icon=None,
#     kernelInitString='',
#     applicableModules=ALL,
#     version='N/A',
#     author='N/A',
#     description='N/A',
#     helpUrl='N/A'
# )
