# -*- coding: utf-8 -*-

from abaqus import *
from abaqusConstants import *
# from sg2DSqrUF_V5 import *
# from sg2DHex_V5 import *
# from sg2DSqrInterface_V5 import *
# from sg2DHexInterface_V5 import *
from caeModules import *
# from yZview import *
# import utilities
# from utilities import *
import utilities_abq as uab
from textRepr import *
import regionToolset

from scGenInput import *
from scGen1DInput_aba import *
from UdetermineVolume import *
from UdetermineNSG import *
from userDataSG import *
from convert2sc import *
from createSCInputMain import *
import time
import os
from caeModules import *


# ==============================================================================
#
#   Main
#
# ==============================================================================

def create2DV5SG(profile, fiber_flag, vf_f, interface_flag, t_interface,
                 model_name, fiber_matname, matrix_matname, interface_matname,
                 mesh_size, elem_type, new_filename, analysis, model_source, abaqus_input,
                 macro_model, specific_model, bk, sk, cos, w, elem_flag, trans_flag,temp_flag,ap1,ap2,ap3,gen_input_only):


    if profile == 1:
        if t_interface == 0.0:
            p, pname = createSqrV5(model_name, fiber_flag, vf_f, fiber_matname,
                            matrix_matname, mesh_size, elem_type)
        elif t_interface != 0.0:
            p, pname = createSqrInterfaceV5(model_name, fiber_flag, vf_f, interface_flag,
                                     t_interface, fiber_matname, matrix_matname,
                                     interface_matname, mesh_size, elem_type)
    elif profile == 2:
        if t_interface == 0.0:
            p, pname = createHexV5(model_name, fiber_flag, vf_f, fiber_matname,
                            matrix_matname, mesh_size, elem_type)
        elif t_interface != 0.0:
            p,pname = createHexInterfaceV5(model_name, fiber_flag, vf_f, interface_flag,
                                     t_interface, fiber_matname, matrix_matname,
                                     interface_matname, mesh_size, elem_type)

    uab.setViewYZ(nsg=2, obj=p, clr='Material')
    part_name=pname
    homogenization(gen_input_only, model_source, macro_model, analysis, elem_flag, trans_flag, ap1, ap2, ap3, w, model_name, part_name, abaqus_input, new_filename, specific_model, bk=[[0.0, 0.0, 0.0]],sk=[[0.0, 0.0]], cos=[[1.0, 0.0]], temp_flag=0)
    return 1


# ==============================================================================
#
#   Square Unidirectional Fiber
#
# ==============================================================================

def createSqrV5(model_name, fiber_flag, vf_f, fiber_matname, matrix_matname, mesh_size, elem_type):
    # ---------------------------------------
    #### Define Parameters
    # --------------------------------------

    part2DName = 'sqrP2' + 'quater'
    part2DFullName = 'sqrP2'
    partsobj = mdb.models[model_name].parts
    print
    '#-------part_name  %s---------------------------' % part2DFullName

    # -------------------------------
    blockSize = 1.0
    quarterSize = 1.0 / 2.0 * blockSize

    if elem_type == 'Linear':
        elementType1 = S4
        elementType2 = S3
    elif elem_type == 'Quadratic':
        elementType1 = S8R
        elementType2 = STRI65

    if fiber_flag == 1:  # vf_f is volume fraction  of the fiber
        vof_fiber = vf_f
        fiberRadius = blockSize * sqrt(vof_fiber / pi)

    elif fiber_flag == 2:  # vf_f is radius of the fiber
        fiberRadius = vf_f
        vof_fiber = pi * fiberRadius ** 2 / blockSize ** 2

    if fiberRadius >= blockSize / 2.0:
        raise ValueError('The volume fraction of fiber is out of range. Please adjust the values.')

    print
    'blockSize: %s' % blockSize
    print
    '#---fiber------------------------'
    print
    'vof_fiber: %s' % vof_fiber
    print
    'fiberRadius: %s' % fiberRadius

    fiber_setname = 'Fiber_section'
    matrix_setname = 'Matrix_section'

    p = mdb.models[model_name].Part(name=part2DName, dimensionality=THREE_D,
                                    type=DEFORMABLE_BODY)

    datumPlaneYZ_id = p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0).id
    datumAxisZ_id = p.DatumAxisByPrincipalAxis(principalAxis=ZAXIS).id
    # ---------------------------------------------------
    YZworkPlaneTransform = (0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0)  # y-z plane
    #    YZviewVector = (1.0, 0.0, 0.0)
    #    YZcameraUpVector = (0.0, 0.0, 1.0)
    # --------------------------------------------------
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__',
                                                 sheetSize=200.0, transform=YZworkPlaneTransform)

    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    #    session.viewports['Viewport: 1'].view.setValues(session.views['Left'])

    p = mdb.models[model_name].parts[part2DName]
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.rectangle(point1=(0.0, 0.0), point2=(quarterSize, quarterSize))
    p = mdb.models[model_name].parts[part2DName]
    e1, d2 = p.edges, p.datums
    p.Shell(sketchPlane=d2[datumPlaneYZ_id], sketchUpEdge=d2[datumAxisZ_id], sketchPlaneSide=SIDE1,
            sketchOrientation=RIGHT, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']

    p = mdb.models[model_name].parts[part2DName]

    #    session.viewports['Viewport: 1'].view.setViewpoint(viewVector = (1.0, 0.0, 0.0), cameraUpVector = (0.0, 0.0, 1.0))
    #    session.viewports['Viewport: 1'].view.fitView()
    # -------------------------------------------------------------
    #    Define fiber on the shell
    # --------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    f, e, d = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f[0], sketchUpEdge=e[1],
                              sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__',
                                                 sheetSize=2.0, gridSpacing=0.02, transform=t)
    g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[model_name].parts[part2DName]
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, fiberRadius))
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    pickedFaces = f
    e1, d2 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e1[1], faces=pickedFaces, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']
    #    session.viewports['Viewport: 1'].view.setViewpoint(viewVector = (1.0, 0.0, 0.0), cameraUpVector = (0.0, 0.0, 1.0))
    #    session.viewports['Viewport: 1'].view.fitView()

    # Define Sections and assign them
    # --------------------------------------
    mdb.models[model_name].HomogeneousShellSection(name=fiber_setname, preIntegrate=OFF,
                                                   material=fiber_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize, thicknessField='',
                                                   idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)

    mdb.models[model_name].HomogeneousShellSection(name=matrix_setname, preIntegrate=OFF,
                                                   material=matrix_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize,
                                                   thicknessField='', idealization=NO_IDEALIZATION,
                                                   poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)

    # -------
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#2 ]',), )
    region = p.Set(faces=faces, name=fiber_setname)
    p = mdb.models[model_name].parts[part2DName]
    p.SectionAssignment(region=region, sectionName=fiber_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]',), )
    region = p.Set(faces=faces, name=matrix_setname)
    p = mdb.models[model_name].parts[part2DName]
    p.SectionAssignment(region=region, sectionName=matrix_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    # assign material direction
    # -----------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    region = p.sets[fiber_setname]
    orientation = None
    mdb.models[model_name].parts[part2DName].MaterialOrientation(region=region,
                                                                 orientationType=GLOBAL, axis=AXIS_1,
                                                                 additionalRotationType=ROTATION_NONE,
                                                                 localCsys=None, fieldName='')
    #: Specified material orientation has been assigned to the selected regions.
    p = mdb.models[model_name].parts[part2DName]
    region = p.sets[matrix_setname]
    orientation = None
    mdb.models[model_name].parts[part2DName].MaterialOrientation(region=region,
                                                                 orientationType=GLOBAL, axis=AXIS_1,
                                                                 additionalRotationType=ROTATION_NONE,
                                                                 localCsys=None, fieldName='')

    #    session.viewports['Viewport: 1'].setValues(displayedObject=p)

    # generate mesh on the quarter shell part
    # -----------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    p.seedPart(size=mesh_size, deviationFactor=0.1, minSizeFactor=0.1)
    elemType1 = mesh.ElemType(elemCode=elementType1, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=elementType2, elemLibrary=STANDARD)
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    pickedRegions = f.getSequenceFromMask(mask=('[#3 ]',), )
    p.setMeshControls(regions=pickedRegions, elemShape=QUAD, algorithm=MEDIAL_AXIS)
    pickedRegions = (faces,)

    faces = f.getSequenceFromMask(mask=('[#3 ]',), )
    pickedRegions = (faces,)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    p = mdb.models[model_name].parts[part2DName]
    p.generateMesh()
    # -------------------------

    # import the quarter Shell part in the Assembly
    # generate the full shell model by doing 2 reflect
    # -------------------------------------------------------
    a1 = mdb.models[model_name].rootAssembly
    p = mdb.models[model_name].parts[part2DName]
    a1.Instance(name=part2DName + '-1', part=p, dependent=ON)
    a1.Instance(name=part2DName + '-2', part=p, dependent=ON)

    a1 = mdb.models[model_name].rootAssembly
    a1.rotate(instanceList=(part2DName + '-2',), axisPoint=(0.0, 0.0, 0.0),
              axisDirection=(0.0, 10.0, 0.0), angle=180.0)

    a1 = mdb.models[model_name].rootAssembly
    a1.InstanceFromBooleanMerge(name=part2DName + 'half', instances=(a1.instances[part2DName + '-1'],
                                                                     a1.instances[part2DName + '-2'],),
                                mergeNodes=BOUNDARY_ONLY,
                                nodeMergingTolerance=0.0001 * mesh_size, domain=MESH, originalInstances=DELETE)

    p1 = mdb.models[model_name].parts[part2DName + 'half']

    a1 = mdb.models[model_name].rootAssembly
    p = mdb.models[model_name].parts[part2DName + 'half']
    a1.Instance(name=part2DName + 'half' + '-2', part=p, dependent=ON)
    a1 = mdb.models[model_name].rootAssembly
    a1.rotate(instanceList=(part2DName + 'half' + '-2',), axisPoint=(0.0, 0.0, 0.0),
              axisDirection=(10.0, 0.0, 0.0), angle=180.0)
    ##: The instance Part-3-2 was rotated by 180. degrees about the axis defined by the point 0., 0., 0. and the vector 10., 0., 0.

    a1 = mdb.models[model_name].rootAssembly
    a1.InstanceFromBooleanMerge(name=part2DFullName, instances=(a1.instances[part2DName + 'half' + '-1'],
                                                                a1.instances[part2DName + 'half' + '-2'],),
                                mergeNodes=BOUNDARY_ONLY,
                                nodeMergingTolerance=0.0001 * mesh_size, domain=MESH, originalInstances=DELETE)

    # make the final merged part (shell model) has the same shell element normal (make the element connectivity arranged in the anticlockwise direction)
    p = mdb.models[model_name].parts[part2DFullName]
    z1 = p.elements
    regions = regionToolset.Region(elements=z1)
    p.flipNormal(referenceRegion=z1[1], regions=regions)

    # delete the unwanted part and instances
    # a.deleteFeatures((part2DName+'-1', part2DName+'-2', part2DName+'half-1',  part2DName+'half-2', ))
    del mdb.models[model_name].parts[part2DName + 'half']
    del mdb.models[model_name].parts[part2DName]
    a = mdb.models[model_name].rootAssembly
    del a.features[part2DFullName + '-1']

    #    setYZview()
    p = mdb.models[model_name].parts[part2DFullName]
    #    session.viewports['Viewport: 1'].setValues(displayedObject = a)
    #    session.viewports['Viewport: 1'].view.setViewpoint(viewVector = (1.0, 0.0, 0.0), cameraUpVector = (0.0, 0.0, 1.0))
    #    session.viewports['Viewport: 1'].view.fitView()
    #    cmap=session.viewports['Viewport: 1'].colorMappings['Material']
    #    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    #    session.viewports['Viewport: 1'].disableMultipleColors()

    return p,part2DFullName


# ==============================================================================
#
#   Square Unidirectional Fiber with Interphase
#
# ==============================================================================

def createSqrInterfaceV5(model_name, fiber_flag, vf_f, interface_flag,
                         t_interface, fiber_matname, matrix_matname,
                         interface_matname, mesh_size, elem_type):
    # ---------------------------------------
    #### Define Parameters
    # --------------------------------------

    part2DName = 'sqrP3' + 'quater'
    part2DFullName = 'sqrP3'
    partsobj = mdb.models[model_name].parts

    fiber_setname = 'Fiber_section'
    matrix_setname = 'Matrix_section'
    interface_setname = 'Interphase_section'

    print
    '#-------part_name  %s---------------------------' % part2DFullName

    # -------------------------------
    blockSize = 1.
    quarterSize = 1.0 / 2.0 * blockSize

    if elem_type == 'Linear':
        elementType1 = S4
        elementType2 = S3
    elif elem_type == 'Quadratic':
        elementType1 = S8R
        elementType2 = STRI65

    if fiber_flag == 1:  # vf_f is volume fraction  of the fiber
        vof_fiber = vf_f
        fiberRadius = blockSize * sqrt(vof_fiber / pi)
    elif fiber_flag == 2:  # vf_f is radius of the fiber
        fiberRadius = vf_f
        vof_fiber = pi * fiberRadius ** 2 / blockSize ** 2

    try:
        if interface_flag == 1:  # t_interface is volume fraction of the interface
            vof_interface = t_interface
            interfaceRadius = blockSize * sqrt((vof_interface + vof_fiber) / pi)
            if interfaceRadius >= blockSize / 2.0:
                False
        elif interface_flag == 2:  # t_interface is thickness of the interface
            interfaceRadius = fiberRadius + t_interface
            vof_interface = pi * (interfaceRadius ** 2 - fiberRadius ** 2) / blockSize ** 2
            if interfaceRadius >= blockSize / 2.0:
                False
    except:
        raise ValueError('The volume fraction of fiber and interphase is out of range. Please adjust the values.')

    print
    'blockSize: %s' % blockSize

    print
    '#---fiber------------------------'
    print
    'vof_fiber: %s' % vof_fiber
    print
    'fiberRadius: %s' % fiberRadius

    p = mdb.models[model_name].Part(name=part2DName, dimensionality=THREE_D,
                                    type=DEFORMABLE_BODY)

    datumPlaneYZ_id = p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0).id
    datumAxisZ_id = p.DatumAxisByPrincipalAxis(principalAxis=ZAXIS).id
    # ---------------------------------------------------
    YZworkPlaneTransform = (0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0)  # y-z plane
    #    YZviewVector = (1.0, 0.0, 0.0)
    #    YZcameraUpVector = (0.0, 0.0, 1.0)
    # --------------------------------------------------
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__',
                                                 sheetSize=200.0, transform=YZworkPlaneTransform)

    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    #    session.viewports['Viewport: 1'].view.setValues(session.views['Left'])

    p = mdb.models[model_name].parts[part2DName]
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.rectangle(point1=(0.0, 0.0), point2=(quarterSize, quarterSize))
    p = mdb.models[model_name].parts[part2DName]
    e1, d2 = p.edges, p.datums
    p.Shell(sketchPlane=d2[datumPlaneYZ_id], sketchUpEdge=d2[datumAxisZ_id], sketchPlaneSide=SIDE1,
            sketchOrientation=RIGHT, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']

    p = mdb.models[model_name].parts[part2DName]

    #    session.viewports['Viewport: 1'].view.setViewpoint(viewVector = (1.0, 0.0, 0.0), cameraUpVector = (0.0, 0.0, 1.0))
    #    session.viewports['Viewport: 1'].view.fitView()
    # -------------------------------------------------------------
    #    Define fiber and interface on the shell
    # --------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    f, e, d = p.faces, p.edges, p.datums
    t = YZworkPlaneTransform
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__',
                                                 sheetSize=2.0, gridSpacing=0.02, transform=t)
    g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[model_name].parts[part2DName]
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, fiberRadius))
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, interfaceRadius))
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    pickedFaces = f
    e1, d2 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e1[1], faces=pickedFaces, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']
    #    session.viewports['Viewport: 1'].view.setViewpoint(viewVector = (1.0, 0.0, 0.0), cameraUpVector = (0.0, 0.0, 1.0))
    #    session.viewports['Viewport: 1'].view.fitView()

    # Define Sections and assign them
    # --------------------------------------
    mdb.models[model_name].HomogeneousShellSection(name=fiber_setname, preIntegrate=OFF,
                                                   material=fiber_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize, thicknessField='',
                                                   idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)

    mdb.models[model_name].HomogeneousShellSection(name=matrix_setname, preIntegrate=OFF,
                                                   material=matrix_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize,
                                                   thicknessField='', idealization=NO_IDEALIZATION,
                                                   poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)

    mdb.models[model_name].HomogeneousShellSection(name=interface_setname, preIntegrate=OFF,
                                                   material=interface_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize,
                                                   thicknessField='', idealization=NO_IDEALIZATION,
                                                   poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)

    # -------
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#4 ]',), )
    region = p.Set(faces=faces, name=fiber_setname)
    p = mdb.models[model_name].parts[part2DName]
    p.SectionAssignment(region=region, sectionName=fiber_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#2 ]',), )
    region = p.Set(faces=faces, name=interface_setname)
    p = mdb.models[model_name].parts[part2DName]
    p.SectionAssignment(region=region, sectionName=interface_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]',), )
    region = p.Set(faces=faces, name=matrix_setname)
    p = mdb.models[model_name].parts[part2DName]
    p.SectionAssignment(region=region, sectionName=matrix_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    # assign material direction
    # -----------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    region = p.sets[fiber_setname]
    orientation = None
    mdb.models[model_name].parts[part2DName].MaterialOrientation(region=region,
                                                                 orientationType=GLOBAL, axis=AXIS_1,
                                                                 additionalRotationType=ROTATION_NONE,
                                                                 localCsys=None, fieldName='')
    #: Specified material orientation has been assigned to the selected regions.
    p = mdb.models[model_name].parts[part2DName]
    region = p.sets[matrix_setname]
    orientation = None
    mdb.models[model_name].parts[part2DName].MaterialOrientation(region=region,
                                                                 orientationType=GLOBAL, axis=AXIS_1,
                                                                 additionalRotationType=ROTATION_NONE,
                                                                 localCsys=None, fieldName='')
    #: Specified material orientation has been assigned to the selected regions.
    p = mdb.models[model_name].parts[part2DName]
    region = p.sets[interface_setname]
    orientation = None
    mdb.models[model_name].parts[part2DName].MaterialOrientation(region=region,
                                                                 orientationType=GLOBAL, axis=AXIS_1,
                                                                 additionalRotationType=ROTATION_NONE,
                                                                 localCsys=None, fieldName='')
    #    session.viewports['Viewport: 1'].setValues(displayedObject=p)

    # generate mesh on the quarter shell part
    # -----------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    p.seedPart(size=mesh_size, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    pickedRegions = f.getSequenceFromMask(mask=('[#7 ]',), )
    p.setMeshControls(regions=pickedRegions, elemShape=QUAD, algorithm=MEDIAL_AXIS)

    elemType1 = mesh.ElemType(elemCode=elementType1, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=elementType2, elemLibrary=STANDARD)
    faces = f.getSequenceFromMask(mask=('[#7 ]',), )
    pickedRegions = (faces,)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    p = mdb.models[model_name].parts[part2DName]
    p.generateMesh()

    # import the quarter Shell part in the Assembly
    # generate the full shell model by doing 2 reflect
    # -------------------------------------------------------
    a1 = mdb.models[model_name].rootAssembly
    p = mdb.models[model_name].parts[part2DName]
    a1.Instance(name=part2DName + '-1', part=p, dependent=ON)
    a1.Instance(name=part2DName + '-2', part=p, dependent=ON)

    a1 = mdb.models[model_name].rootAssembly
    a1.rotate(instanceList=(part2DName + '-2',), axisPoint=(0.0, 0.0, 0.0),
              axisDirection=(0.0, 10.0, 0.0), angle=180.0)

    a1 = mdb.models[model_name].rootAssembly
    a1.InstanceFromBooleanMerge(name=part2DName + 'half', instances=(a1.instances[part2DName + '-1'],
                                                                     a1.instances[part2DName + '-2'],),
                                mergeNodes=BOUNDARY_ONLY,
                                nodeMergingTolerance=0.0001 * mesh_size, domain=MESH, originalInstances=DELETE)

    p1 = mdb.models[model_name].parts[part2DName + 'half']

    a1 = mdb.models[model_name].rootAssembly
    p = mdb.models[model_name].parts[part2DName + 'half']
    a1.Instance(name=part2DName + 'half' + '-2', part=p, dependent=ON)
    a1 = mdb.models[model_name].rootAssembly
    a1.rotate(instanceList=(part2DName + 'half' + '-2',), axisPoint=(0.0, 0.0, 0.0),
              axisDirection=(10.0, 0.0, 0.0), angle=180.0)
    ##: The instance Part-3-2 was rotated by 180. degrees about the axis defined by the point 0., 0., 0. and the vector 10., 0., 0.

    a1 = mdb.models[model_name].rootAssembly
    a1.InstanceFromBooleanMerge(name=part2DFullName, instances=(a1.instances[part2DName + 'half' + '-1'],
                                                                a1.instances[part2DName + 'half' + '-2'],),
                                mergeNodes=BOUNDARY_ONLY,
                                nodeMergingTolerance=0.0001 * mesh_size, domain=MESH, originalInstances=DELETE)

    # make the final merged part (shell model) has the same shell element normal (make the element connectivity arranged in the anticlockwise direction)
    p = mdb.models[model_name].parts[part2DFullName]
    z1 = p.elements
    regions = regionToolset.Region(elements=z1)
    p.flipNormal(referenceRegion=z1[1], regions=regions)

    # delete the unwanted part and instances
    # a.deleteFeatures((part2DName+'-1', part2DName+'-2', part2DName+'half-1',  part2DName+'half-2', ))
    del mdb.models[model_name].parts[part2DName + 'half']
    del mdb.models[model_name].parts[part2DName]
    a = mdb.models[model_name].rootAssembly
    del a.features[part2DFullName + '-1']

    #    setYZview()
    p = mdb.models[model_name].parts[part2DFullName]
    #    session.viewports['Viewport: 1'].setValues(displayedObject = a)
    #    session.viewports['Viewport: 1'].view.setViewpoint(viewVector = (1.0, 0.0, 0.0), cameraUpVector = (0.0, 0.0, 1.0))
    #    session.viewports['Viewport: 1'].view.fitView()
    #    cmap=session.viewports['Viewport: 1'].colorMappings['Material']
    #    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    #    session.viewports['Viewport: 1'].disableMultipleColors()

    return p ,part2DFullName


# ==============================================================================
#
#   Hexagonal Unidirectional Fiber
#
# ==============================================================================

def createHexV5(model_name, fiber_flag, vf_f, fiber_matname, matrix_matname, mesh_size, elem_type):
    # ---------------------------------------------------------
    part2DName = 'hexP2' + 'quater'
    part2DFullName = 'hexP2'
    partsobj = mdb.models[model_name].parts

    print
    '#-------part_name  %s---------------------------' % part2DFullName
    # ---------------------------------------
    #### Define Parameters
    # --------------------------------------

    blockSize = 1.0
    blockSizeA = blockSize / 2.0
    blockSizeB = blockSize * sqrt(3.0) / 2.0
    meshSize = mesh_size

    if elem_type == 'Linear':
        elementType1 = S4
        elementType2 = S3
    elif elem_type == 'Quadratic':
        elementType1 = S8R
        elementType2 = STRI65

    totalArea = blockSizeA * blockSizeB * 4.0

    if fiber_flag == 1:  # vf_f is volume fraction  of the fiber
        vof_fiber = vf_f
        fiberRadius = blockSize * sqrt(sqrt(3.0) * vof_fiber / 2.0 / pi)
    elif fiber_flag == 2:  # vf_f is radius of the fiber
        fiberRadius = vf_f
        vof_fiber = 2.0 * pi * fiberRadius ** 2.0 / totalArea

    print
    'blockSize: %s' % blockSize
    print
    'totalArea: %s' % totalArea

    print
    '#---fiber------------------------'
    print
    'vof_fiber: %s' % vof_fiber
    print
    'fiberRadius: %s' % fiberRadius

    if fiberRadius >= blockSize / 2.0:
        raise ValueError('The volume fraction of fiber is out of range. Please adjust the values.')

    fiber_setname = 'Fiber_section'
    matrix_setname = 'Matrix_section'

    p = mdb.models[model_name].Part(name=part2DName, dimensionality=THREE_D,
                                    type=DEFORMABLE_BODY)

    datumPlaneYZ_id = p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0).id
    datumAxisZ_id = p.DatumAxisByPrincipalAxis(principalAxis=ZAXIS).id
    # ---------------------------------------------------
    YZworkPlaneTransform = (0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0)  # y-z plane
    #    YZviewVector = (1.0, 0.0, 0.0)
    #    YZcameraUpVector = (0.0, 0.0, 1.0)
    # --------------------------------------------------
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__',
                                                 sheetSize=200.0, transform=YZworkPlaneTransform)

    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    #    session.viewports['Viewport: 1'].view.setValues(session.views['Left'])

    p = mdb.models[model_name].parts[part2DName]

    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.rectangle(point1=(0.0, 0.0), point2=(blockSizeA, blockSizeB))
    p = mdb.models[model_name].parts[part2DName]
    e1, d2 = p.edges, p.datums
    p.Shell(sketchPlane=d2[datumPlaneYZ_id], sketchUpEdge=d2[datumAxisZ_id], sketchPlaneSide=SIDE1,
            sketchOrientation=RIGHT, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']

    # Define fiber on the shell
    # --------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    f, e, d1 = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f[0], sketchUpEdge=e[1],
                              sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
    s1 = mdb.models[model_name].ConstrainedSketch(name='__profile__',
                                                  sheetSize=blockSize * 4.00, gridSpacing=0.1 * blockSize, transform=t)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[model_name].parts[part2DName]
    p.projectReferencesOntoSketch(sketch=s1, filter=COPLANAR_EDGES)
    s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, fiberRadius), point2=(fiberRadius,
                                                                             0.0), direction=CLOCKWISE)
    s1.CoincidentConstraint(entity1=v[4], entity2=g[5], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[5], entity2=g[2], addUndoState=False)
    #: Warning: Cannot continue yet--complete the step or cancel the procedure.
    s1.ArcByCenterEnds(center=(blockSizeA, blockSizeA * sqrt(3)),
                       point1=(blockSizeA - fiberRadius, blockSizeA * sqrt(3)), point2=(blockSizeA,
                                                                                        blockSizeA * sqrt(
                                                                                            3) - fiberRadius),
                       direction=COUNTERCLOCKWISE)
    s1.CoincidentConstraint(entity1=v[6], entity2=g[4], addUndoState=False)
    s1.CoincidentConstraint(entity1=v[7], entity2=g[3], addUndoState=False)
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#1 ]',), )
    e1, d2 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e1[1], faces=pickedFaces, sketch=s1)
    s1.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']

    # Define materials and Sections and assign them
    # --------------------------------------

    # create sections
    mdb.models[model_name].HomogeneousShellSection(name=matrix_setname, preIntegrate=OFF,
                                                   material=matrix_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize,
                                                   thicknessField='', idealization=NO_IDEALIZATION,
                                                   poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)
    mdb.models[model_name].HomogeneousShellSection(name=fiber_setname, preIntegrate=OFF,
                                                   material=fiber_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize, thicknessField='',
                                                   idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)
    # Assign sections
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#3 ]',), )
    region = p.Set(faces=faces, name=fiber_setname)
    p = mdb.models[model_name].parts[part2DName]
    p.SectionAssignment(region=region, sectionName=fiber_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#4 ]',), )
    region = p.Set(faces=faces, name=matrix_setname)
    p = mdb.models[model_name].parts[part2DName]
    p.SectionAssignment(region=region, sectionName=matrix_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    # generate mesh on the quarter shell part
    # ----------------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    p.seedPart(size=meshSize, deviationFactor=0.1, minSizeFactor=0.1)
    elemType1 = mesh.ElemType(elemCode=elementType1, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=elementType2, elemLibrary=STANDARD)
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#7 ]',), )
    pickedRegions = (faces,)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    pickedRegions = f.getSequenceFromMask(mask=('[#7 ]',), )
    p.setMeshControls(regions=pickedRegions, elemShape=QUAD, algorithm=MEDIAL_AXIS)
    p = mdb.models[model_name].parts[part2DName]
    p.generateMesh()

    # import the quarter Shell part in the Assembly
    # generate the full shell model by doing 2 reflect
    a1 = mdb.models[model_name].rootAssembly
    p = mdb.models[model_name].parts[part2DName]
    a1.Instance(name=part2DName + '-1', part=p, dependent=ON)
    a1.Instance(name=part2DName + '-2', part=p, dependent=ON)

    a1 = mdb.models[model_name].rootAssembly
    a1.rotate(instanceList=(part2DName + '-2',), axisPoint=(0.0, 0.0, 0.0),
              axisDirection=(0.0, 10.0, 0.0), angle=180.0)

    a1 = mdb.models[model_name].rootAssembly
    a1.InstanceFromBooleanMerge(name=part2DName + 'half', instances=(a1.instances[part2DName + '-1'],
                                                                     a1.instances[part2DName + '-2'],),
                                mergeNodes=BOUNDARY_ONLY,
                                nodeMergingTolerance=0.0001 * meshSize, domain=MESH, originalInstances=DELETE)

    p1 = mdb.models[model_name].parts[part2DName + 'half']
    a1 = mdb.models[model_name].rootAssembly
    p = mdb.models[model_name].parts[part2DName + 'half']
    a1.Instance(name=part2DName + 'half' + '-2', part=p, dependent=ON)
    a1 = mdb.models[model_name].rootAssembly
    a1.rotate(instanceList=(part2DName + 'half' + '-2',), axisPoint=(0.0, 0.0, 0.0),
              axisDirection=(10.0, 0.0, 0.0), angle=180.0)
    ##: The instance Part-3-2 was rotated by 180. degrees about the axis defined by the point 0., 0., 0. and the vector 10., 0., 0.

    a1 = mdb.models[model_name].rootAssembly
    a1.InstanceFromBooleanMerge(name=part2DFullName, instances=(a1.instances[part2DName + 'half' + '-1'],
                                                                a1.instances[part2DName + 'half' + '-2'],),
                                mergeNodes=BOUNDARY_ONLY,
                                nodeMergingTolerance=0.0001 * meshSize, domain=MESH, originalInstances=DELETE)

    # make the final merged part (shell model) has the same shell element normal (make the element connectivity arranged in the anticlockwise direction)
    p = mdb.models[model_name].parts[part2DFullName]
    z1 = p.elements
    regions = regionToolset.Region(elements=z1)
    p.flipNormal(referenceRegion=z1[1], regions=regions)

    # delete the unwanted part and instances
    # a.deleteFeatures((part2DName+'-1', part2DName+'-2', part2DName+'half-1',  part2DName+'half-2', ))
    del mdb.models[model_name].parts[part2DName + 'half']
    del mdb.models[model_name].parts[part2DName]
    a = mdb.models[model_name].rootAssembly
    del a.features[part2DFullName + '-1']

    #    setYZview()
    p = mdb.models[model_name].parts[part2DFullName]
    #    session.viewports['Viewport: 1'].setValues(displayedObject = a)
    #    session.viewports['Viewport: 1'].view.setViewpoint(viewVector = (1.0, 0.0, 0.0), cameraUpVector = (0.0, 0.0, 1.0))
    #    session.viewports['Viewport: 1'].view.fitView()
    #    cmap=session.viewports['Viewport: 1'].colorMappings['Material']
    #    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    #    session.viewports['Viewport: 1'].disableMultipleColors()

    return p, part2DFullName


# ==============================================================================
#
#   Hexagonal Unidirectional Fiber with Interphase
#
# ==============================================================================

def createHexInterfaceV5(model_name, fiber_flag, vf_f, interface_flag,
                         t_interface, fiber_matname, matrix_matname,
                         interface_matname, mesh_size, elem_type):
    # ---------------------------------------
    #### Define Parameters
    # --------------------------------------

    part2DName = 'hexP3' + 'quater'
    part2DFullName = 'hexP3'

    fiber_setname = 'Fiber_section'
    matrix_setname = 'Matrix_section'
    interface_setname = 'Interphase_section'

    partsobj = mdb.models[model_name].parts

    print
    '#-------part_name  %s---------------------------' % part2DFullName

    # ---------------------------------------------------------
    blockSize = 1.0
    blockSizeA = blockSize / 2.0
    blockSizeB = blockSize * sqrt(3.0) / 2.0

    meshSize = mesh_size

    if elem_type == 'Linear':
        elementType1 = S4
        elementType2 = S3
    elif elem_type == 'Quadratic':
        elementType1 = S8R
        elementType2 = STRI65

    totalArea = blockSizeA * blockSizeB * 4.0

    if fiber_flag == 1:  # vf_f is volume fraction  of the fiber
        vof_fiber = vf_f
        fiberRadius = blockSize * sqrt(sqrt(3.0) * vof_fiber / 2.0 / pi)
    elif fiber_flag == 2:  # vf_f is radius of the fiber
        fiberRadius = vf_f
        vof_fiber = 2.0 * pi * fiberRadius ** 2.0 / totalArea

    try:
        if interface_flag == 1:  # t_interface is volume fraction of the interface
            vof_interface = t_interface
            interfaceRadius = blockSize * sqrt(sqrt(3) * (vof_interface + vof_fiber) / 2 / pi)
        elif interface_flag == 2:  # t_interface is thickness of the interface
            interfaceRadius = fiberRadius + t_interface
            vof_interface = 2 * pi * (interfaceRadius ** 2 - fiberRadius ** 2) / totalArea

        if interfaceRadius >= blockSize / 2.0:
            False
    except:
        raise ValueError('The volume fraction of fiber and interphase is out of range. Please adjust the values.')

    print
    'blockSize: %s' % blockSize
    print
    'totalArea: %s' % totalArea

    print
    '#---fiber------------------------'
    print
    'vof_fiber: %s' % vof_fiber
    print
    'fiberRadius: %s' % fiberRadius

    print
    '#---interface-------------------------'
    print
    'vof_interface: %s' % vof_interface
    print
    'interfaceRadius: %s' % interfaceRadius
    # --------------------------------------------------------------

    p = mdb.models[model_name].Part(name=part2DName, dimensionality=THREE_D,
                                    type=DEFORMABLE_BODY)

    datumPlaneYZ_id = p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0).id
    datumAxisZ_id = p.DatumAxisByPrincipalAxis(principalAxis=ZAXIS).id
    # ---------------------------------------------------
    YZworkPlaneTransform = (0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0)  # y-z plane
    #    YZviewVector = (1.0, 0.0, 0.0)
    #    YZcameraUpVector = (0.0, 0.0, 1.0)
    # --------------------------------------------------
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__',
                                                 sheetSize=200.0, transform=YZworkPlaneTransform)

    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    #    session.viewports['Viewport: 1'].view.setValues(session.views['Left'])

    p = mdb.models[model_name].parts[part2DName]

    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.rectangle(point1=(0.0, 0.0), point2=(blockSizeA, blockSizeB))
    p = mdb.models[model_name].parts[part2DName]
    e1, d2 = p.edges, p.datums
    p.Shell(sketchPlane=d2[datumPlaneYZ_id], sketchUpEdge=d2[datumAxisZ_id], sketchPlaneSide=SIDE1,
            sketchOrientation=RIGHT, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']

    p = mdb.models[model_name].parts[part2DName]

    # --------------------------------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    f1, e, d = p.faces, p.edges, p.datums
    t = p.MakeSketchTransform(sketchPlane=f1[0], sketchUpEdge=e[1],
                              sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
    s = mdb.models[model_name].ConstrainedSketch(name='__profile__', sheetSize=2.0,
                                                 gridSpacing=0.04, transform=t)
    g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=SUPERIMPOSE)
    p = mdb.models[model_name].parts[part2DName]
    p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, fiberRadius))
    s.CoincidentConstraint(entity1=v[4], entity2=g[5], addUndoState=False)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(0.0, interfaceRadius))

    s.CoincidentConstraint(entity1=v[5], entity2=g[5], addUndoState=False)
    s.CircleByCenterPerimeter(center=(blockSizeA, blockSizeB), point1=(blockSizeA, blockSizeB - fiberRadius))

    s.CoincidentConstraint(entity1=v[6], entity2=g[3], addUndoState=False)
    s.CircleByCenterPerimeter(center=(blockSizeA, blockSizeB), point1=(blockSizeA, blockSizeB - interfaceRadius))

    s.CoincidentConstraint(entity1=v[7], entity2=g[3], addUndoState=False)
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    pickedFaces = f.getSequenceFromMask(mask=('[#1 ]',), )
    e1, d2 = p.edges, p.datums
    p.PartitionFaceBySketch(sketchUpEdge=e1[1], faces=pickedFaces, sketch=s)
    s.unsetPrimaryObject()
    del mdb.models[model_name].sketches['__profile__']

    # Define Sections and assign them
    # --------------------------------------
    mdb.models[model_name].HomogeneousShellSection(name=fiber_setname, preIntegrate=OFF,
                                                   material=fiber_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize, thicknessField='',
                                                   idealization=NO_IDEALIZATION, poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)

    mdb.models[model_name].HomogeneousShellSection(name=matrix_setname, preIntegrate=OFF,
                                                   material=matrix_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize,
                                                   thicknessField='', idealization=NO_IDEALIZATION,
                                                   poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)

    mdb.models[model_name].HomogeneousShellSection(name=interface_setname, preIntegrate=OFF,
                                                   material=interface_matname, thicknessType=UNIFORM,
                                                   thickness=0.01 * blockSize,
                                                   thicknessField='', idealization=NO_IDEALIZATION,
                                                   poissonDefinition=DEFAULT,
                                                   thicknessModulus=None, temperature=GRADIENT, useDensity=OFF,
                                                   integrationRule=SIMPSON, numIntPts=5)

    # define sets
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    faces = f.findAt(((0.0, 0.0, 0.0),), ((0.0, blockSizeA, blockSizeB),))
    p.Set(faces=faces, name=fiber_setname)
    #: The set 'fiber' has been created (2 faces).

    f = p.faces
    faces = f.findAt(((0.0, blockSizeA / 2.0, blockSizeB / 2.0),))
    p.Set(faces=faces, name=matrix_setname)
    #: The set 'matrix' has been created (1 face).

    f = p.faces
    faces = f.findAt(((0.0, (fiberRadius + interfaceRadius) / 2.0, 0.0),),
                     ((0.0, blockSizeA - (fiberRadius + interfaceRadius) / 2.0, blockSizeB),))
    p.Set(faces=faces, name=interface_setname)
    #: The set 'Interphase' has been created (2 faces).

    p = mdb.models[model_name].parts[part2DName]
    region = p.sets[fiber_setname]
    p.SectionAssignment(region=region, sectionName=fiber_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    region = p.sets[interface_setname]
    p.SectionAssignment(region=region, sectionName=interface_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    region = p.sets[matrix_setname]
    p.SectionAssignment(region=region, sectionName=matrix_setname, offset=0.0,
                        offsetType=MIDDLE_SURFACE, offsetField='',
                        thicknessAssignment=FROM_SECTION)

    # assign material direction
    # -----------------------------------------
    p = mdb.models[model_name].parts[part2DName]
    region = p.sets[fiber_setname]
    orientation = None
    mdb.models[model_name].parts[part2DName].MaterialOrientation(region=region,
                                                                 orientationType=GLOBAL, axis=AXIS_1,
                                                                 additionalRotationType=ROTATION_NONE,
                                                                 localCsys=None, fieldName='')
    #: Specified material orientation has been assigned to the selected regions.
    p = mdb.models[model_name].parts[part2DName]
    region = p.sets[matrix_setname]
    orientation = None
    mdb.models[model_name].parts[part2DName].MaterialOrientation(region=region,
                                                                 orientationType=GLOBAL, axis=AXIS_1,
                                                                 additionalRotationType=ROTATION_NONE,
                                                                 localCsys=None, fieldName='')
    #: Specified material orientation has been assigned to the selected regions.
    p = mdb.models[model_name].parts[part2DName]
    region = p.sets[interface_setname]
    orientation = None
    mdb.models[model_name].parts[part2DName].MaterialOrientation(region=region,
                                                                 orientationType=GLOBAL, axis=AXIS_1,
                                                                 additionalRotationType=ROTATION_NONE,
                                                                 localCsys=None, fieldName='')
    session.viewports['Viewport: 1'].setValues(displayedObject=p)

    # generate mesh
    p = mdb.models[model_name].parts[part2DName]
    f = p.faces
    pickedRegions = f.getSequenceFromMask(mask=('[#1f ]',), )
    p.setMeshControls(regions=pickedRegions, elemShape=QUAD, algorithm=MEDIAL_AXIS)
    p = mdb.models[model_name].parts[part2DName]
    p.seedPart(size=0.054, deviationFactor=0.1, minSizeFactor=0.1)

    elemType1 = mesh.ElemType(elemCode=elementType1, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=elementType2, elemLibrary=STANDARD)

    faces = f.getSequenceFromMask(mask=('[#1f ]',), )
    pickedRegions = (faces,)
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    p = mdb.models[model_name].parts[part2DName]
    p.generateMesh()

    # import the quarter Shell part in the Assembly
    # generate the full shell model by doing 2 reflect
    # -------------------------------------------------------
    a1 = mdb.models[model_name].rootAssembly
    p = mdb.models[model_name].parts[part2DName]
    a1.Instance(name=part2DName + '-1', part=p, dependent=ON)
    a1.Instance(name=part2DName + '-2', part=p, dependent=ON)

    a1 = mdb.models[model_name].rootAssembly
    a1.rotate(instanceList=(part2DName + '-2',), axisPoint=(0.0, 0.0, 0.0),
              axisDirection=(0.0, 10.0, 0.0), angle=180.0)

    a1 = mdb.models[model_name].rootAssembly
    a1.InstanceFromBooleanMerge(name=part2DName + 'half', instances=(a1.instances[part2DName + '-1'],
                                                                     a1.instances[part2DName + '-2'],),
                                mergeNodes=BOUNDARY_ONLY,
                                nodeMergingTolerance=0.0001 * meshSize, domain=MESH, originalInstances=DELETE)

    p1 = mdb.models[model_name].parts[part2DName + 'half']

    a1 = mdb.models[model_name].rootAssembly
    p = mdb.models[model_name].parts[part2DName + 'half']
    a1.Instance(name=part2DName + 'half' + '-2', part=p, dependent=ON)
    a1 = mdb.models[model_name].rootAssembly
    a1.rotate(instanceList=(part2DName + 'half' + '-2',), axisPoint=(0.0, 0.0, 0.0),
              axisDirection=(10.0, 0.0, 0.0), angle=180.0)
    ##: The instance Part-3-2 was rotated by 180. degrees about the axis defined by the point 0., 0., 0. and the vector 10., 0., 0.

    a1 = mdb.models[model_name].rootAssembly
    a1.InstanceFromBooleanMerge(name=part2DFullName, instances=(a1.instances[part2DName + 'half' + '-1'],
                                                                a1.instances[part2DName + 'half' + '-2'],),
                                mergeNodes=BOUNDARY_ONLY,
                                nodeMergingTolerance=0.0001 * meshSize, domain=MESH, originalInstances=DELETE)

    # make the final merged part (shell model) has the same shell element normal (make the element connectivity arranged in the anticlockwise direction)
    p = mdb.models[model_name].parts[part2DFullName]
    z1 = p.elements
    regions = regionToolset.Region(elements=z1)
    p.flipNormal(referenceRegion=z1[1], regions=regions)

    # delete the unwanted part and instances
    # a.deleteFeatures((part2DName+'-1', part2DName+'-2', part2DName+'half-1',  part2DName+'half-2', ))
    del mdb.models[model_name].parts[part2DName + 'half']
    del mdb.models[model_name].parts[part2DName]
    a = mdb.models[model_name].rootAssembly
    del a.features[part2DFullName + '-1']

    #    setYZview()
    p = mdb.models[model_name].parts[part2DFullName]
    #    session.viewports['Viewport: 1'].setValues(displayedObject = a)
    #    session.viewports['Viewport: 1'].view.setViewpoint(viewVector = (1.0, 0.0, 0.0), cameraUpVector = (0.0, 0.0, 1.0))
    #    session.viewports['Viewport: 1'].view.fitView()
    #    cmap=session.viewports['Viewport: 1'].colorMappings['Material']
    #    session.viewports['Viewport: 1'].setColor(colorMapping=cmap)
    #    session.viewports['Viewport: 1'].disableMultipleColors()


    return p,part2DFullName

def homogenization(
        gen_input_only, model_source, macro_model, analysis,
        elem_flag, trans_flag, ap1, ap2, ap3, w='',
        model_name2='',part_name='', abaqus_input='', new_filename='',
        specific_model=0, bk=[[0.0, 0.0, 0.0]],
        sk=[[0.0, 0.0]], cos=[[1.0, 0.0]], temp_flag=0):

    # ap = []
    # ap = [
    #     ['ap000', ap000], ['ap100', ap100], ['ap010', ap010], ['ap001', ap001],
    #     ['ap111', ap111], ['ap110', ap110], ['ap101', ap101], ['ap011', ap011]
    # ]
    # ap_dic = {}
    # apvector = []
    # ap_dic['ap000'] = [0, 0, 0]
    # ap_dic['ap100'] = [1, 0, 0]
    # ap_dic['ap010'] = [0, 1, 0]
    # ap_dic['ap001'] = [0, 0, 1]
    # ap_dic['ap111'] = [1, 1, 1]
    # ap_dic['ap110'] = [1, 1, 0]
    # ap_dic['ap101'] = [1, 0, 1]
    # ap_dic['ap011'] = [0, 1, 1]

    if analysis == 33:
        analysis = 3
    elif analysis == 44:
        analysis = 4

    apvector = [0, 0, 0]
    # print ap1
    # print ap2
    # print ap3

    if ap1:
        apvector[0] = 1
    if ap2:
        apvector[1] = 1
    if ap3:
        apvector[2] = 1

    # print apvector

    # Definition of the time vector for viscoelastic and thermoviscoelastic cases
    tvector = [0, 0, 0]  # Initial time, Final Time, Time increment in decades
    # print tvector
    # part_name=p
    if model_source == 1:
        print
        "inside if"
        nSG = determineNSG(model_name2, part_name)
        macro_model_dimension = str(macro_model) + 'D'
        print
        'Dimension of Structure Genome: ' + str(nSG)
        print
        'Dimension of Macroscopic Model: ' + macro_model_dimension

        if w == '':  # w imported is a string, this if-else gives w as a float
            w = determineVolume(
                model_name2, part_name, macro_model_dimension, nSG
            )
        else:
            w = float(w)

        print
        tvector
        if nSG == 2 or nSG == 3:
            [sc_input, macro_model_dim] = generateInputFromCAE(
                model_source, macro_model_dimension,
                analysis, elem_flag, trans_flag, w, nSG,
                model_name2, part_name, abaqus_input, new_filename,
                specific_model, bk[0],
                sk[0], cos[0], temp_flag, apvector, tvector
            )

        elif nSG == 1:
            [sc_input, macro_model_dim] = generate_1DInputFromCAE(
                model_source, macro_model_dimension,
                analysis, elem_flag, trans_flag, w, nSG,
                model_name2, part_name, abaqus_input, new_filename,
                specific_model, bk[0],
                sk[0], cos[0], temp_flag, tvector
            )  # ,nlayer

    elif model_source == 2:
        if w == '':
            w = 0.0
        else:
            w = float(w)

        # [sc_input, macro_model_dim] = convert2sc(
        #     abaqus_input, new_filename, macro_model, specific_model,
        #     analysis, elem_flag, trans_flag, temp_flag,
        #     bk[0], sk[0], cos[0], w
        # )

        [sc_input, macro_model_dim] = createSCInputMain(
            abaqus_input, new_filename, macro_model, specific_model,
            analysis, elem_flag, trans_flag, temp_flag, tvector,
            bk[0], sk[0], cos[0], w
        )

    with open(str(sc_input), 'r') as f:
        lines = f.readlines()
        if analysis == 0:
            lines[0] = '\t\t0\t0\t0\t0\t0\t0\n'
        if analysis == 1:
            lines[0] = '\t\t1\t0\t0\t0\t0\t0\n'

    with open(str(sc_input), 'w') as f:
        f.writelines(lines)

    print
    'Finish creating SwiftComp input.'

    if not gen_input_only:
        try:
            scTimestart = time.clock()
            if apvector == [0, 0, 0]:
                os.system(
                    'Swiftcomp ' + sc_input + ' ' + macro_model_dim + ' H'
                )
            else:
                os.system(
                    'Swiftcomp ' + sc_input + ' ' + macro_model_dim + ' HA'
                )

            scTimeEnd = time.clock()
            scTime = scTimeEnd - scTimestart

            # os.system('Notepad ' + sc_input + '.k')
            comp_file = sc_input + '.k'
            mystring = ''
            with open(comp_file, 'r')as f:
                lines = f.readlines()
                ECStart = [i for i in range(len(lines)) if 'Engineering Constants' in lines[i]]

                def is_num(s):
                    try:
                        float(s)
                    except ValueError:
                        return False
                    else:
                        return True

                mylist = []
                for j in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
                    for i in lines[ECStart[0] + j].split():
                        if is_num(i):
                            mylist.append(i)
            [E1, E2, E3, G12, G13, G23, v12, v13, v23] = mylist
            mdb.models['Model-1'].Material('Lamina')
            mdb.models['Model-1'].materials['Lamina'].Elastic(type=ENGINEERING_CONSTANTS, table=((
                                                                                           float(E1), float(E2),
                                                                                           float(E3), float(v12),
                                                                                           float(v13), float(v23),
                                                                                           float(G12), float(G13),
                                                                                           float(G23)),))
            if analysis == 1:
                with open(comp_file, 'r') as f2:
                    lines = f2.readlines()
                    TCStart = [i for i in range(len(lines)) if 'Thermal Coefficients' in lines[i]]

                    mylist = []
                    for j in [2, 3, 4]:
                        for i in lines[TCStart[0] + j].split():
                            if is_num(i):
                                mylist.append(i)

                [alpha11, alpha22, alpha33] = mylist

                mdb.models['Model-1'].materials['Lamina'].Expansion(type=ORTHOTROPIC, table=((float(alpha11), float(alpha22), float(alpha33)),))
            print
            'scTime: ' + str(scTime)

        except:
            raise WindowsError(
                '''
                Unexpected error happened. 
                Please check the Command line window 
                for more information.
                '''
            )

    #     str(sc_input)+'.k'
    return 1