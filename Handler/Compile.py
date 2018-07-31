# -*- coding: UTF-8 -*-
from __future__ import print_function

import os
import json
import subprocess

def saveFile(path, fileName, data):
    if not os.path.exists(path):
        os.makedirs(path)
    filepath = os.path.join(path, fileName)
    with open(filepath, 'wb') as upFile:
        upFile.write(data)

def compilePyFile(path, fileName):
    # compile py file
    cmdStr = 'python -c ' + \
             '"from distutils.core import setup;' + \
             ' from Cython.Build import cythonize;' + \
             ' setup(ext_modules = cythonize(\'' + fileName + '\'))"' + \
             ' build_ext --inplace'
    proc = subprocess.Popen(cmdStr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=path)

    errorStr = ""
    line = "start"
    collectMessage = False

    while line:
        if line.startswith('Error compiling '):
            errorStr = 'Failed to compile strategy file:\n'
            collectMessage = True  # start collect error message
        elif collectMessage and line.startswith('Traceback '):
            collectMessage = False  # stop collect error message
        else:
            if collectMessage:
                errorStr += line

        line = proc.stdout.readline()
        print(">> ", line,)  # line has \n, so no need to switch line in print

    print()  # switch line after all printed

    retStr = None
    if errorStr:
        retStr = json.dumps({'msg': errorStr, 'status': 500})
    return retStr


def compileMFile(path, strategyId, fileName):
    errorStr = "matlab compile error"

    # compile m file
    mcompile = "matlab  -nojvm -nodisplay -nosplash -nodesktop -r 'pcode *.m, exit'"
    finalFileName = 'STR' + strategyId + '.zip'

    # chdir
    os.chdir(path)

    # unzip
    cmdStr = 'unzip -o ' + fileName
    ret = os.system(cmdStr)

    # rename
    if fileName[:-4] != 'Main':
        cmdStr = 'mv -f ' + fileName[:-4] + '.m Main.m'
        ret = ret or os.system(cmdStr)

    # compile *.m to *.p
    cmdStr = mcompile
    ret = ret or os.system(cmdStr)

    # zip
    cmdStr = 'zip ' + finalFileName + ' *.p'
    ret = ret or os.system(cmdStr)
    print(ret)
    # remove tmp files
    cmdStr = 'rm -rf *.m *.p'
    ret = ret or os.system(cmdStr)

    retStr = None
    if ret:
        retStr = json.dumps({'msg': errorStr, 'status': 500})
    return retStr
