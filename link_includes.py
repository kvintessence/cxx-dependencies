#!/usr/bin/env python

from __future__ import print_function

import os
from database import SourceFile
from source_files_finder import spawnSourceFile
from pony import orm as pony


@pony.db_session
def linkIncludes():
    for sourceFile in SourceFile.select():
        for include in sourceFile.includes:
            # try relative path first
            relativePath = "/".join(sourceFile.fullPath.split("/")[:-1] + [include.path])

            if os.path.isfile(relativePath):
                linkedSourceFile = spawnSourceFile(relativePath)
                include.link = linkedSourceFile
                continue

            possibleMatches = SourceFile.select(lambda f: f.fullPath.endswith("/" + include.path))
            if len(possibleMatches) == 0:
                continue

            if len(possibleMatches) > 1:
                print("More than one match found for include '" + include.path + "':")
                for match in possibleMatches:
                    print(" --> '" + match.fullPath + "':")

            include.link = possibleMatches.first()
