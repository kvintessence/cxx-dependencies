#!/usr/bin/env python

from __future__ import print_function

import re
import os
from database import SourceFile, Include
from shell import eprint
from pony import orm as pony


@pony.db_session
def spawnSourceFile(filePath, isTarget=False, systemHeaders=False):
    fullPath = os.path.abspath(filePath)

    if SourceFile.get(fullPath=fullPath):
        return SourceFile.get(fullPath=fullPath)

    shortName = fullPath.split("/")[-1]
    isHeader = shortName.endswith((".hpp", ".h"))

    sourceFile = SourceFile(fullPath=fullPath, fileName=shortName, isTarget=isTarget, isHeader=isHeader)

    with open(filePath) as file:
        for line in file:
            if systemHeaders:
                result = re.search(r'[#@]\s*(?:include|import)\s*[\"\'<](.+)[\"\'>]', line)
            else:
                result = re.search(r'[#@]\s*(?:include|import)\s*[\"\'](.+)[\"\']', line)

            if result is not None:
                importPath = result.group(1)
                importFileName = importPath.split('/')[-1]

                if Include.get(path=importPath, owner=sourceFile):
                    print("Duplicate include '%s' found in file '%s'." % (importPath, sourceFile.fullPath))
                else:
                    Include(path=importPath, fileName=importFileName, owner=sourceFile)

    return sourceFile


def spawnSourceDirectory(dirPath, isTarget=False, systemHeaders=False):
    postfixes = (".cpp", ".hpp", ".c", ".h", ".m", ".mm")

    for root, subFolders, files in os.walk(dirPath):
        for fileName in files:
            if fileName.endswith(postfixes):
                spawnSourceFile(os.path.join(root, fileName), isTarget, systemHeaders)


def spawnSourceFiles(entries, isTarget=False, systemHeaders=False):
    if not entries:
        return

    for path in entries:
        if os.path.isfile(path):
            spawnSourceFile(path, isTarget, systemHeaders)
        elif os.path.isdir(path):
            spawnSourceDirectory(path, isTarget, systemHeaders)
        else:
            eprint("Error: couldn't process path '%s'." % path)
