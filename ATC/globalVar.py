from kernelAccess import mdb, session
import json

import globalVar

global EQS
global IV
global L
global U
global P
global Th
global elemID
global mat_name1


def my_init():
    global EQS
    global L_ID
    global Th
    EQS = []
    L_ID = []
    Th = []


def my_init_iv():  # v'1'
    global IV
    global coeff
    coeff = []
    IV = [0]


def add_to(l, e):
    EQS.append(e)
    L_ID.append(l)


def add_thickness(t):
    Th.append(t)


def add_coeff(c):
    for i in c.split(','):
        coeff.append(int(i))


def get_coeff():
    return coeff


def get_myeqs():
    return EQS


def get_mylid():
    return L_ID


def my_init_material():
    global mat_name1
    mat_name1 = []


def add_to_material(mat_name):
    mat_name1.append(mat_name)


def get_mymaterial():
    return mat_name1


def get_mythickness():
    return list(set(Th))


def add_myinitialvalues(iv):  # v'1'
    for i in iv:
        IV.append(int(iv))


def get_myinitialvalues():  # v'1'
    return list(set(IV))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def my_init_para():
    global L
    global U
    global P
    L = []
    U = []
    P = []


def add_to_mybounds(l, u, p):
    for i in l.split(','):
        L.append(int(i))
    for i in u.split(','):
        U.append(int(i))

    P.append(p)


def get_mylowerbound():
    return L


def get_myupperbound():
    return U


def get_mydiv():
    return P


bound_dict = {}


# bound_dict["type"] = "continuous"


def variable_list_bounds(layer_name, adv_name, l, u):
    bound_dict["name"] = layer_name + adv_name
    bound_dict["type"] = "continuous"
    bound_dict["bounds"] = []
    bound_dict["bounds"].append(int(l))
    bound_dict["bounds"].append(int(u))

    return bound_dict


radius_bound_dict = {}


def radius_bounds(l, u):
    radius_bound_dict["name"] = "inclusion_radius"
    radius_bound_dict["type"] = "continuous"
    radius_bound_dict["bounds"] = []
    radius_bound_dict["bounds"].append(float(l))
    radius_bound_dict["bounds"].append(float(u))

    return radius_bound_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def init_elements():
    global elemID
    elemID = []


def add_to_elements(label):
    elemID.append(label)


def get_myelemID():
    return elemID


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# global fileName
# global functionName
# global trans
# global ply_th
# global ply_number
# global mat_name
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def init_script():
#     global fileName
#     global functionName
#     global trans
#     global ply_th
#     global ply_number
#     global mat_name
#     fileName=[]
#     functionName=[]
#     trans=[]
#     ply_th=[]
#     ply_number=[]
#     mat_name=[]
#
# def add_to_script(filename,functionname,t):
#     fileName.append(filename)
#     functionName.append(functionname)
#     trans.append(t)
#
#
# def get_myfilename():
#     return fileName
#
# def get_myfunctionname():
#     return functionName
#
# def get_mytransformation():
#     return trans
#
# def get_myplythickness():
#     return ply_th
#
# def get_myplynumber():
#     return ply_number
#
# def get_mymat_name():
#     return mat_name
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

global coeffname


def init_coeffname():
    global coeffname
    coeffname = []


def add_to_coeffname(tabl):
    coeffname.append(tabl)


def get_mycoeffname():
    return coeffname


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global coeffval


def init_coeffval():
    global coeffval
    coeffval = []


def add_to_coeffval(table):
    coeffval.append(table)


def get_mycoeffval():
    return coeffval


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global nodeset


def init_nodeset():
    global nodeset
    nodeset = []


def add_to_mynodeset(node):
    nodeset.append(node)


def get_mynodeset():
    return nodeset


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global jobname


def init_jobname():
    global jobname
    jobname = []


def add_to_myjobs(job):
    jobname.append(job)


def get_myjobname():
    return jobname


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global switch


def switch0():
    global switch
    switch = 0


def switch1():
    global switch
    switch = 1


def get_Switch():
    return switch


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# advance para table
global adv1
global adv2
global adv3
global adv4


def advpara():
    global adv1
    global adv2
    global adv3
    global adv4

    adv1 = []
    adv2 = []
    adv3 = []
    adv4 = []


def add_to_advname(name):
    adv1.append(name)


def add_to_advL(l):
    adv2.append(l)


def add_to_advU(u):
    adv3.append(u)


def add_to_advP(p):
    adv4.append(p)


def get_myAdvname():
    return adv1


def get_myAdvL():
    return adv2


def get_myAdvU():
    return adv3


def get_myAdvP():
    return adv4


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global LB
global UB


def my_init_bounds():
    global LB
    global UB
    LB = []
    UB = []


def add_to_myBounds(l, u):
    for i in l.split(','):
        LB.append(int(i))
    for i in u.split(','):
        UB.append(int(i))


def get_mylowerB():
    return LB


def get_myupperB():
    return UB


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global flag


def flag0():  # angle
    global flag
    flag = 0


def flag1():  # exp
    global flag
    flag = 1


def flag2():  # script
    global flag
    flag = 2


def get_flag():
    return flag


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

global thisdict


def init_thisdict():
    global thisdict
    thisdict = {"file": [], "function": [], "transformation": [], "coeffname": [], "coeffval": [], "m": []}


def add_to_thisdict(f, func, trans, coeffname0, coeffval0, m0):
    thisdict["file"].append(f)
    thisdict["function"].append(func)
    thisdict["transformation"].append(trans)
    thisdict["coeffname"].append(coeffname0)
    thisdict["coeffval"].append(coeffval0)
    thisdict["m"].append(m0)


def get_thisdict():
    d0 = thisdict
    return d0


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global trans


def init_trans():
    global trans
    trans = []


def add_to_mytrans(t):
    trans.append(t)


def get_mytrans():
    return trans


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global fun


def init_fun():
    global fun
    fun = []


def add_to_myfunction(t):
    fun.append(t)


def get_myfun():
    return fun


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
global file


def init_file():
    global file
    file = []


def add_to_myfile(t):
    file.append(t)


def get_myfile():
    return file


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global choicelist


def init_choicelist():
    global choicelist
    choicelist = []


def add_to_choicelist(c):
    choicelist.append(c)


def get_mychoicelist():
    return choicelist


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
layup = ''


def add_to_layup(c):
    global layup
    layup = c


def get_mylayup():
    return layup


def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


# def get_mylayuplist():
#     for i in layup:
#         for j in i:
#             if is_num(j):
#                 layup_list.append(j)
#     return layup_list
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global gname


def init_globalname():
    global gname
    gname = []


def add_to_globalname(m):
    gname.append(m)


def get_myglobalname():
    return gname


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global gval


def init_globalval():
    global gval
    gval = []


def add_to_globalval(m):
    gval.append(m)


def get_myglobalval():
    return gval


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# failure criteria
global failure


def init_failure():
    global failure
    failure = []


def add_to_failure(f):
    failure.append(f)


def get_myfailurecriteria():
    return failure


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# strength
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global strength


def init_strength():
    global strength
    strength = []


def add_to_strength(s):
    strength.append(s)


def get_mystrengthcriteria():
    return strength


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# steps-abaqus
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global abq_name


def init_abq_name():
    global abq_name
    abq_name = []


def add_to_abq_name(s):
    abq_name.append(s)


def get_myabq_name():
    return abq_name


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global abq_job


def init_abq_job():
    global abq_job
    abq_job = []


def add_to_abq_job(s):
    abq_job.append(s)


def get_myabq_job():
    return abq_job


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global abq_script


def init_abq_script():
    global abq_script
    abq_script = []


def add_to_abq_script(s):
    abq_script.append(s)


def get_myabq_script():
    return abq_script


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global abq_step_result


def init_abq_step_result():
    global abq_step_result
    abq_step_result = []


def add_to_abq_step_result(s):
    abq_step_result.append(s)


def get_myabq_step_result():
    return abq_step_result


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# steps-python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global py_name


def init_py_name():
    global py_name
    py_name = ''


def add_to_py_name(s):
    global py_name
    py_name = s


def get_steps_py_name():
    return py_name


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global py_script


def init_py_script():
    global py_script
    py_script = ''


def add_to_py_script(s):
    global py_script
    py_script = s


def get_steps_py_script():
    return py_script


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global py_func


def init_py_func():
    global py_func
    py_func = ''


def add_to_py_func(s):
    global py_func
    py_func = s


def get_steps_py_func():
    return py_func


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global abq_arg


def init_abq_arg():
    global abq_arg
    abq_arg = []


def add_to_abq_arg(s):
    abq_arg.append(s)


def get_myabq_arg():
    return abq_arg


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global py_arg_name


def init_py_arg_name():
    global py_arg_name
    py_arg_name = []


def add_to_py_arg_name(s):
    py_arg_name.append(s)


def get_mypy_arg_name():
    return py_arg_name


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global others


# others = []

def init_others():
    global others
    others = []


def add_to_others(s):
    others.append(s)


def get_others():
    return others


# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global py_arg_val


def init_py_arg_val():
    global py_arg_val
    py_arg_val = []


def add_to_py_arg_val(s):
    py_arg_val.append(s)


def get_mypy_arg_val():
    return py_arg_val

# ~~~~~~~~~~~~~~~~~machine learning part~~~~~~~~~~~~~~~~~~~~~~~
global abq_job_ml


def init_abq_job_ml():
    global abq_job_ml
    abq_job_ml = []

def add_to_abq_job_ml(s):
    abq_job_ml.append(s)


def get_myabq_job_ml():
    return abq_job_ml


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


global switch_failure


def switch_failure0():
    global switch_failure
    switch_failure = 0


def switch_failure1():
    global switch_failure
    switch_failure = 1


def get_Switch_failure():
    return switch_failure


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global switch_globalpara


def switch_globalpara0():
    global switch_globalpara
    switch_globalpara = 0


def switch_globalpara1():
    global switch_globalpara
    switch_globalpara = 1


def get_Switch_globalpara():
    return switch_globalpara


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global symmetry


def init_symmetry():
    global symmetry
    symmetry = 0


def symmetry0():
    global symmetry
    symmetry = 0


def symmetry1():
    global symmetry
    symmetry = 1


def get_symmetry():
    return symmetry


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global lm


def init_mylaminamat():
    global lm
    lm = []


def add_to_mylaminamat(s):
    lm.append(s)


def get_mylaminamat():
    list(set(lm))
    lm.sort()
    return lm


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

global im


def init_myinclusionmat():
    global im
    im = []


def add_to_myinclusionmat(s):
    im.append(s)


def get_myinclusionmat():
    im.sort()
    return im


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

global mm


def init_mymatrixmat():
    global mm
    mm = []


def add_to_mymatrixmat(s):
    mm.append(s)


def get_mymatrixmat():
    mm.sort()
    return mm


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

material_dict = {}
material_dict['name'] = ''
material_dict['type'] = ''
material_dict['model'] = {}
material_dict['model']['md3'] = {}
material_dict['model']['md3']['type'] = ''
material_dict['model']['md3']['elasticity'] = []
material_dict['model']['md3']['cte'] = []


# material_dict['model']['md3']['specific_heat']
# print(json.dumps(material_dict))


def json_material(name, modelname, type="material", md3_type="isotropic", elasticity=[], cte=[]):
    material_dict['name'] = name  # steel
    material_dict['type'] = type

    # vpName = session.currentViewportName
    # modelName = session.sessionState[vpName]['modelName']

    cm = mdb.models[modelname].materials

    try:
        density = cm[name].density.table[0][0]
        material_dict['model']['md3']['density'] = density
    except:
        pass

    try:
        cte = cm[name].expansion.table[0]
        material_dict['model']['md3']['cte'] = cte
    except:
        pass

    try:
        elasticity = cm[name].elastic.table[0]
        material_dict['model']['md3']['elasticity'] = elasticity
    except:
        pass

    try:
        specific_heat = cm[name].specificHeat.table[0][0]
        material_dict['model']['md3']['specific_heat'] = specific_heat
    except:
        pass

    if len(elasticity) == 2:
        md3_type = "isotropic"
    elif len(elasticity) == 9:
        md3_type = "engineering"

    material_dict['model']['md3']['type'] = md3_type
    return material_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

defined_var = {}
defined_var["layer"] = []
defined_var["variable"] = []
defined_var["value"] = []


def define_variables(l1, v1, val):
    defined_var["layer"].append(l1)
    defined_var["variable"].append(v1)
    defined_var["value"].append(val)
    return defined_var


def get_define_variables():
    return defined_var


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

layer_dict = {}


# layer_dict["name"] = {}


def func_layer_dict(layer_name, orientation, thickness, material_name):
    layer_dict.update({layer_name: []})
    layer_dict[layer_name].append(orientation)
    layer_dict[layer_name].append(thickness)
    layer_dict[layer_name].append(material_name)
    return 1


def get_layer_dict():
    return layer_dict


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# distributions
dist = {}
dist["name"] = ""
dist["function"] = ""
dist["coefficients"] = {}


def define_distributions(dist_name, function_name, layer_name, coefficients):
    dist["name"] = dist_name
    dist["function"] = function_name
    for i in range(len(coefficients)):
        new_coeff_name = layer_name + coefficients[i]
        dist["coefficients"].update({coefficients[i]: new_coeff_name})
    return dist


#
# def get_distributions():
#     return dist_list


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

layer_plies_list = {}


def layer_plies(thisdict_plies):
    layer_plies_list.update(thisdict_plies)
    return 1


def get_layer_plies():
    return layer_plies_list


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
global plies_eq
plies_eq = "1"


def add_plies(p):
    global plies_eq
    plies_eq = p


def get_plies():
    return plies_eq
    
### get initial value of design variables

global IV_dv, IV_thick

def IV_designVar(s):
    global IV_dv
    IV_dv = s
    return IV_dv

def get_IV_designVar():
    return IV_dv

def IV_thickEQN(s):
    global IV_thick
    IV_thick = s
    return IV_thick

def get_IV_thickEQN():
    return IV_thick

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# dfa_list = []

def Parameters():
    parameters = {}
    define_variables_dict = globalVar.get_define_variables()
    for i in range(len(define_variables_dict["layer"])):
        parameters.update({str(define_variables_dict["layer"][i]) + str(define_variables_dict["variable"][i]):
                               define_variables_dict["value"][i]})
    return parameters


layers_info = {}


def get_layers(plane_orientation, number_of_plies, thickness, material_name):
    layers_info.update({"in-plane_orientation": str(plane_orientation),
                        "number_of_plies": str(number_of_plies),
                        "ply_thickness": float(thickness),
                        "material": str(material_name)})
    return layers_info


class Layer:
    dfa_dict = {}
    sg_parameters = {}

    def __init__(self, layer_name='', orientation='', thickness=0.0, material_name='', type_=''):
        self.layer_name = layer_name
        self.orientation = orientation
        self.thickness = thickness
        self.material_name = material_name
        self.type_ = type_
        self.function = {}
        # self.plies = '1'

    def defineFiberAngles(self, plies='1'):
        type_ = "constant angle"
        if self.layer_name != '':
            try:
                a = float(self.orientation)
            except:
                type_ = "expression"
            if plies == '1':
                self.dfa_dict.update(
                    {self.layer_name: {"orientation": [self.orientation], "ply_thickness": self.thickness,
                                       "material": self.material_name, "coefficients": [], "type": type_}})
            else:
                self.dfa_dict.update(
                    {self.layer_name: {"orientation": [self.orientation, str(plies)], "ply_thickness": self.thickness,
                                       "material": self.material_name, "coefficients": [], "type": type_}})
        return self.dfa_dict

    def get_defineFiberAngles(self):
        return self.dfa_dict

    def add_function_name(self, layer_id, func_name):
        self.dfa_dict[layer_id].update({"function name": [func_name]})
        return self.dfa_dict

    def add_function2_name(self, layer_id, func_name):
        self.dfa_dict[layer_id]["function name"].append(func_name)
        return self.dfa_dict

    def add_coefficients(self):
        define_variables_dict = globalVar.get_define_variables()

        for i in range(len(define_variables_dict["layer"])):
            self.dfa_dict[define_variables_dict["layer"][i]]["coefficients"].append(
                str(define_variables_dict["layer"][i]) + str(define_variables_dict["variable"][i]))

    def add_numA(self, dist_a, layer_id):
        self.dfa_dict[layer_id].update({"plane_orientation": dist_a})
        return self.dfa_dict

    def get_sg_parameters(self):
        for v in self.dfa_dict.values():
            self.sg_parameters.update({v["plane_orientation"]: 0})
            self.sg_parameters.update({v["plane_orientation"].replace("a", "p"): 1})
        return self.sg_parameters


class Distribution:
    dis = {
        'name': '',
        'function': '',
        'coefficients': {}
    }

    def __init__(self, name='', function='', coefficients={}):
        self.name = name
        self.function = function
        self.coefficients = coefficients

    def add_distribution(self):
        self.dis["name"] = self.name
        self.dis["function"] = self.function
        self.dis["coefficients"] = self.coefficients
        return self.dis


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# functions
class Functions:
    functions = {}

    def __init__(self, name='', type_="expression", expression=''):
        self.name = name
        self.type_ = type_
        self.expression = expression

    def add_functions(self):
        self.functions["name"] = self.name
        self.functions["type"] = self.type_
        self.functions["expression"] = self.expression
        self.functions["coefficients"] = []

        for i in range(len(self.expression)):
            if self.expression[i] == 'v':
                self.functions["coefficients"].append('v' + str(self.expression[i + 1]))
            self.functions["coefficients"] = list(set(self.functions["coefficients"]))
            if self.expression[i] == 'n':
                self.functions["return_type"] = "integer"
                self.functions["coefficients"].append('n' + str(self.expression[i + 1]))
            self.functions["coefficients"] = list(set(self.functions["coefficients"]))
        return self.functions
