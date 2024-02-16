from abaqus import *
from abaqusConstants import *

import os

# py_path = "E:\\tools\\msg_design_tool_v0.0.7\\scripts;D:\\Program Files\\dakota-6.11.0-release-public-Windows.x86-UI\\share\\dakota\\Python;D:\\Anaconda3;D:\\Anaconda3\\Scripts;D:\\Anaconda3\\Library\\mingw-w64\\bin;D:\\Anaconda3\\Library\\bin;D:\\Anaconda3\\Lib\\site-packages"

# sys_path = "E:\\tools\\msg_design_tool_v0.0.7\\scripts;D:\\Program Files\\dakota-6.11.0-release-public-Windows.x86-UI\\share\\dakota\\Python;D:\\Anaconda3;D:\\Anaconda3\\Scripts;D:\\Anaconda3\\Library\\mingw-w64\\bin;D:\\Anaconda3\\Library\\bin;D:\\Anaconda3\\Lib\\site-packages;D:\\Program Files\\dakota-6.11.0-release-public-Windows.x86-UI\\bin;D:\\Program Files\\dakota-6.11.0-release-public-Windows.x86-UI\\lib;D:\\MSG\\SwiftCompTailorable;D:\\SIMULIA\\Commands;C:\\Windows\\System32"
with open('Paths.txt') as inp:
    lines=inp.readlines()
sys_path=lines[0]
py_path=lines[1]

os.environ["PYTHONPATH"] = py_path
os.environ["PATH"] = sys_path


def KernelFunction():
    return True 


def ParaFunction():

    os.system('datc.bat vs_design_ps.yml')
    
    return True

#
# def StructuralFunc():
#     return True


def Optimization():

    os.system('datc.bat vs_design_opti.yml')
    return True


def Task4():

    os.system('python run.py vs_cyl_bck_design.json')
    return True


def num_plies(equation):
    return True
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
##############################################################
