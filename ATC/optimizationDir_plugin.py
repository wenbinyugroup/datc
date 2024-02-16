from abaqusGui import *
from abaqusConstants import ALL
import osutils, os
import globalVar

###########################################################################
# Class definition
###########################################################################

class OptimizationDir_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='Optimization', objectName='Kernel_Function', registerQuery=False)
        pickedDefault = ''
        self.maxevalKw = AFXIntKeyword(self.cmd, 'maxeval', True,10000)
        self.popsizeKw = AFXIntKeyword(self.cmd, 'popsize', True,100)
        self.seedKw = AFXIntKeyword(self.cmd, 'seed', True,1027)
        self.printpopKw = AFXStringKeyword(self.cmd, 'printpop', True,'true')#bool
        self.descriptorKw = AFXStringKeyword(self.cmd, 'descriptor', True, 'u1')
        self.senseKw = AFXStringKeyword(self.cmd, 'sense', True, 'min')
        self.ineq_descriptorKw = AFXStringKeyword(self.cmd, 'ineq_descriptor', True, '')
        self.upperboundKw = AFXFloatKeyword(self.cmd, 'upperbound', True
                                            )

        # iv = globalVar.get_myinitialvalues()
        # self.UKw = AFXTupleKeyword(self.cmd, 'U', True, len(iv))
        # self.LKw = AFXTupleKeyword(self.cmd, 'L', True, len(iv))
        self.keyword19Kw = AFXStringKeyword(self.cmd, 'keyword19', True)
        self.jobnameKw = AFXStringKeyword(self.cmd, 'jobname', True, '')
        self.nodesetKw = AFXStringKeyword(self.cmd, 'nodeset', True, '')

        self.tablecoeffKw = AFXTableKeyword(self.cmd, 'tablecoeff', True)
        self.tablecoeffKw.setColumnType(0, AFXTABLE_TYPE_STRING)
        self.tablecoeffKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getFirstDialog(self):

        import optimizationDirDB
        return optimizationDirDB.OptimizationDirDB(self)

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
globalVar.my_init_bounds()
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(buttonText='ATC|5.Optimization',
        object=OptimizationDir_plugin(toolset),
        messageId=AFXMode.ID_ACTIVATE,
        icon=None,
        kernelInitString='',
        applicableModules=ALL,
        version='N/A',
        author='N/A',
        description='N/A',
        helpUrl='N/A')
