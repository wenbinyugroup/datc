from odbAccess import openOdb
import sys
# import csv
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
    step_name_buckling = 'Step-1'

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
            egva = abs(float(_temp[1].split()[-1]))
            # eigenvalues[mode] = egva
            result['eig{}'.format(mode)] = egva
            # if mode == 1:
            #     result['mcr'] = math.fabs(egva)

    # print eigenvalues
    # result['eigenvalues'] = eigenvalues

    return



def getOutputFromOdb(odb_name):
    print 'reading result from odb: ' + odb_name

    result = {}

    odb = openOdb(path=odb_name)
    # print odb.steps

    # Get eigenvalues
    # ===============
    getBucklingStepResult(odb, result)


    print 'done'

    odb.close()

    return result


def writeResultToFile(result, file_name, load_file_name=None):
    print 'writing result to file: ' + file_name

    # Write buckling moment (eigenvalues) and max displacement
    with open(file_name, 'w') as file:
        for k, v in result.items():
            file.write('{} = {}\n'.format(k, v))


    return


if __name__ == '__main__':

    main(sys.argv[1], *sys.argv[2:])
    # print sys.argv
    # main('Job-1.odb', 'abq_result.dat', 'abq_section_loads.csv')

