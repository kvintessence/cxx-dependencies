#!/usr/bin/env python

from database import SourceFile
from pony import orm as pony


@pony.db_session
def getDepth(sourceFile, origin, depth=0):
    linkedFiles = [i.link for i in sourceFile.includes if i.link]

    if (len(linkedFiles) > 0):
        return max([getDepth(f, origin, depth + 1) for f in linkedFiles if f != origin])
    else:
        return depth + (1 if len(sourceFile.includes) > 0 else 0)


@pony.db_session
def getDependencies(sourceFile, bag=None):
    bag = bag or set()

    bag.add(sourceFile.fullPath)

    for include in sourceFile.includes:
        if include.link:
            if include.link.fullPath not in bag:
                bag |= getDependencies(include.link, bag)
        else:
            bag.add(include.path)

    return bag


@pony.db_session
def getIncluders(sourceFile, bag=None):
    bag = bag or set()

    bag.add(sourceFile.fullPath)

    for include in sourceFile.includedBy:
        if include.owner.fullPath not in bag:
            bag |= getIncluders(include.owner, bag)

    return bag


@pony.db_session
def recalculateDependencies(allSourceFiles=False):
    for sourceFile in SourceFile.select(lambda f: f.isTarget or allSourceFiles):
        sourceFile.dependenciesCount = len(getDependencies(sourceFile)) - 1


@pony.db_session
def recalculateIncluders(allSourceFiles=False):
    for sourceFile in SourceFile.select(lambda f: f.isTarget or allSourceFiles):
        sourceFile.includersCount = len(getIncluders(sourceFile)) - 1


@pony.db_session
def averageDependenciesCount():
    counts = [f.dependenciesCount for f in SourceFile.select(lambda f: f.isTarget and not f.isHeader)]
    if len(counts) > 0:
        return float(sum(counts)) / len(counts)
    return 0
