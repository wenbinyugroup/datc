import io
import numpy as np
import os
from os.path import exists
import sys
import json

def GenYML_NAS_SA(bdffilename):

    if bdffilename.count('\\') == 0:
        bdf_name = bdffilename
    else:
        bdf_name = bdffilename.split("\\")[-1]

    ##### read lamina properties

    lamina = bdf_name + "LaminaProp.txt"

    with open(lamina) as file1:
        lines1 = file1.readlines()

    #### order of the lamina property in the LP : E11 E22 E33 nu12 nu23 nu31 G12 G23 G31
    LP = []
    for i in range(len(lines1)):
        LP.append(float(lines1[i].split("\n")[0]))

    #### reorder of the lamina property in the LaminaProp : E11 E22 E33 G12 G13 G23 nu12 nu13 nu23 (Swiftcomp can take this format)
    # nu13 = nu31*E11/E33
    la = np.zeros(len(LP))

    la[0] = LP[0]
    la[1] = LP[1]
    la[2] = LP[2]
    la[3] = LP[6]
    la[4] = LP[8]
    la[5] = LP[7]
    la[6] = LP[3]
    la[7] = round(LP[5] * LP[0] / LP[2], 5)
    la[8] = LP[4]

    # ##### read thickness
    #
    # thickness = bdf_name + "Thickness.txt"
    #
    # with open(thickness) as file2:
    #     lines2 = file2.readlines()
    #
    # thick = float(lines2[0])
    ##### read lower bound, upper bound and division

    # lud = "LUD.txt"
    lud = bdf_name + "FiberPath_PS.txt"

    with open(lud) as file3:
        lines3 = file3.readlines()

    count = 0
    for k in range(len(lines3)):
        if lines3[k] != '\n':
            count += 1
        else:
            break

    nv = int(count / 5)

    lyr_lud = {}
    var_name = {}
    for i in range(nv):
        lyr_lud[lines3[5*i].split('\n')[0]+lines3[5*i+1].split('\n')[0]] = [lines3[5*i+1].split('\n')[0], lines3[5*i+2].split('\n')[0], lines3[5*i+3].split('\n')[0], lines3[5*i+4].split('\n')[0]]
        var_name[lines3[5*i+1].split('\n')[0]] = lines3[5*i].split('\n')[0]+lines3[5*i+1].split('\n')[0]


    #
    # get the initial value of the design variables

    AllIV = "DesignVariable_fp.txt"
    with open(AllIV) as file6:
        lines6 = file6.readlines()
    count2 = 0
    for k in range(len(lines6)):
        if lines6[k] != '\n':
            count2 += 1
        else:
            break

    niv = int(count2 / 3)

    IV = {}
    for i in range(niv):
        IV[lines6[3*i].split('\n')[0]+lines6[3*i+1].split('\n')[0]] = lines6[3*i+2].split('\n')[0]


    # initial values v1 v2 ... v9 v10
    # IVfile = cwd_nas + "\\" + oname + "InitialValues.txt"
    # IVfile = bdf_name + "InitialValues.txt"
    #
    # with open(IVfile) as file7:
    #     lines7 = file7.readlines()
    #
    # # if lines12[0] != '\n':
    # NumIV = len(lines7)
    #
    # IV = []
    # IV_name = []
    #
    # for i in range(NumIV):
    #     IV.append(lines7[i].split("\n")[0])
    #     exec(f'v{i + 1} = IV[i]')
    #     IV_name.append(f'v{i+1}')

    ########################### code used to generate the differnt layer information in the vs_design.json file


    funcname_eqn = bdf_name + "all_funcname_eqn.txt"

    with open(funcname_eqn) as file8:
        lines8 = file8.readlines()
    count1 = 0
    for k in range(len(lines8)):
        if lines8[k] != '\n':
            count1 += 1
        else:
            break
    dictallFiberA = {}
    dictallThick = {}
    dictallMatname = {}
    Allfuncname = []

    for i in range(int(count1 / 4)):
        if lines8[i] != '\n':
            dictallFiberA[lines8[i * 4].split('\n')[0]] = lines8[i * 4 + 1].split('\n')[0]
            dictallThick[lines8[i * 4].split('\n')[0]] = lines8[i * 4 + 2].split('\n')[0]
            dictallMatname[lines8[i * 4].split('\n')[0]] = lines8[i * 4 + 3].split('\n')[0]
            Allfuncname.append(lines8[i * 4].split('\n')[0])

    ##### read scripts functions

    scriptinfo = bdf_name + "all_funcScripts.txt"

    with open(scriptinfo) as file9:
        lines9 = file9.readlines()

    lines9new = []

    for j in range(len(lines9)):
        if lines9[j] != '\n' and lines9[j] != '0\n' and lines9[j] != '0':
            # lines2[j] = lines2[j].split('\n')[0]
            lines9new.append(lines9[j].split('\n')[0])


    dict2 = {}

    for h in range(int(len(lines9new) / 6)):
        if lines9new[h] != '\n':
            dict2[lines9new[6 * h]] = [lines9new[6 * h + 1], lines9new[6 * h + 2], lines9new[6 * h + 3], lines9new[6 * h + 4],
                                    lines9new[6 * h + 5]]



    ##### read layup information
    layup = bdf_name + "layup.txt"

    with open(layup) as file10:
        lines10 = file10.readlines()

    layupinfo = lines10[0].split('\n')[0].replace("[", "").replace("]s", "").split('/')

    # layID = []
    allfuncname = []
    for kk in range(len(layupinfo)):
        allfuncname.append(dictallFiberA[layupinfo[kk]])
        # layID.append('l' + str(kk + 1))
        # layID.append(Allfuncname[layupinfo[kk]])

    # dict1 = {}
    #
    # for k in allfuncname:
    #     dict1[k] = dictallFiberA[k]

    # count number of v1, v2, v3

    ##### read steps information
    st = bdf_name + "steps.txt"

    with open(st) as file11:
        lines11 = file11.readlines()

    nas_name = lines11[0].strip()
    job_file = lines11[1].strip()
    post_script = lines11[2].strip()
    post_args = lines11[3].strip().split(',')
    pargs = []
    for ll in post_args:
        pargs.append(ll.strip())
    step_result_file = lines11[4].strip()

    ### find how many function and corresponding layer

    Alleqn_layer = {}

    for i, j in dictallFiberA.items():
        if '+' in j or '-' in j or '*' in j or '/' in j or 'script' in j:
            Alleqn_layer[i] = j



    def findV(iv, eq):
        countV = 0
        for i in iv:
            if i in eq:
                countV += 1
        return countV

    def findVARISindex(iv, eq):
        index_name = []
        for i in range(len(iv)):
            if iv[i] in eq:
                index_name.append(i)
        return index_name

    global name, vals, namenew

    
    newSF = 'vs_design_ps.yml'

    with open(newSF, 'w') as fnew:
        fnew.write('version: "0.9"\n')
        fnew.write('\n')
        fnew.write('setting:\n')
        fnew.write('  log_level_cmd: "info"\n')
        fnew.write('  log_level_file: "debug"\n')
        fnew.write('  log_file_name: "eval.log"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('structure:\n')
        fnew.write('  name: "square_plate"\n')
        fnew.write('  parameters:\n')
        for i, j in IV.items():
            fnew.write('    ' + i + ': ' + str(j) + '\n')
        fnew.write('  distributions:\n')
        # for i, j in Alleqn_layer.items():
        #     icount = 1
        #     fnew.write('    - name: a'+str(icount)+'\n')
        #     fnew.write('      function: f'+str(icount)+'\n')
        #     fnew.write('      coefficients:\n')
        #     fnew.write('        v1: l2v1\n')
        #     fnew.write('        v2: l2v2\n')
        #     icount += 1
        countaf = 0
        countf = 0
        for j in allfuncname:
            if '+' in j or '-' in j or '*' in j or '/' in j:
                countaf += 1
                countf += 1
                fnew.write('    - name: a' + str(countaf) + '\n')
                fnew.write('      function: f' + str(countf) + '\n')
                fnew.write('      coefficients:\n')
                fnew.write('        '+list(var_name.keys())[0]+': '+list(var_name.values())[0]+'\n')
                fnew.write('        ' + list(var_name.keys())[1] + ': ' + list(var_name.values())[1] + '\n')
            else:
                countaf += 1
        # fnew.write('    - name: a2\n')
        # fnew.write('      function: f1\n')
        # fnew.write('      coefficients:\n')
        # fnew.write('        v1: l1v1\n')
        # fnew.write('        v2: l1v2\n')
        fnew.write('  design:\n')
        fnew.write('    file: "'+ bdf_name + '"\n')
        fnew.write('    solver: "nastran"\n')
        fnew.write('    section_prop_file: "testshell.bdf"\n')
        fnew.write('    sg_assignment:\n')
        fnew.write('      all: "mainsg"\n')
        fnew.write('  sg:\n')
        fnew.write('    mainsg:\n')
        fnew.write('      base: "lv1_layup"\n')
        fnew.write('      model: "md2"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('function:\n')
        countfunc = 0
        for i in allfuncname:
            if '+' in i or '-' in i or '*' in i or '/' in i:
                countfunc += 1
                fnew.write('  - name: "f'+str(countfunc)+'"\n')
                fnew.write('    type: "expression"\n')
                fnew.write('    expression: "' + i + '"\n')
                fnew.write('    coefficients: ["' + list(var_name.keys())[0] + '", "' + list(var_name.keys())[1] + '"]\n')
        # fnew.write('  - name: "f1"\n')
        # fnew.write('    type: "expression"\n')
        # fnew.write('    expression: "'+dict1['l2']+'"\n')
        # fnew.write('    coefficients: ["' + IV_name[0] + '", "' + IV_name[1]+'"]\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('sg:\n')
        fnew.write('  - name: "lv1_layup"\n')
        fnew.write('    parameters:\n')
        counta = 0
        for j in allfuncname:
            counta += 1
            if '+' in j or '-' in j or '*' in j or '/' in j:
                fnew.write('      a'+ str(counta) +': 0\n')
            else:
                fnew.write('      a'+ str(counta) +': '+j+'\n')

        # fnew.write('      a1: 45\n')
        # fnew.write('      a2: 0\n')
        # fnew.write('      a3: 90\n')
        fnew.write('    design:\n')
        fnew.write('      dim: 1\n')
        fnew.write('      type: "descriptive"\n')
        fnew.write('      tool: "default"\n')
        fnew.write('      symmetry: 1\n')
        fnew.write('      layers:\n')
        for i in range(len(dictallFiberA)):
            fnew.write('        - material: "m1"\n')
            fnew.write('          ply_thickness: '+ dictallThick[list(dictallFiberA.keys())[i]] + '\n')
            fnew.write('          number_of_plies: 1\n')
            fnew.write('          in-plane_orientation: a'+ str(i+1) +'\n')
        fnew.write('\n')
        fnew.write('    model:\n')
        fnew.write('      md2:\n')
        fnew.write('        tool: "swiftcomp"\n')
        fnew.write('        version: "2.2"\n')
        fnew.write('        mesh_size: -1\n')
        fnew.write('\n')
        fnew.write('  - name: "m1"\n')
        fnew.write('    type: "material"\n')
        fnew.write('    model:\n')
        fnew.write('      md3:\n')
        fnew.write('        type: "engineering"\n')
        fnew.write('        density: 1.0\n')
        fnew.write('        elasticity:\n')
        fnew.write('          [\n')
        fnew.write('            '+str(la[0]) + ', ' + str(la[1]) + ', ' + str(la[2]) + ',\n')
        fnew.write('            '+str(la[3]) + ', ' + str(la[4]) + ', ' + str(la[5]) + ',\n')
        fnew.write('            '+str(la[6]) + ', ' + str(la[7]) + ', ' + str(la[8]) + '\n')
        fnew.write('          ]\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('analysis:\n')
        fnew.write('  steps:\n')
        fnew.write('    - name: "homogenization"\n')
        fnew.write('      type: "sg"\n')
        fnew.write('      analysis: "h"\n')
        fnew.write('    - name: "structural analysis"\n')
        fnew.write('      type: "nastran"\n')
        fnew.write('      job_file: "' + bdf_name + '"\n')
        fnew.write('      setting:\n')
        fnew.write('        timeout: 300\n')
        fnew.write('      args:\n')
        fnew.write('        - "interactive"\n')
        fnew.write('      post_process:\n')
        fnew.write('        - script: "' + post_script + '"\n')
        fnew.write('          args: [\n')
        fnew.write('            "' + pargs[0] + '",\n')
        fnew.write('            "' + pargs[1] + '", "' + pargs[2] + '",\n')
        # fnew.write('            "-n", "center",\n')
        fnew.write('            "' + pargs[3] + '", "' + pargs[4] + '",\n')
        fnew.write('            "' + pargs[5] + '", "' + pargs[6] + '"\n')
        fnew.write('          ]\n')
        fnew.write('      step_result_file: "' + pargs[6] + '"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('study:\n')
        fnew.write('  method:\n')
        fnew.write('    multidim_parameter_study:\n')
        fnew.write('      partitions: [' + list(lyr_lud.values())[0][-1] + ', ' + list(lyr_lud.values())[1][-1] + ']\n')
        fnew.write('  variables:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    list:\n')
        for j in range(len(lyr_lud)):
            fnew.write('      - name: "'+ list(lyr_lud.keys())[j] +'"\n')
            fnew.write('        type: "continuous"\n')
            fnew.write('        bounds: [' + list(lyr_lud.values())[j][1] + ', ' + list(lyr_lud.values())[j][2] + ']\n')
        fnew.write('  responses:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    response_functions:\n')
        fnew.write('      - descriptor: "u1"\n')
        fnew.write('  interface:\n')
        fnew.write('    fork:\n')
        fnew.write('      parameters_file: "params.in"\n')
        fnew.write('      results_file: "results.out"\n')
        fnew.write('      file_save: on\n')
        fnew.write('      work_directory:\n')
        fnew.write('        named: "evals/eval"\n')
        fnew.write('        directory_tag: on\n')
        fnew.write('        directory_save: on\n')
        fnew.write('    required_files: ["model/*", ' + bdf_name + ']\n')

        fnew.close()


def GenYML_ABQ_SA(inpfilename):

    # inpfilename = 'plate400s4r.inp'

    if inpfilename.count('/') == 0:
        onlyinpname = inpfilename.split('.')[0]
        inp_name = inpfilename
    else:
        onlyinpname = inpfilename.split("/")[-1].split('.')[0]
        inp_name = inpfilename.split("/")[-1]

    ##### read lamina properties

    lamina = inp_name + "LaminaProp_adv_SA.txt"

    with open(lamina) as file1:
        lines1 = file1.readlines()

    #### order of the lamina property in the LP : E11 E22 E33 nu12 nu23 nu31 G12 G23 G31
    LP = []
    for i in range(len(lines1)):
        LP.append(float(lines1[i].split("\n")[0]))

    #### reorder of the lamina property in the LaminaProp : E11 E22 E33 G12 G13 G23 nu12 nu13 nu23 (Swiftcomp can take this format)
    # nu13 = nu31*E11/E33
    la = np.zeros(len(LP))

    la[0] = LP[0]
    la[1] = LP[1]
    la[2] = LP[2]
    la[3] = LP[6]
    la[4] = LP[7]
    la[5] = LP[8]
    la[6] = LP[3]
    la[7] = LP[4]
    la[8] = LP[5]

    ##### read thickness

    layupinfo = inp_name + "LayupandLayerinfo.txt"

    with open(layupinfo) as file2:
        lines2 = file2.readlines()

    layup = lines2[0].split('\n')[0].replace('[', '').replace(']', '').split('/')

    layup_info = {}
    for i in range(len(layup)):
        layup_info[lines2[4*i+1].split('\n')[0]] = {'type': lines2[4*i+2].split('\n')[0], 'ply_thickness': lines2[4*i+3].split('\n')[0], 'orientation': lines2[4*i+4].split('\n')[0].replace('[', '').replace(']', '').replace("'",'')}


    ##### initial values v1 v2 ... v9 v10
    IVfile = inp_name + "DesignVariable_ply.txt"

    with open(IVfile) as file7:
        lines7 = file7.readlines()

    # if lines12[0] != '\n':
    iv_list = lines7[0].split("\n")[0].replace('[', '').replace(']', '').replace("'", '').split(',')
    NumIV = len(iv_list)

    IV = []
    IV_name = {}
    IV_name_removeDuplicate = []

    for i in range(int(NumIV/3)):
        IV.append([iv_list[3*i].strip(),iv_list[3*i+1].strip(),iv_list[3*i+2].strip()])
        IV_name_removeDuplicate.append(iv_list[3*i+1].strip())
        IV_name[iv_list[3*i].strip()+iv_list[3*i+1].strip()] = {'var name': iv_list[3*i+1].strip(), 'var value': iv_list[3*i+2].strip()}

    IV_name_removeDuplicate = list(set(IV_name_removeDuplicate)).sort()

        # exec(f'v{i + 1} = IV[i]')
        # IV_name.append(f'v{i + 1}')
    #
    # ########################### code used to generate the differnt layer information in the vs_design.json file

    # funcname_eqn = inp_name + "all_funcname_eqn.txt"
    #
    # if os.path.getsize(funcname_eqn) == 0:
    #     print("The file is empty.")
    # else:
    #     with open(funcname_eqn) as file8:
    #         lines8 = file8.readlines()
    #     count1 = 0
    #     for k in range(len(lines8)):
    #         if lines8[k] != '\n':
    #             count1 += 1
    #         else:
    #             break
    #     dictall = {}
    #     Allfuncname = []
    #     funcname = {}
    #     for i in range(int(count1 / 2)):
    #         if lines8[i] != '\n':
    #             dictall[lines8[i * 2].split('\n')[0]] = lines8[i * 2 + 1].split('\n')[0]
    #             Allfuncname.append(lines8[i * 2].split('\n')[0])
    #             funcname[str(i + 1)] = lines8[i * 2].split('\n')[0]


    ##### read scripts functions

    scriptinfo = inp_name + "all_funcScripts.txt"

    if os.path.getsize(scriptinfo) == 0:
        print("This is one-line expression problem.")
    else:
        with open(scriptinfo) as file9:
            lines9 = file9.readlines()

        lines9new = []

        for j in range(len(lines9)):
            if lines9[j] != '\n' and lines9[j] != '0\n' and lines9[j] != '0':
                # lines2[j] = lines2[j].split('\n')[0]
                lines9new.append(lines9[j].split('\n')[0])

        dict2 = {}

        for h in range(int(len(lines9new) / 6)):
            if lines9new[h] != '\n':
                dict2[lines9new[6 * h]] = [lines9new[6 * h + 1], lines9new[6 * h + 2], lines9new[6 * h + 3],
                                           lines9new[6 * h + 4],
                                           lines9new[6 * h + 5]]


    newSF = 'vs_design_sa.yml'

    with open(newSF, 'w') as fnew:
        fnew.write('version: "0.9"\n')
        fnew.write('\n')
        # fnew.write('setting:\n')
        # fnew.write('  log_level_cmd: "info"\n')
        # fnew.write('  log_level_file: "debug"\n')
        # fnew.write('  log_file_name: "eval.log"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('structure:\n')
        fnew.write('  name: "square_plate"\n')
        fnew.write('  type: null\n')
        fnew.write('  parameter:\n')
        for i, j in IV_name.items():
            fnew.write('    '+ i +': ' + '0' + '\n')

        fnew.write('  distribution:\n')
        id_layup_expressin = []
        for i in range(len(layup)):
            if layup_info[layup[i]]['type'] == 'expression':
                id_layup_expressin.append(i)
        for i in range(len(id_layup_expressin)):
            fnew.write('    - name: a'+str(id_layup_expressin[i]+1)+'\n')
            fnew.write('      function: f'+str(id_layup_expressin[i])+'\n')
            fnew.write('      coefficients:\n')
            for j, k in IV_name.items():
                if layup[id_layup_expressin[i]] in j:
                    fnew.write('        '+k['var name']+': '+ j +'\n')
        fnew.write('  design:\n')
        fnew.write('    file: "plate400s4r.inp"\n')
        fnew.write('    solver: "abaqus"\n')
        fnew.write('    section_prop_file: "shellsections.inp"\n')
        # fnew.write('    file: "' + bdf_name + '"\n')
        # fnew.write('    solver: "nastran"\n')
        # fnew.write('   section_prop_file: "shellsections.bdf"\n')
        fnew.write('    sg_assignment:\n')
        fnew.write('      all: "mainsg"\n')
        fnew.write('  sg:\n')
        fnew.write('    mainsg:\n')
        fnew.write('      base: "lv1_layup"\n')
        fnew.write('      model: "md2"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('function:\n')
        for i in range(len(id_layup_expressin)):
            fnew.write('  - name: "f'+str(id_layup_expressin[i])+'"\n')
            fnew.write('    type: "expression"\n')
            fnew.write('    expression: "' + layup_info[layup[id_layup_expressin[i]]]['orientation'] + '"\n')
            var_in_eqn = []
            for j, k in IV_name.items():
                if layup[id_layup_expressin[i]] in j:
                    var_in_eqn.append(k['var name'])
                    # fnew.write('    coefficients: ["' + IV_name[0] + '", "' + IV_name[1] + '"]\n')
            fnew.write('    coefficients: ' + json.dumps(var_in_eqn) + '\n')

        fnew.write('\n')
        fnew.write('\n')
        fnew.write('sg:\n')
        fnew.write('  - name: "lv1_layup"\n')
        fnew.write('    parameters:\n')
        for i in range(len(layup)):
            if layup_info[layup[i]]['type'] == 'expression':
                fnew.write('      a'+str(i+1)+': 0\n')
            else:
                fnew.write('      a' + str(i + 1) + ': '+layup_info[layup[i]]['orientation']+'\n')
        fnew.write('    design:\n')
        fnew.write('      dim: 1\n')
        fnew.write('      symmetry: 1\n')
        fnew.write('      layers:\n')
        for i in range(len(layup)):
            fnew.write('        - material: "m1"\n')
            fnew.write('          ply_thickness: ' + str(layup_info[layup[i]]['ply_thickness']) + '\n')
            fnew.write('          number_of_plies: 1\n')
            fnew.write('          in-plane_orientation: a' + str(i + 1) + '\n')
        fnew.write('\n')
        fnew.write('    model:\n')
        fnew.write('      md2:\n')
        fnew.write('        tool: "swiftcomp"\n')
        fnew.write('        version: "2.2"\n')
        fnew.write('        mesh_size: -1\n')
        fnew.write('\n')
        fnew.write('  - name: "m1"\n')
        fnew.write('    type: "material"\n')
        fnew.write('    model:\n')
        fnew.write('      md3:\n')
        fnew.write('        type: "engineering"\n')
        fnew.write('        density: 1.0\n')
        fnew.write('        elasticity:\n')
        fnew.write('          [\n')
        fnew.write('            ' + str(la[0]) + ', ' + str(la[1]) + ', ' + str(la[2]) + ',\n')
        fnew.write('            ' + str(la[3]) + ', ' + str(la[4]) + ', ' + str(la[5]) + ',\n')
        fnew.write('            ' + str(la[6]) + ', ' + str(la[7]) + ', ' + str(la[8]) + '\n')
        fnew.write('          ]\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('analysis:\n')
        fnew.write('  steps:\n')
        fnew.write('    - name: "homogenization"\n')
        fnew.write('      type: "sg"\n')
        fnew.write('      analysis: "h"\n')
        fnew.write('      setting:\n')
        fnew.write('        solver: "swiftcomp"\n')
        fnew.write('    - name: "structural analysis"\n')
        fnew.write('      type: "abaqus"\n')
        fnew.write('      job_file: "'+inp_name+'"\n')
        # fnew.write('      job_file: "' + bdf_name + '"\n')
        fnew.write('      setting:\n')
        fnew.write('        timeout: 300\n')
        fnew.write('      args:\n')
        fnew.write('        - "interactive"\n')
        fnew.write('      post_process:\n')
        # fnew.write('        - script: "' + post_script + '"\n')
        fnew.write('        - script: "abq_get_result.py"\n')
        fnew.write('          args: \n')
        fnew.write('            - "'+inp_name.split('.')[0]+'.odb"\n')
        fnew.write('            - "abq_result.dat"\n')
        # fnew.write('      step_result_file: "' + pargs[6] + '"\n')
        fnew.write('      step_result_file: "abq_result.dat"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('study:\n')
        fnew.write('  method:\n')
        fnew.write('    list_parameter_study:\n')
        ps_var_iv = []
        for i, j in IV_name.items():
            ps_var_iv.append(float(j['var value']))
        fnew.write('      list_of_points: ' + str(ps_var_iv) + '\n')
        fnew.write('  variables:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    list:\n')
        for i, j in IV_name.items():
            fnew.write('      - name: "' + i + '"\n')
            fnew.write('        type: "continuous"\n')
            fnew.write('        bounds: [' + str(0) + ', ' + str(90) + ']\n')
        fnew.write('  responses:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    response_functions:\n')
        fnew.write('      - descriptor: "eig1"\n')
        fnew.write('  interface:\n')
        fnew.write('    fork:\n')
        fnew.write('      parameters_file: "params.in"\n')
        fnew.write('      results_file: "results.out"\n')
        fnew.write('      file_save: on\n')
        fnew.write('      work_directory:\n')
        fnew.write('        named: "evals/eval"\n')
        fnew.write('        directory_tag: on\n')
        fnew.write('        directory_save: on\n')
        fnew.write('    required_files: ["model/*", '+ inp_name +']\n')

        fnew.close()

def GenYML_ABQ_PS(inpfilename):

    # inpfilename = 'plate400s4r.inp'

    if inpfilename.count('/') == 0:
        onlyinpname = inpfilename.split('.')[0]
        inp_name = inpfilename
    else:
        onlyinpname = inpfilename.split("/")[-1].split('.')[0]
        inp_name = inpfilename.split("/")[-1]

    ##### read lamina properties

    lamina = inp_name + "LaminaProp_adv_SA.txt"

    with open(lamina) as file1:
        lines1 = file1.readlines()

    #### order of the lamina property in the LP : E11 E22 E33 nu12 nu23 nu31 G12 G23 G31
    LP = []
    for i in range(len(lines1)):
        LP.append(float(lines1[i].split("\n")[0]))

    #### reorder of the lamina property in the LaminaProp : E11 E22 E33 G12 G13 G23 nu12 nu13 nu23 (Swiftcomp can take this format)
    # nu13 = nu31*E11/E33
    la = np.zeros(len(LP))

    la[0] = LP[0]
    la[1] = LP[1]
    la[2] = LP[2]
    la[3] = LP[6]
    la[4] = LP[7]
    la[5] = LP[8]
    la[6] = LP[3]
    la[7] = LP[4]
    la[8] = LP[5]

    ##### read thickness

    layupinfo = inp_name + "LayupandLayerinfo.txt"

    with open(layupinfo) as file2:
        lines2 = file2.readlines()

    layup = lines2[0].split('\n')[0].replace('[', '').replace(']', '').split('/')

    layup_info = {}
    for i in range(len(layup)):
        layup_info[lines2[4*i+1].split('\n')[0]] = {'type': lines2[4*i+2].split('\n')[0], 'ply_thickness': lines2[4*i+3].split('\n')[0], 'orientation': lines2[4*i+4].split('\n')[0].replace('[', '').replace(']', '').replace("'",'')}

    ##### read abaqus arguments

    argsinfo = inp_name + "args.txt"

    with open(argsinfo) as file3:
        lines3 = file3.readlines()

    abqname = lines3[0].split('\n')[0]

    abqscipt = lines3[1].split('\n')[0]

    abqargs = []
    for i in range(len(lines3[2].split('\n')[0].replace('[','').replace(']','').split(','))):
        abqargs.append(lines3[2].split('\n')[0].replace('[','').replace(']','').split(',')[i].strip()[1:-1])

    abqStep_result = lines3[-1].split('\n')[0]




    ##### initial values v1 v2 ... v9 v10
    IVfile = inp_name + "DesignVariable_ply.txt"

    with open(IVfile) as file7:
        lines7 = file7.readlines()

    # if lines12[0] != '\n':
    iv_list = lines7[0].split("\n")[0].replace('[', '').replace(']', '').replace("'", '').split(',')
    NumIV = len(iv_list)

    IV = []
    IV_name = {}
    IV_name_removeDuplicate = []

    for i in range(int(NumIV/3)):
        IV.append([iv_list[3*i].strip(),iv_list[3*i+1].strip(),iv_list[3*i+2].strip()])
        IV_name_removeDuplicate.append(iv_list[3*i+1].strip())
        IV_name[iv_list[3*i].strip()+iv_list[3*i+1].strip()] = {'var name': iv_list[3*i+1].strip(), 'var value': iv_list[3*i+2].strip()}

    IV_name_removeDuplicate = list(set(IV_name_removeDuplicate)).sort()

    ##### read scripts functions

    scriptinfo = inp_name + "all_funcScripts.txt"

    if os.path.getsize(scriptinfo) == 0:
        print("This is one-line expression problem.")
    else:
        with open(scriptinfo) as file9:
            lines9 = file9.readlines()

        lines9new = []

        for j in range(len(lines9)):
            if lines9[j] != '\n' and lines9[j] != '0\n' and lines9[j] != '0':
                # lines2[j] = lines2[j].split('\n')[0]
                lines9new.append(lines9[j].split('\n')[0])

        dict2 = {}

        for h in range(int(len(lines9new) / 6)):
            if lines9new[h] != '\n':
                dict2[lines9new[6 * h]] = [lines9new[6 * h + 1], lines9new[6 * h + 2], lines9new[6 * h + 3],
                                           lines9new[6 * h + 4],
                                           lines9new[6 * h + 5]]

    ##### read lower, upper and partition information

    lupinfo = inp_name + "LUP.txt"

    with open(lupinfo) as file4:
        lines4 = file4.readlines()

    lup = []
    for i in range(len(lines4[0].split('\n')[0].replace('[', '').replace(']', '').split(','))):
        lup.append(lines4[0].split('\n')[0].replace('[', '').replace(']', '').split(',')[i].strip()[1:-1])

    #### information in lu_info is [initial value, lower bound, upper bound, partition]
    lu_info = {}
    for j in range(int(len(lup)/4)):
        lu_info[lup[4*j]+lup[4*j+1]] = [IV_name[lup[4*j]+lup[4*j+1]]['var value'], lup[4*j+2], lup[4*j+3], lines4[-1].split('\n')[0].replace('[', '').replace(']', '').split(',')[j].strip()]



    #### get the layer name that use expression

    layup_with_vars = []
    for i, j in layup_info.items():
        if j['type'] == 'expression':
            layup_with_vars.append(i)

    #### get the layer name with corresponding variables
    layer_with_vars_update = {}

    for k in layup_with_vars:
        varinlayer = []
        for h in IV:
            if k == h[0]:
                varinlayer.append(h[1])
        layer_with_vars_update[k] = varinlayer

    ### get the name with the same dictionary value and store it in (flipped)
    flipped = {}
    for key, value in layer_with_vars_update.items():
        if str(value) not in flipped:
            flipped[str(value)] = [key]
        else:
            flipped[str(value)].append(key)

    final_var_names = []

    for i, j in flipped.items():
        if len(j) == 1:
            for k in layer_with_vars_update[j[0]]:
                final_var_names.append(j[0]+k)
        else:
            for h in layer_with_vars_update[j[0]]:
                final_var_names.append(h)

    final_var_names_with_value = {}
    for i in final_var_names:
        for j, k in lu_info.items():
            if i in j:
                final_var_names_with_value[i] = k

    partition_info = []

    for i, j in final_var_names_with_value.items():
        partition_info.append(int(j[-1]))


    newSF = 'vs_design_ps.yml'

    with open(newSF, 'w') as fnew:
        fnew.write('version: "0.9"\n')
        fnew.write('\n')
        # fnew.write('setting:\n')
        # fnew.write('  log_level_cmd: "info"\n')
        # fnew.write('  log_level_file: "debug"\n')
        # fnew.write('  log_file_name: "eval.log"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('structure:\n')
        fnew.write('  name: "square_plate"\n')
        fnew.write('  type: null\n')
        fnew.write('  parameter:\n')
        for i, j in final_var_names_with_value.items():
            fnew.write('    ' + i + ': ' + j[0] + '\n')

        fnew.write('  distribution:\n')
        id_layup_expressin = []
        for i in range(len(layup)):
            if layup_info[layup[i]]['type'] == 'expression':
                id_layup_expressin.append(i)
        for i in range(len(id_layup_expressin)):
            fnew.write('    - name: a'+str(id_layup_expressin[i]+1)+'\n')
            fnew.write('      function: f'+str(id_layup_expressin[i])+'\n')
            fnew.write('      coefficients:\n')
            for j, k in IV_name.items():
                if layup[id_layup_expressin[i]] in j:
                    fnew.write('        '+k['var name']+': '+ j +'\n')
        fnew.write('  design:\n')
        fnew.write('    file: "'+inpfilename+'"\n')
        fnew.write('    solver: "abaqus"\n')
        fnew.write('    section_prop_file: "shellsections.inp"\n')
        # fnew.write('    file: "' + bdf_name + '"\n')
        # fnew.write('    solver: "nastran"\n')
        # fnew.write('   section_prop_file: "shellsections.bdf"\n')
        fnew.write('    sg_assignment:\n')
        fnew.write('      all: "mainsg"\n')
        fnew.write('  sg:\n')
        fnew.write('    mainsg:\n')
        fnew.write('      base: "lv1_layup"\n')
        fnew.write('      model: "md2"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('function:\n')
        for i in range(len(id_layup_expressin)):
            fnew.write('  - name: "f'+str(id_layup_expressin[i])+'"\n')
            fnew.write('    type: "expression"\n')
            fnew.write('    expression: "' + layup_info[layup[id_layup_expressin[i]]]['orientation'] + '"\n')
            var_in_eqn = []
            for j, k in IV_name.items():
                if layup[id_layup_expressin[i]] in j:
                    var_in_eqn.append(k['var name'])
                    # fnew.write('    coefficients: ["' + IV_name[0] + '", "' + IV_name[1] + '"]\n')
            fnew.write('    coefficients: ' + json.dumps(var_in_eqn) + '\n')

        fnew.write('\n')
        fnew.write('\n')
        fnew.write('sg:\n')
        fnew.write('  - name: "lv1_layup"\n')
        fnew.write('    parameters:\n')
        for i in range(len(layup)):
            if layup_info[layup[i]]['type'] == 'expression':
                fnew.write('      a'+str(i+1)+': 0\n')
            else:
                fnew.write('      a' + str(i + 1) + ': '+layup_info[layup[i]]['orientation']+'\n')
        fnew.write('    design:\n')
        fnew.write('      dim: 1\n')
        fnew.write('      symmetry: 1\n')
        fnew.write('      layers:\n')
        for i in range(len(layup)):
            fnew.write('        - material: "m1"\n')
            fnew.write('          ply_thickness: ' + str(layup_info[layup[i]]['ply_thickness']) + '\n')
            fnew.write('          number_of_plies: 1\n')
            fnew.write('          in-plane_orientation: a' + str(i + 1) + '\n')
        fnew.write('\n')
        fnew.write('    model:\n')
        fnew.write('      md2:\n')
        fnew.write('        tool: "swiftcomp"\n')
        fnew.write('        version: "2.2"\n')
        fnew.write('        mesh_size: -1\n')
        fnew.write('\n')
        fnew.write('  - name: "m1"\n')
        fnew.write('    type: "material"\n')
        fnew.write('    model:\n')
        fnew.write('      md3:\n')
        fnew.write('        type: "engineering"\n')
        fnew.write('        density: 1.0\n')
        fnew.write('        elasticity:\n')
        fnew.write('          [\n')
        fnew.write('            ' + str(la[0]) + ', ' + str(la[1]) + ', ' + str(la[2]) + ',\n')
        fnew.write('            ' + str(la[3]) + ', ' + str(la[4]) + ', ' + str(la[5]) + ',\n')
        fnew.write('            ' + str(la[6]) + ', ' + str(la[7]) + ', ' + str(la[8]) + '\n')
        fnew.write('          ]\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('analysis:\n')
        fnew.write('  steps:\n')
        fnew.write('    - name: "homogenization"\n')
        fnew.write('      type: "sg"\n')
        fnew.write('      analysis: "h"\n')
        fnew.write('      setting:\n')
        fnew.write('        solver: "swiftcomp"\n')
        fnew.write('    - name: "'+abqname+'"\n')
        fnew.write('      type: "abaqus"\n')
        fnew.write('      job_file: "'+inp_name+'"\n')
        # fnew.write('      job_file: "' + bdf_name + '"\n')
        fnew.write('      setting:\n')
        fnew.write('        timeout: 600\n')
        fnew.write('      args:\n')
        fnew.write('        - "interactive"\n')
        fnew.write('      post_process:\n')
        # fnew.write('        - script: "' + post_script + '"\n')
        fnew.write('        - script: "'+abqscipt+'"\n')
        fnew.write('          args: \n')
        for i in abqargs:
            fnew.write('            - "'+i+'"\n')
        fnew.write('      step_result_file: "'+abqStep_result+'"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('study:\n')
        fnew.write('  method:\n')
        fnew.write('    multidim_parameter_study:\n')
        fnew.write('      partitions: ' + str(partition_info) + '\n')
        fnew.write('  variables:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    list:\n')
        for i, j in final_var_names_with_value.items():
            fnew.write('      - name: "' + i + '"\n')
            fnew.write('        type: "continuous"\n')
            fnew.write('        bounds: [' + j[1] + ', ' + j[2] + ']\n')
        fnew.write('  responses:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    response_functions:\n')
        if 'buckling' in abqname:
            fnew.write('      - descriptor: "eig1"\n')
        else:
            fnew.write('      - descriptor: "u"\n')
        fnew.write('  interface:\n')
        fnew.write('    fork:\n')
        fnew.write('      parameters_file: "params.in"\n')
        fnew.write('      results_file: "results.out"\n')
        fnew.write('      file_save: on\n')
        fnew.write('      work_directory:\n')
        fnew.write('        named: "evals/eval"\n')
        fnew.write('        directory_tag: on\n')
        fnew.write('        directory_save: on\n')
        fnew.write('    required_files: ["model/*", ' + inp_name + ']\n')
        fnew.close()


def GenYML_ABQ_PS_lhs(inpfilename):

    # inpfilename = 'plate400s4r.inp'

    if inpfilename.count('/') == 0:
        onlyinpname = inpfilename.split('.')[0]
        inp_name = inpfilename
    else:
        onlyinpname = inpfilename.split("/")[-1].split('.')[0]
        inp_name = inpfilename.split("/")[-1]

    ##### read lamina properties

    lamina = inp_name + "LaminaProp_adv_SA.txt"

    with open(lamina) as file1:
        lines1 = file1.readlines()

    #### order of the lamina property in the LP : E11 E22 E33 nu12 nu23 nu31 G12 G23 G31
    LP = []
    for i in range(len(lines1)):
        LP.append(float(lines1[i].split("\n")[0]))

    #### reorder of the lamina property in the LaminaProp : E11 E22 E33 G12 G13 G23 nu12 nu13 nu23 (Swiftcomp can take this format)
    # nu13 = nu31*E11/E33
    la = np.zeros(len(LP))

    la[0] = LP[0]
    la[1] = LP[1]
    la[2] = LP[2]
    la[3] = LP[6]
    la[4] = LP[7]
    la[5] = LP[8]
    la[6] = LP[3]
    la[7] = LP[4]
    la[8] = LP[5]

    ##### read thickness

    layupinfo = inp_name + "LayupandLayerinfo.txt"

    with open(layupinfo) as file2:
        lines2 = file2.readlines()

    layup = lines2[0].split('\n')[0].replace('[', '').replace(']', '').split('/')

    layup_info = {}
    for i in range(len(layup)):
        layup_info[lines2[4*i+1].split('\n')[0]] = {'type': lines2[4*i+2].split('\n')[0], 'ply_thickness': lines2[4*i+3].split('\n')[0], 'orientation': lines2[4*i+4].split('\n')[0].replace('[', '').replace(']', '').replace("'",'')}

    ##### read abaqus arguments

    argsinfo = inp_name + "args.txt"

    with open(argsinfo) as file3:
        lines3 = file3.readlines()

    abqname = lines3[0].split('\n')[0]

    abqscipt = lines3[1].split('\n')[0]

    abqargs = []
    for i in range(len(lines3[2].split('\n')[0].replace('[','').replace(']','').split(','))):
        abqargs.append(lines3[2].split('\n')[0].replace('[','').replace(']','').split(',')[i].strip()[1:-1])

    abqStep_result = lines3[-1].split('\n')[0]




    ##### initial values v1 v2 ... v9 v10
    IVfile = inp_name + "DesignVariable_ply.txt"

    with open(IVfile) as file7:
        lines7 = file7.readlines()

    # if lines12[0] != '\n':
    iv_list = lines7[0].split("\n")[0].replace('[', '').replace(']', '').replace("'", '').split(',')
    NumIV = len(iv_list)

    IV = []
    IV_name = {}
    IV_name_removeDuplicate = []

    for i in range(int(NumIV/3)):
        IV.append([iv_list[3*i].strip(),iv_list[3*i+1].strip(),iv_list[3*i+2].strip()])
        IV_name_removeDuplicate.append(iv_list[3*i+1].strip())
        IV_name[iv_list[3*i].strip()+iv_list[3*i+1].strip()] = {'var name': iv_list[3*i+1].strip(), 'var value': iv_list[3*i+2].strip()}

    IV_name_removeDuplicate = list(set(IV_name_removeDuplicate)).sort()

    ##### read scripts functions

    scriptinfo = inp_name + "all_funcScripts.txt"

    if os.path.getsize(scriptinfo) == 0:
        print("This is one-line expression problem.")
    else:
        with open(scriptinfo) as file9:
            lines9 = file9.readlines()

        lines9new = []

        for j in range(len(lines9)):
            if lines9[j] != '\n' and lines9[j] != '0\n' and lines9[j] != '0':
                # lines2[j] = lines2[j].split('\n')[0]
                lines9new.append(lines9[j].split('\n')[0])

        dict2 = {}

        for h in range(int(len(lines9new) / 6)):
            if lines9new[h] != '\n':
                dict2[lines9new[6 * h]] = [lines9new[6 * h + 1], lines9new[6 * h + 2], lines9new[6 * h + 3],
                                           lines9new[6 * h + 4],
                                           lines9new[6 * h + 5]]

    ##### read lower, upper and partition information

    lupinfo = inp_name + "LUP.txt"

    with open(lupinfo) as file4:
        lines4 = file4.readlines()

    lup = []
    for i in range(len(lines4[0].split('\n')[0].replace('[', '').replace(']', '').split(','))):
        lup.append(lines4[0].split('\n')[0].replace('[', '').replace(']', '').split(',')[i].strip()[1:-1])

    #### information in lu_info is [initial value, lower bound, upper bound, partition]
    lu_info = {}
    for j in range(int(len(lup)/4)):
        lu_info[lup[4*j]+lup[4*j+1]] = [IV_name[lup[4*j]+lup[4*j+1]]['var value'], lup[4*j+2], lup[4*j+3]]



    #### get the layer name that use expression

    layup_with_vars = []
    for i, j in layup_info.items():
        if j['type'] == 'expression':
            layup_with_vars.append(i)

    #### get the layer name with corresponding variables
    layer_with_vars_update = {}

    for k in layup_with_vars:
        varinlayer = []
        for h in IV:
            if k == h[0]:
                varinlayer.append(h[1])
        layer_with_vars_update[k] = varinlayer

    ### get the name with the same dictionary value and store it in (flipped)
    flipped = {}
    for key, value in layer_with_vars_update.items():
        if str(value) not in flipped:
            flipped[str(value)] = [key]
        else:
            flipped[str(value)].append(key)

    final_var_names = []

    for i, j in flipped.items():
        if len(j) == 1:
            for k in layer_with_vars_update[j[0]]:
                final_var_names.append(j[0]+k)
        else:
            for h in layer_with_vars_update[j[0]]:
                final_var_names.append(h)

    final_var_names_with_value = {}
    for i in final_var_names:
        for j, k in lu_info.items():
            if i in j:
                final_var_names_with_value[i] = k

    ##### read number of samples

    numlhs = inp_name + "NumofSamples.txt"

    with open(numlhs) as file5:
        lines5 = file5.readlines()

    num_lhs = lines5[0].split('\n')[0]

    newSF = 'vs_design_ps_lhs.yml'

    with open(newSF, 'w') as fnew:
        fnew.write('version: "0.9"\n')
        fnew.write('\n')
        # fnew.write('setting:\n')
        # fnew.write('  log_level_cmd: "info"\n')
        # fnew.write('  log_level_file: "debug"\n')
        # fnew.write('  log_file_name: "eval.log"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('structure:\n')
        fnew.write('  name: "square_plate"\n')
        fnew.write('  type: null\n')
        fnew.write('  parameter:\n')
        for i, j in final_var_names_with_value.items():
            fnew.write('    ' + i + ': ' + j[0] + '\n')

        fnew.write('  distribution:\n')
        id_layup_expressin = []
        for i in range(len(layup)):
            if layup_info[layup[i]]['type'] == 'expression':
                id_layup_expressin.append(i)
        for i in range(len(id_layup_expressin)):
            fnew.write('    - name: a'+str(id_layup_expressin[i]+1)+'\n')
            fnew.write('      function: f'+str(id_layup_expressin[i])+'\n')
            fnew.write('      coefficients:\n')
            for j, k in IV_name.items():
                if layup[id_layup_expressin[i]] in j:
                    fnew.write('        '+k['var name']+': '+ j +'\n')
        fnew.write('  design:\n')
        fnew.write('    file: "'+inpfilename+'"\n')
        fnew.write('    solver: "abaqus"\n')
        fnew.write('    section_prop_file: "shellsections.inp"\n')
        # fnew.write('    file: "' + bdf_name + '"\n')
        # fnew.write('    solver: "nastran"\n')
        # fnew.write('   section_prop_file: "shellsections.bdf"\n')
        fnew.write('    sg_assignment:\n')
        fnew.write('      all: "mainsg"\n')
        fnew.write('  sg:\n')
        fnew.write('    mainsg:\n')
        fnew.write('      base: "lv1_layup"\n')
        fnew.write('      model: "md2"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('function:\n')
        for i in range(len(id_layup_expressin)):
            fnew.write('  - name: "f'+str(id_layup_expressin[i])+'"\n')
            fnew.write('    type: "expression"\n')
            fnew.write('    expression: "' + layup_info[layup[id_layup_expressin[i]]]['orientation'] + '"\n')
            var_in_eqn = []
            for j, k in IV_name.items():
                if layup[id_layup_expressin[i]] in j:
                    var_in_eqn.append(k['var name'])
                    # fnew.write('    coefficients: ["' + IV_name[0] + '", "' + IV_name[1] + '"]\n')
            fnew.write('    coefficients: ' + json.dumps(var_in_eqn) + '\n')

        fnew.write('\n')
        fnew.write('\n')
        fnew.write('sg:\n')
        fnew.write('  - name: "lv1_layup"\n')
        fnew.write('    parameters:\n')
        for i in range(len(layup)):
            if layup_info[layup[i]]['type'] == 'expression':
                fnew.write('      a'+str(i+1)+': 0\n')
            else:
                fnew.write('      a' + str(i + 1) + ': '+layup_info[layup[i]]['orientation']+'\n')
        fnew.write('    design:\n')
        fnew.write('      dim: 1\n')
        fnew.write('      symmetry: 1\n')
        fnew.write('      layers:\n')
        for i in range(len(layup)):
            fnew.write('        - material: "m1"\n')
            fnew.write('          ply_thickness: ' + str(layup_info[layup[i]]['ply_thickness']) + '\n')
            fnew.write('          number_of_plies: 1\n')
            fnew.write('          in-plane_orientation: a' + str(i + 1) + '\n')
        fnew.write('\n')
        fnew.write('    model:\n')
        fnew.write('      md2:\n')
        fnew.write('        tool: "swiftcomp"\n')
        fnew.write('        version: "2.2"\n')
        fnew.write('        mesh_size: -1\n')
        fnew.write('\n')
        fnew.write('  - name: "m1"\n')
        fnew.write('    type: "material"\n')
        fnew.write('    model:\n')
        fnew.write('      md3:\n')
        fnew.write('        type: "engineering"\n')
        fnew.write('        density: 1.0\n')
        fnew.write('        elasticity:\n')
        fnew.write('          [\n')
        fnew.write('            ' + str(la[0]) + ', ' + str(la[1]) + ', ' + str(la[2]) + ',\n')
        fnew.write('            ' + str(la[3]) + ', ' + str(la[4]) + ', ' + str(la[5]) + ',\n')
        fnew.write('            ' + str(la[6]) + ', ' + str(la[7]) + ', ' + str(la[8]) + '\n')
        fnew.write('          ]\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('analysis:\n')
        fnew.write('  steps:\n')
        fnew.write('    - name: "homogenization"\n')
        fnew.write('      type: "sg"\n')
        fnew.write('      analysis: "h"\n')
        fnew.write('      setting:\n')
        fnew.write('        solver: "swiftcomp"\n')
        fnew.write('    - name: "'+abqname+'"\n')
        fnew.write('      type: "abaqus"\n')
        fnew.write('      job_file: "'+inp_name+'"\n')
        # fnew.write('      job_file: "' + bdf_name + '"\n')
        fnew.write('      setting:\n')
        fnew.write('        timeout: 600\n')
        fnew.write('      args:\n')
        fnew.write('        - "interactive"\n')
        fnew.write('      post_process:\n')
        # fnew.write('        - script: "' + post_script + '"\n')
        fnew.write('        - script: "'+abqscipt+'"\n')
        fnew.write('          args: \n')
        for i in abqargs:
            fnew.write('            - "'+i+'"\n')
        fnew.write('      step_result_file: "'+abqStep_result+'"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('study:\n')
        fnew.write('  method:\n')
        fnew.write('    sampling:\n')
        fnew.write('      sample_type:\n')
        fnew.write('        lhs:\n')
        fnew.write('      samples: ' + num_lhs + '\n')
        fnew.write('      seed: 1027\n')
        fnew.write('  variables:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    list:\n')
        for i, j in final_var_names_with_value.items():
            fnew.write('      - name: "' + i + '"\n')
            fnew.write('        type: "continuous"\n')
            fnew.write('        bounds: [' + j[1] + ', ' + j[2] + ']\n')
        fnew.write('  responses:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    response_functions:\n')
        if 'buckling' in abqname:
            fnew.write('      - descriptor: "eig1"\n')
        else:
            fnew.write('      - descriptor: "u"\n')
        fnew.write('  interface:\n')
        fnew.write('    fork:\n')
        fnew.write('      parameters_file: "params.in"\n')
        fnew.write('      results_file: "results.out"\n')
        fnew.write('      file_save: on\n')
        fnew.write('      work_directory:\n')
        fnew.write('        named: "evals/eval"\n')
        fnew.write('        directory_tag: on\n')
        fnew.write('        directory_save: on\n')
        fnew.write('    required_files: ["model/*", ' + inp_name + ']\n')
        fnew.close()


def GenYML_ABQ_OPTIM(inpfilename):

    # inpfilename = 'plate400s4r.inp'

    if inpfilename.count('/') == 0:
        onlyinpname = inpfilename.split('.')[0]
        inp_name = inpfilename
    else:
        onlyinpname = inpfilename.split("/")[-1].split('.')[0]
        inp_name = inpfilename.split("/")[-1]

    ##### read lamina properties

    lamina = inp_name + "LaminaProp_adv_SA.txt"

    with open(lamina) as file1:
        lines1 = file1.readlines()

    #### order of the lamina property in the LP : E11 E22 E33 nu12 nu23 nu31 G12 G23 G31
    LP = []
    for i in range(len(lines1)):
        LP.append(float(lines1[i].split("\n")[0]))

    #### reorder of the lamina property in the LaminaProp : E11 E22 E33 G12 G13 G23 nu12 nu13 nu23 (Swiftcomp can take this format)
    # nu13 = nu31*E11/E33
    la = np.zeros(len(LP))

    la[0] = LP[0]
    la[1] = LP[1]
    la[2] = LP[2]
    la[3] = LP[6]
    la[4] = LP[7]
    la[5] = LP[8]
    la[6] = LP[3]
    la[7] = LP[4]
    la[8] = LP[5]

    ##### read thickness

    layupinfo = inp_name + "LayupandLayerinfo.txt"

    with open(layupinfo) as file2:
        lines2 = file2.readlines()

    layup = lines2[0].split('\n')[0].replace('[', '').replace(']', '').split('/')

    layup_info = {}
    for i in range(len(layup)):
        layup_info[lines2[4*i+1].split('\n')[0]] = {'type': lines2[4*i+2].split('\n')[0], 'ply_thickness': lines2[4*i+3].split('\n')[0], 'orientation': lines2[4*i+4].split('\n')[0].replace('[', '').replace(']', '').replace("'",'')}

    ##### read abaqus arguments

    argsinfo = inp_name + "args.txt"

    with open(argsinfo) as file3:
        lines3 = file3.readlines()

    abqname = lines3[0].split('\n')[0]

    abqscipt = lines3[1].split('\n')[0]

    abqargs = []
    for i in range(len(lines3[2].split('\n')[0].replace('[','').replace(']','').split(','))):
        abqargs.append(lines3[2].split('\n')[0].replace('[','').replace(']','').split(',')[i].strip()[1:-1])

    abqStep_result = lines3[-1].split('\n')[0]




    ##### initial values v1 v2 ... v9 v10
    IVfile = inp_name + "DesignVariable_ply.txt"

    with open(IVfile) as file7:
        lines7 = file7.readlines()

    # if lines12[0] != '\n':
    iv_list = lines7[0].split("\n")[0].replace('[', '').replace(']', '').replace("'", '').split(',')
    NumIV = len(iv_list)

    IV = []
    IV_name = {}
    IV_name_removeDuplicate = []

    for i in range(int(NumIV/3)):
        IV.append([iv_list[3*i].strip(),iv_list[3*i+1].strip(),iv_list[3*i+2].strip()])
        IV_name_removeDuplicate.append(iv_list[3*i+1].strip())
        IV_name[iv_list[3*i].strip()+iv_list[3*i+1].strip()] = {'var name': iv_list[3*i+1].strip(), 'var value': iv_list[3*i+2].strip()}

    IV_name_removeDuplicate = list(set(IV_name_removeDuplicate)).sort()

    ##### read scripts functions

    scriptinfo = inp_name + "all_funcScripts.txt"

    if os.path.getsize(scriptinfo) == 0:
        print("This is one-line expression problem.")
    else:
        with open(scriptinfo) as file9:
            lines9 = file9.readlines()

        lines9new = []

        for j in range(len(lines9)):
            if lines9[j] != '\n' and lines9[j] != '0\n' and lines9[j] != '0':
                # lines2[j] = lines2[j].split('\n')[0]
                lines9new.append(lines9[j].split('\n')[0])

        dict2 = {}

        for h in range(int(len(lines9new) / 6)):
            if lines9new[h] != '\n':
                dict2[lines9new[6 * h]] = [lines9new[6 * h + 1], lines9new[6 * h + 2], lines9new[6 * h + 3],
                                           lines9new[6 * h + 4],
                                           lines9new[6 * h + 5]]

    ##### read lower, upper and partition information

    lupinfo = inp_name + "bounds_opti.txt"

    with open(lupinfo) as file4:
        lines4 = file4.readlines()

    lup = []
    for i in range(len(lines4[0].split('\n')[0].replace('[', '').replace(']', '').split(','))):
        lup.append(lines4[0].split('\n')[0].replace('[', '').replace(']', '').split(',')[i].strip()[1:-1])

    #### information in lu_info is [initial value, lower bound, upper bound, partition]
    lu_info = {}
    for j in range(int(len(lup)/4)):
        lu_info[lup[4*j]+lup[4*j+1]] = [IV_name[lup[4*j]+lup[4*j+1]]['var value'], lup[4*j+2], lup[4*j+3]]



    #### get the layer name that use expression

    layup_with_vars = []
    for i, j in layup_info.items():
        if j['type'] == 'expression':
            layup_with_vars.append(i)

    #### get the layer name with corresponding variables
    layer_with_vars_update = {}

    for k in layup_with_vars:
        varinlayer = []
        for h in IV:
            if k == h[0]:
                varinlayer.append(h[1])
        layer_with_vars_update[k] = varinlayer

    ### get the name with the same dictionary value and store it in (flipped)
    flipped = {}
    for key, value in layer_with_vars_update.items():
        if str(value) not in flipped:
            flipped[str(value)] = [key]
        else:
            flipped[str(value)].append(key)

    final_var_names = []

    for i, j in flipped.items():
        if len(j) == 1:
            for k in layer_with_vars_update[j[0]]:
                final_var_names.append(j[0]+k)
        else:
            for h in layer_with_vars_update[j[0]]:
                final_var_names.append(h)

    final_var_names_with_value = {}
    for i in final_var_names:
        for j, k in lu_info.items():
            if i in j:
                final_var_names_with_value[i] = k

    ##### read method info

    methodinfo = inp_name + "method_opti.txt"

    with open(methodinfo) as file5:
        lines5 = file5.readlines()

    method = lines5[0].split('\n')[0].replace('[', '').replace(']', '').split(',')

    newSF = 'vs_design_op.yml'

    with open(newSF, 'w') as fnew:
        fnew.write('version: "0.9"\n')
        fnew.write('\n')
        # fnew.write('setting:\n')
        # fnew.write('  log_level_cmd: "info"\n')
        # fnew.write('  log_level_file: "debug"\n')
        # fnew.write('  log_file_name: "eval.log"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('structure:\n')
        fnew.write('  name: "square_plate"\n')
        fnew.write('  type: null\n')
        fnew.write('  parameter:\n')
        for i, j in final_var_names_with_value.items():
            fnew.write('    ' + i + ': ' + j[0] + '\n')

        fnew.write('  distribution:\n')
        id_layup_expressin = []
        for i in range(len(layup)):
            if layup_info[layup[i]]['type'] == 'expression':
                id_layup_expressin.append(i)
        for i in range(len(id_layup_expressin)):
            fnew.write('    - name: a'+str(id_layup_expressin[i]+1)+'\n')
            fnew.write('      function: f'+str(id_layup_expressin[i])+'\n')
            fnew.write('      coefficients:\n')
            for j, k in IV_name.items():
                if layup[id_layup_expressin[i]] in j:
                    fnew.write('        '+k['var name']+': '+ j +'\n')
        fnew.write('  design:\n')
        fnew.write('    file: "'+inpfilename+'"\n')
        fnew.write('    solver: "abaqus"\n')
        fnew.write('    section_prop_file: "shellsections.inp"\n')
        # fnew.write('    file: "' + bdf_name + '"\n')
        # fnew.write('    solver: "nastran"\n')
        # fnew.write('   section_prop_file: "shellsections.bdf"\n')
        fnew.write('    sg_assignment:\n')
        fnew.write('      all: "mainsg"\n')
        fnew.write('  sg:\n')
        fnew.write('    mainsg:\n')
        fnew.write('      base: "lv1_layup"\n')
        fnew.write('      model: "md2"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('function:\n')
        for i in range(len(id_layup_expressin)):
            fnew.write('  - name: "f'+str(id_layup_expressin[i])+'"\n')
            fnew.write('    type: "expression"\n')
            fnew.write('    expression: "' + layup_info[layup[id_layup_expressin[i]]]['orientation'] + '"\n')
            var_in_eqn = []
            for j, k in IV_name.items():
                if layup[id_layup_expressin[i]] in j:
                    var_in_eqn.append(k['var name'])
                    # fnew.write('    coefficients: ["' + IV_name[0] + '", "' + IV_name[1] + '"]\n')
            fnew.write('    coefficients: ' + json.dumps(var_in_eqn) + '\n')

        fnew.write('\n')
        fnew.write('\n')
        fnew.write('sg:\n')
        fnew.write('  - name: "lv1_layup"\n')
        fnew.write('    parameters:\n')
        for i in range(len(layup)):
            if layup_info[layup[i]]['type'] == 'expression':
                fnew.write('      a'+str(i+1)+': 0\n')
            else:
                fnew.write('      a' + str(i + 1) + ': '+layup_info[layup[i]]['orientation']+'\n')
        fnew.write('    design:\n')
        fnew.write('      dim: 1\n')
        fnew.write('      symmetry: 1\n')
        fnew.write('      layers:\n')
        for i in range(len(layup)):
            fnew.write('        - material: "m1"\n')
            fnew.write('          ply_thickness: ' + str(layup_info[layup[i]]['ply_thickness']) + '\n')
            fnew.write('          number_of_plies: 1\n')
            fnew.write('          in-plane_orientation: a' + str(i + 1) + '\n')
        fnew.write('\n')
        fnew.write('    model:\n')
        fnew.write('      md2:\n')
        fnew.write('        tool: "swiftcomp"\n')
        fnew.write('        version: "2.2"\n')
        fnew.write('        mesh_size: -1\n')
        fnew.write('\n')
        fnew.write('  - name: "m1"\n')
        fnew.write('    type: "material"\n')
        fnew.write('    model:\n')
        fnew.write('      md3:\n')
        fnew.write('        type: "engineering"\n')
        fnew.write('        density: 1.0\n')
        fnew.write('        elasticity:\n')
        fnew.write('          [\n')
        fnew.write('            ' + str(la[0]) + ', ' + str(la[1]) + ', ' + str(la[2]) + ',\n')
        fnew.write('            ' + str(la[3]) + ', ' + str(la[4]) + ', ' + str(la[5]) + ',\n')
        fnew.write('            ' + str(la[6]) + ', ' + str(la[7]) + ', ' + str(la[8]) + '\n')
        fnew.write('          ]\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('analysis:\n')
        fnew.write('  steps:\n')
        fnew.write('    - name: "homogenization"\n')
        fnew.write('      type: "sg"\n')
        fnew.write('      analysis: "h"\n')
        fnew.write('      setting:\n')
        fnew.write('        solver: "swiftcomp"\n')
        fnew.write('    - name: "'+abqname+'"\n')
        fnew.write('      type: "abaqus"\n')
        fnew.write('      job_file: "'+inp_name+'"\n')
        # fnew.write('      job_file: "' + bdf_name + '"\n')
        fnew.write('      setting:\n')
        fnew.write('        timeout: 600\n')
        fnew.write('      args:\n')
        fnew.write('        - "interactive"\n')
        fnew.write('      post_process:\n')
        # fnew.write('        - script: "' + post_script + '"\n')
        fnew.write('        - script: "'+abqscipt+'"\n')
        fnew.write('          args: \n')
        for i in abqargs:
            fnew.write('            - "'+i+'"\n')
        fnew.write('      step_result_file: "'+abqStep_result+'"\n')
        fnew.write('\n')
        fnew.write('\n')
        fnew.write('study:\n')
        fnew.write('  method:\n')
        fnew.write('    soga:\n')
        fnew.write('      max_function_evaluations: '+method[0].strip()[1:-1]+'\n')
        fnew.write('      population_size: '+method[1].strip()[1:-1]+'\n')
        fnew.write('      seed: '+method[2].strip()[1:-1]+'\n')
        fnew.write('      print_each_pop: ' + method[3].strip()[1:-1] + '\n')
        fnew.write('  variables:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    list:\n')
        for i, j in final_var_names_with_value.items():
            fnew.write('      - name: "' + i + '"\n')
            fnew.write('        type: "continuous"\n')
            fnew.write('        bounds: [' + j[1] + ', ' + j[2] + ']\n')
        fnew.write('  responses:\n')
        fnew.write('    data_form: "explicit"\n')
        fnew.write('    objective_functions:\n')
        if 'buckling' in abqname:
            fnew.write('      - descriptor: "eig1"\n')
        else:
            fnew.write('      - descriptor: "u"\n')
        fnew.write('        sense: "max"\n')

        fnew.write('  interface:\n')
        fnew.write('    fork:\n')
        fnew.write('      parameters_file: "params.in"\n')
        fnew.write('      results_file: "results.out"\n')
        fnew.write('      file_save: on\n')
        fnew.write('      work_directory:\n')
        fnew.write('        named: "evals/eval"\n')
        fnew.write('        directory_tag: on\n')
        fnew.write('        directory_save: on\n')
        fnew.write('    required_files: ["model/*", ' + inp_name + ']\n')
        fnew.close()

solver = sys.argv[1]
originalfilename = sys.argv[2]

if __name__ == '__main__':
    if (solver == "nastran_sa") and len(originalfilename) != 0:
        GenYML_NAS_SA(originalfilename)
    elif (solver == "abaqus_sa") and len(originalfilename) != 0:
        GenYML_ABQ_SA(originalfilename)
    elif (solver == "abaqus_ps") and len(originalfilename) != 0:
        GenYML_ABQ_PS(originalfilename)
    elif (solver == "abaqus_ps_lhs") and len(originalfilename) != 0:
        GenYML_ABQ_PS_lhs(originalfilename)
    elif (solver == "abaqus_op") and len(originalfilename) != 0:
        GenYML_ABQ_OPTIM(originalfilename)
    else:
        print("input Abaqus or Nastran or oldfile name as the parameter in the command line:")