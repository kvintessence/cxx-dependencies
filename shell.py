#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import errno
from subprocess import Popen, PIPE


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def executableExists(executableName):
    try:
        devnull = open(os.devnull, "w")
        Popen([executableName], stdout=devnull, stderr=devnull)
    except OSError as error:
        if error.errno == os.errno.ENOENT:
            return False

    return True


def runCommand(command):
    return runCommands([command])


def createIntermediateDirs(path):
    p = os.path.abspath(os.path.dirname(path.rstrip('/') + '/'))

    if not os.path.exists(p):
        try:
            os.makedirs(p)
        except OSError as exc:
            pass
            if exc.errno != errno.EEXIST:
                raise


def runCommands(commandsList):
    if not (isinstance(commandsList, list) or isinstance(commandsList, tuple)):
        return runCommands([commandsList])

    try:
        p = Popen(commandsList[0], stdout=PIPE, shell=True)

        for command in commandsList[1:]:
            p = Popen(command, stdin=p.stdout, stdout=PIPE, shell=True)

        return p.stdout.read().strip()
    except TypeError:
        # TODO: log through module
        print("Can't iterate through commands list: " + str(commandsList))
