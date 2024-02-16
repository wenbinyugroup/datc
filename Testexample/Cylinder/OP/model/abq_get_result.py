from odbAccess import openOdb
import sys
import csv
import math


def main(odb_name, *args):
    fn_result = args[0]

    try:
        fn_load = args[1]
    except IndexError:
        fn_load = None

    result = getOutputFromOdb(odb_name)

    writeResultToFile(result, fn_result, fn_load)

    return


def getBucklingStepResult(odb, result):
    step_name_buckling = 'buckling'

    # print ndset.upper()
    # ndset = odb.rootAssembly.nodeSets[ndset.upper()]
    # eigenvalues = {}  # {mode: eigenvalue, ...}
    step = odb.steps[step_name_buckling]
    for frame in step.frames:
        # print frame
        description = frame.description.strip()
        # print description

        if description.startswith('Mode'):
            _temp = description.strip().split(':')
            mode = int(_temp[0].split()[-1])
            egva = float(_temp[1].split()[-1])
            # eigenvalues[mode] = egva
            result['eig{}'.format(mode)] = egva
            if mode == 1:
                result['mcr'] = math.fabs(egva)

    # print eigenvalues
    # result['eigenvalues'] = eigenvalues

    return


def getBendingStepResult(odb, result):
    step_name_bending = 'bending'

    step = odb.steps[step_name_bending]
    frame = step.frames[-1]
    # print ''
    # print frame

    field_outputs = frame.fieldOutputs
    # print ''
    # print field_outputs

    # Get sectional stresses
    sf_labels_odb = field_outputs['SF'].componentLabels
    sm_labels_odb = field_outputs['SM'].componentLabels
    sf_labels = ['SF1', 'SF2', 'SF3']
    sm_labels = ['SM1', 'SM2', 'SM3']
    sf_labels_sg = ['N11', 'N22', 'N12']
    sm_labels_sg = ['M11', 'M22', 'M12']
    sf_cols = [sf_labels_odb.index(label) for label in sf_labels]
    sm_cols = [sm_labels_odb.index(label) for label in sm_labels]
    # print ''
    # print sf_cols
    # print sm_cols

    # print ''
    # print field_outputs['SF']
    # print ''
    # print field_outputs['SM']
    # print ''
    # print field_outputs['SF'].values[0]
    shell_stresses = {}
    for value in field_outputs['SF'].values:
        shell_stresses[value.elementLabel] = []
        data = value.data.tolist()
        for i in sf_cols:
            shell_stresses[value.elementLabel].append(data[i])
    for value in field_outputs['SM'].values:
        data = value.data.tolist()
        for i in sm_cols:
            shell_stresses[value.elementLabel].append(data[i])
    # print ''
    # for i in range(10):
    #     print shell_stresses[i+1]

    result['shell_stresses'] = shell_stresses
    result['shell_stress_labels'] = sf_labels_sg + sm_labels_sg


    # Get the max displacement
    # displacements = {}
    disp_max = 0
    for value in field_outputs['U'].values:
        u = value.data.tolist()
        u = u[0]**2 + u[1]**2 + u[2]**2
        if u > disp_max:
            disp_max = u

    # print ''
    # for i in range(10):
    #     print displacements[i+1]
    result['disp_max'] = math.sqrt(disp_max)

    return


def getOutputFromOdb(odb_name):
    print 'reading result from odb: ' + odb_name

    result = {}

    odb = openOdb(path=odb_name)
    # print odb.steps

    # Get eigenvalues
    # ===============
    getBucklingStepResult(odb, result)


    # Get bending result
    # ==================
    # getBendingStepResult(odb, result)

    print 'done'

    odb.close()

    return result


def writeResultToFile(result, file_name, load_file_name=None):
    print 'writing result to file: ' + file_name

    # Write buckling moment (eigenvalues) and max displacement
    with open(file_name, 'w') as file:
        for k, v in result.items():
            file.write('{} = {}\n'.format(k, v))


    # Write shell forces and moments
    if load_file_name:
        with open(load_file_name, 'wb') as fo:
            csv_writer = csv.writer(fo)
            csv_writer.writerow(['EID',] + result['shell_stress_labels'])
            # csv_writer.writerow(data_u_set)
            for k, v in result['shell_stresses'].items():
                csv_writer.writerow([k,] + v)

    return


if __name__ == '__main__':

    main(sys.argv[1], *sys.argv[2:])
    # print sys.argv
    # main('Job-1.odb', 'abq_result.dat', 'abq_section_loads.csv')

