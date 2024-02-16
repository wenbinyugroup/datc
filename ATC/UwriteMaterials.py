# -*- coding: utf-8 -*-

from utilities import *
from abaqus import *
from abaqusConstants import *
from material import *
from section import *
from scPronyMain import *

def writeMaterials(matDict, analysis, model_name, file):
    ntemp = 1
    temperature = 0
    model = mdb.models[model_name]
    for mat_name, mat_id in matDict.iteritems():
        try :
            model.materials[mat_name].density
        except:
            print 'density is not defined in material "%s" ' % mat_name
            print 'default values density = 0.1, temperature = 0 will be used,'
            print 'which will not influence the results if analysis is not temperature related.'
            model.materials[mat_name].Density(table=((0.0, ), ))
        density = model.materials[mat_name].density.table[0][0]
        
		#Definition of the parameters in case of viscoelastic/thermoviscoelastic analyses C - Constant, P - Prony, T - Time
        Para = model.materials[mat_name].materialIdentifier	

        if analysis in [7,8]:
           LEN=len(model.materials[mat_name].elastic.table)
           if Para != '' and LEN !=1:
				Para = Para				
				xC=0
           else: 
				Para = ' C'
				LEN=1
				if analysis in [8]:
					mp1sheat = model.materials[mat_name].specificHeat.table[0]
					mp1cte   = model.materials[mat_name].expansion.table[0]
					mp1      = list(mp1cte) + list(mp1sheat)
				
        else:
            Para = ''
            LEN=1			
		
        if analysis != 2:
            matType = model.materials[mat_name].elastic.type
            mp = model.materials[mat_name].elastic.table [0]	
            if analysis == 1:
                mp1sheat = model.materials[mat_name].specificHeat.table[0]
                mp1cte   = model.materials[mat_name].expansion.table[0]
                mp1      = list(mp1cte) + list(mp1sheat)
            elif analysis == 3:
                mp3pieT = model.materials[mat_name].piezoelectric.type
                mp3pie = model.materials[mat_name].piezoelectric.table[0]
                mp3d = model.materials[mat_name].dielectric.table[0]


            if matType == ISOTROPIC:
                writeFormat(file, 'ddd', [int(mat_id), 0, ntemp])
                writeFormat(file, 'EEld', [float(temperature), float(density),Para,LEN])
                if LEN > 1:
                    for xC in range (0,int(LEN)):
					    mp2=model.materials[mat_name].elastic.table[int(xC)]
					    writeFormat(file, 'E', [mp2[2]])
					    writeFormat(file, 'EE', [mp2[0], mp2[1]])
					    if analysis == 8:
							mp8   = model.materials[mat_name].expansion.table[int(xC)]
							mp8c=[mp8[0], 1.0 ]
							writeFormat(file, 'E'*2, mp8c)						
                else:
                    writeFormat(file, 'EE', mp[:2])
                    if analysis in [1,8]:
						try:
							writeFormat(file, 'EE', mp1)
						except:
							raise materialTypeError( 'Isotropic CTE and specificHeat is not properly defined in material \'%s\' ' % mat_name)
							print 'Isotropic CTE and specificHeat is not defined properly in material \'%s\' ' %mat_name
							print 'CTE must have the same type as the elastic properties: isotropic, orthotropic or anisotropic for the same material.'
                    elif analysis == 3 and mp3pieT == STRESS:
						try:
							writeFormat(file, 'E' * 6, [mp3pie[0], mp3pie[1], mp3pie[2], mp3pie[5], mp3pie[4], mp3pie[3]])
							writeFormat(file, 'E' * 6, [mp3pie[6], mp3pie[7], mp3pie[8], mp3pie[11], mp3pie[10], mp3pie[9] ])
							writeFormat(file, 'E' * 6, [mp3pie[12], mp3pie[13], mp3pie[14], mp3pie[17], mp3pie[16], mp3pie[15] ])
							writeFormat(file, 'E', mp3d )
						except:
							raise materialTypeError( 'Piezolectricity (stress based) and isotropic electrical permitivity are not properly defined in material \'%s\' ' % mat_name)
							print 'Piezolectricity (stress based) and isotropic electrical permitivity are not defined properly in material \'%s\' ' %mat_name
							print 'Piezoelectricity should be defined based on stress. Electric permitivity must have the same type as the elastic properties: isotropic, orthotropic or anisotropic for the same material.'

            elif matType == ENGINEERING_CONSTANTS:
                writeFormat(file, 'ddd', [int(mat_id), 1, ntemp])
                writeFormat(file, 'EEld', [float(temperature), float(density),Para,LEN])
                if LEN > 1:
                    for xC in range (0,int(LEN)):
					    mp2=model.materials[mat_name].elastic.table[int(xC)]
					    writeFormat(file, 'E', [mp2[9]])
					    writeFormat(file, 'EEE', mp2[:3])
					    writeFormat(file, 'EEE', mp2[6:9])
					    writeFormat(file, 'EEE', mp2[3:6])
					    if analysis == 8:
							mp8   = model.materials[mat_name].expansion.table[int(xC)]
							mp8c=[mp8[0],mp8[1],mp8[2], 1.0 ]
							writeFormat(file, 'E'*4, mp8c)							
                else:
                    writeFormat(file, 'EEE', mp[:3])
                    writeFormat(file, 'EEE', mp[6:9])
                    writeFormat(file, 'EEE', mp[3:6])
                    if analysis in [1,8]:
						try:
							writeFormat(file, 'E'*4, mp1)
						except:
							raise materialTypeError( 'Orthotropic CTE and specificHeat is not properly defined in material \'%s\' ' % mat_name)
							print 'Orthotropic CTE and specificHeat is not properly defined in material \'%s\' ' % mat_name
							print 'CTE must have the same type as the elastic properties: isotropic, orthotropic or anisotropic for the same material.'
                    elif analysis == 3 and mp3pieT == STRESS:
						   try:
								writeFormat(file, 'E' * 6, [mp3pie[0], mp3pie[1], mp3pie[2], mp3pie[5], mp3pie[4],mp3pie[3]])
								writeFormat(file, 'E' * 6, [mp3pie[6], mp3pie[7], mp3pie[8], mp3pie[11], mp3pie[10],mp3pie[9]])
								writeFormat(file, 'E' * 6, [mp3pie[12], mp3pie[13], mp3pie[14], mp3pie[17], mp3pie[16],mp3pie[15]])
								writeFormat(file, 'E'*3, mp3d)
						   except:
								raise materialTypeError('Piezolectricity (stress based) and orthotropic electrical permitivity are not properly defined in material \'%s\' ' % mat_name)
								print 'Piezolectricity (stress based) and isotropic electrical permitivity are not defined properly in material \'%s\' ' % mat_name
								print 'Piezoelectricity should be defined based on stress. Electric permitivity must have the same type as the elastic properties: isotropic, orthotropic or anisotropic for the same material.'

            elif matType == ORTHOTROPIC:
                writeFormat(file, 'ddd', [int(mat_id), 2, ntemp])
                writeFormat(file, 'EEld', [float(temperature), float(density),Para,LEN])			
                if LEN > 1:
                    for xC in range (0,int(LEN)):
					    mp2=model.materials[mat_name].elastic.table[int(xC)]
					    writeFormat(file, 'E', [mp2[9]])
					    writeFormat(file, 'E'*6, [mp2[0], mp2[1],  mp2[3], 0.0, 0.0, 0.0])
					    writeFormat(file, 'E'*5, [       mp2[2],  mp2[4], 0.0, 0.0, 0.0])
					    writeFormat(file, 'E'*4, [               mp2[5], 0.0, 0.0, 0.0])
					    writeFormat(file, 'E'*3, [                    mp2[8], 0.0, 0.0])
					    writeFormat(file, 'E'*2, [                          mp2[7], 0.0])
					    writeFormat(file, 'E'*1, [                                mp2[6]])
					    if analysis == 8:
							mp8   = model.materials[mat_name].expansion.table[int(xC)]
							mp8c=[mp8[0],mp8[1],mp8[2], 0.0, 0.0, 0.0, 1.0 ]
							writeFormat(file, 'E'*7, mp8c)	
                else:
                    writeFormat(file, 'E'*6, [mp[0], mp[1],  mp[3], 0.0, 0.0, 0.0])
                    writeFormat(file, 'E'*5, [       mp[2],  mp[4], 0.0, 0.0, 0.0])
                    writeFormat(file, 'E'*4, [               mp[5], 0.0, 0.0, 0.0])
                    writeFormat(file, 'E'*3, [                    mp[8], 0.0, 0.0])
                    writeFormat(file, 'E'*2, [                          mp[7], 0.0])
                    writeFormat(file, 'E'*1, [                                mp[6]])
                    # writeFormat(file, 'ddd', [int(mat_id), 2, ntemp])
                    # writeFormat(file, 'EE', [float(temperature), float(density)])
                    # writeFormat(file, 'E'*6, [mp[0], mp[1], mp[3], 0.0, 0.0, 0.0])
                    # writeFormat(file, 'E'*5,        [mp[2], mp[4], 0.0, 0.0, 0.0])
                    # writeFormat(file, 'E'*4,               [mp[5], 0.0, 0.0, 0.0])
                    # writeFormat(file, 'E'*3,                      [mp[6], 0.0, 0.0])
                    # writeFormat(file, 'E'*2,                             [mp[7], 0.0])
                    # writeFormat(file, 'E'*1,                                   [mp[8]]) 
				
                    if analysis in [1,8]:
						try:
							mp1=[mp1[0],mp1[1],mp1[2], 0.0, 0.0, 0.0, mp1[3] ]
							writeFormat(file, 'E'*7, mp1)
						except:
							raise materialTypeError( 'Orthotropic CTE and specificHeat is not properly defined in material \'%s\' ' % mat_name)
							print 'Orthotropic CTE and specificHeat is not properly defined in material \'%s\' ' % mat_name
							print 'CTE must have the same type as the elastic properties: isotropic, orthotropic or anisotropic for the same material.'
                    elif analysis == 3 and mp3pieT == STRESS:
						try:
							writeFormat(file, 'E' * 6, [mp3pie[0], mp3pie[1], mp3pie[2], mp3pie[5], mp3pie[4], mp3pie[3]])
							writeFormat(file, 'E' * 6, [mp3pie[6], mp3pie[7], mp3pie[8], mp3pie[11], mp3pie[10], mp3pie[9]])
							writeFormat(file, 'E' * 6, [mp3pie[12], mp3pie[13], mp3pie[14], mp3pie[17], mp3pie[16], mp3pie[15]])
							writeFormat(file, 'E'*3, mp3d)
						except:
							raise materialTypeError('Piezolectricity (stress based) and orthotropic electrical permitivity are not properly defined in material \'%s\' ' % mat_name)
							print 'Piezolectricity (stress based) and isotropic electrical permitivity are not defined properly in material \'%s\' ' % mat_name
							print 'Piezoelectricity should be defined based on stress. Electric permitivity must have the same type as the elastic properties: isotropic, orthotropic or anisotropic for the same material.'

            elif matType == ANISOTROPIC:			
                writeFormat(file, 'ddd', [int(mat_id), 2, ntemp])
                writeFormat(file, 'EEld', [float(temperature), float(density), Para, LEN])
                if LEN > 1:
                    for xC in range (0,int(LEN)):
					    mp2=model.materials[mat_name].elastic.table[int(xC)]
					    writeFormat(file, 'E', [mp2[21]])
					    writeFormat(file, 'E'*6, [mp2[0], mp2[1], mp2[3], mp2[15], mp2[10], mp2[6]])
					    writeFormat(file, 'E'*5, [       mp2[2], mp2[4], mp2[16], mp2[11], mp2[7]])
					    writeFormat(file, 'E'*4, [              mp2[5], mp2[17], mp2[12], mp2[8]])
					    writeFormat(file, 'E'*3, [                     mp2[20], mp2[19], mp2[18]])
					    writeFormat(file, 'E'*2, [                             mp2[14], mp2[13]])
					    writeFormat(file, 'E'*1, [                                     mp2[9]])
					    if analysis == 8:
							mp8   = model.materials[mat_name].expansion.table[int(xC)]
							mp8c=[mp8[0],mp8[1],mp8[2], mp8[3], mp8[4], mp8[5], 1.0 ]
							writeFormat(file, 'E'*7, mp8c)							
                else:
                    writeFormat(file, 'E'*6, [mp[0], mp[1], mp[3], mp[15], mp[10], mp[6]])
                    writeFormat(file, 'E'*5, [       mp[2], mp[4], mp[16], mp[11], mp[7]])
                    writeFormat(file, 'E'*4, [              mp[5], mp[17], mp[12], mp[8]])
                    writeFormat(file, 'E'*3, [                     mp[20], mp[19], mp[18]])
                    writeFormat(file, 'E'*2, [                             mp[14], mp[13]])
                    writeFormat(file, 'E'*1, [                                     mp[9]])
                    # writeFormat(file, 'E'*6, [mp[0], mp[1], mp[3], mp[6], mp[10], mp[15]])
                    # writeFormat(file, 'E'*5, 		[mp[2], mp[4], mp[7], mp[11], mp[16]])
                    # writeFormat(file, 'E'*4, 			   [mp[5], mp[8], mp[12], mp[17]])
                    # writeFormat(file, 'E'*3, [                     mp[9], mp[13], mp[18]])
                    # writeFormat(file, 'E'*2, [							mp[14],	  mp[19]])
                    # writeFormat(file, 'E'*1, [									  mp[20]])							
                    if analysis in [1,8]:
						try:
							mp1=[mp1[0],mp1[1],mp1[2], mp1[5], mp1[4], mp1[3], mp1[6] ]
							writeFormat(file, 'E'*7, mp1)
						except:
							raise materialTypeError( 'Anisotropic CTE and specificHeat is not properly defined in material \'%s\' ' % mat_name)
							print 'Anisotropic CTE and specificHeat is not properly defined in material \'%s\' ' % mat_name
							print 'CTE must have the same type as the elastic properties: isotropic, orthotropic or anisotropic for the same material.'
                    elif analysis == 3 and mp3pieT == STRESS:
						try:
							writeFormat(file, 'E' * 6, [mp3pie[0], mp3pie[1], mp3pie[2], mp3pie[5], mp3pie[4], mp3pie[3]])
							writeFormat(file, 'E' * 6, [mp3pie[6], mp3pie[7], mp3pie[8], mp3pie[11], mp3pie[10], mp3pie[9]])
							writeFormat(file, 'E' * 6, [mp3pie[12], mp3pie[13], mp3pie[14], mp3pie[17], mp3pie[16], mp3pie[15]])
							writeFormat(file, 'E'*3,  [mp[0], mp[1], mp[3]])
							writeFormat(file, 'E'*3, [mp[1], mp[2], mp[4]])
							writeFormat(file, 'E'*3, [mp[3], mp[4], mp[5]])
						except:
							raise materialTypeError(
							'Piezolectricity (stress based) and orthotropic electrical permitivity are not properly defined in material \'%s\' ' % mat_name)
						print 'Piezolectricity (stress based) and isotropic electrical permitivity are not defined properly in material \'%s\' ' % mat_name
						print 'Piezoelectricity should be defined based on stress. Electric permitivity must have the same type as the elastic properties: isotropic, orthotropic or anisotropic for the same material.'


        elif analysis == 2:
            matType2 = model.materials[mat_name].conductivity.type
            mp2 = model.materials[mat_name].conductivity.table[0]
            if matType2 == ISOTROPIC:
                writeFormat(file, 'ddd', [int(mat_id), 0, ntemp])
                writeFormat(file, 'EE', [float(temperature), float(density)])
                try:
                    mp2b = [mp2[0], 0.0 ]
                    writeFormat(file, 'EE', mp2b)
                except:
                    raise materialTypeError(
                        'Isotropic conductivity is not properly defined in material \'%s\' ' % mat_name)
                    print 'Isotropic conductivity is not defined properly in material \'%s\' ' % mat_name
            elif matType2 == ORTHOTROPIC:
                writeFormat(file, 'ddd', [int(mat_id), 1, ntemp])
                writeFormat(file, 'EE', [float(temperature), float(density)])
                try:
                    writeFormat(file, 'EEE', mp2[:3])
                except:
                    raise materialTypeError(
                        'Orthotropic conductivity is not properly defined in material \'%s\' ' % mat_name)
                    print 'Orthotropic conductivity is not defined properly in material \'%s\' ' % mat_name
            elif matType2 == ANISOTROPIC:
                writeFormat(file, 'ddd', [int(mat_id), 2, ntemp])
                writeFormat(file, 'EE', [float(temperature), float(density)])
                try:
                    writeFormat(file, 'E' * 6, mp2[:6])
                except:
                    raise materialTypeError(
                        'Anisotropic conductivity is not properly defined in material \'%s\' ' % mat_name)
                    print 'Anisotropic conductivity is not defined properly in material \'%s\' ' % mat_name
    return

def checkMaterials(matDict, analysis, model_name):

    for mat_name, mat_id in matDict.iteritems():
        
        model = mdb.models[model_name]
        if analysis != 2:
            matType = model.materials[mat_name].elastic.type
            mp = model.materials[mat_name].elastic.table[0]

            try :
                model.materials[mat_name].density
            except:
                print 'density is not defined in material "%s" ' % mat_name
                print 'default values density = 0.1, temperature = 0 will be used,'
                print 'which will not influence the results if analysis is not temperature related.'
                model.materials[mat_name].Density(table=((0.0, ), ))

            if analysis == 1:
                try :
                    model.materials[mat_name].specificHeat
                except:
                    raise ValueError( 'specificHeat is not defined in material \'%s\' ' % mat_name)
                #
                try :
                    model.materials[mat_name].expansion
                except:
                    raise ValueError( 'expansion is not defined in material \'%s\' ' % mat_name )
            if analysis == 3:
                try:
                    model.materials[mat_name].dielectric
                except:
                    raise ValueError('Dielectric material properties are not defined in material \'%s\' ' % mat_name)

                try:
                    model.materials[mat_name].piezoelectric
                except:
                    raise ValueError('Piezoelectric properties are not defined in material \'%s\' ' % mat_name)

        elif analysis == 2:
            matType2 = model.materials[mat_name].conductivity.type
            mp2 = model.materials[mat_name].conductivity.table[0]
            try:
                model.materials[mat_name].conductivity
            except:
                raise ValueError('Conductivity is not defined in material \'%s\' ' % mat_name)
    return
class materialTypeError(Exception):
    pass