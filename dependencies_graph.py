#!/usr/bin/env python

from __future__ import print_function

import os
import tempfile
from shell import runCommand, executableExists, eprint, createIntermediateDirs
from database import SourceFile, GraphNode
from pony import orm as pony


@pony.db_session
def findOneGraphNode(identifier):
    return GraphNode.get(identifier=identifier)


@pony.db_session
def spawnOneGraphNode(identifier, name, color):
    if GraphNode.get(identifier=identifier):
        return GraphNode.get(identifier=identifier)

    return GraphNode(identifier=identifier, name=name, color=color)


@pony.db_session
def spawnGraphNodesRecursively(sourceFile, depth):
    node = spawnOneGraphNode(sourceFile.fullPath, sourceFile.fileName, 'gray')

    if node.processed:
        return

    node.processed = True

    for include in sourceFile.includes:
        if include.link:
            existingNode = findOneGraphNode(include.link.fullPath)

            if (include.link.isTarget and sourceFile.isTarget) or (depth > 0) or existingNode:
                anotherNode = spawnOneGraphNode(include.link.fullPath, include.link.fileName, 'gray')
                node.linksTo.add(anotherNode)

                if depth > 0:
                    newDepth = depth - (0 if include.link.isTarget else 1)
                    spawnGraphNodesRecursively(include.link, newDepth)

        else:
            existingNode = findOneGraphNode(include.path)

            if depth > 0 or existingNode:
                anotherNode = spawnOneGraphNode(include.path, include.fileName, 'gray')
                node.linksTo.add(anotherNode)

    if depth <= 0 and sourceFile.dependenciesCount > 0:
        name = sourceFile.fullPath + "_include_count"
        omittedIncludesNode = spawnOneGraphNode(name, str(sourceFile.dependenciesCount) + "+", 'gray')
        omittedIncludesNode.dashed = True
        node.linksTo.add(omittedIncludesNode)


@pony.db_session
def spawnGraphNodes(depth):
    # add mandatory files
    for sourceFile in SourceFile.select(lambda f: f.isTarget):
        spawnOneGraphNode(sourceFile.fullPath, sourceFile.fileName, 'red')

    # spawn links
    for sourceFile in SourceFile.select(lambda f: f.isTarget):
        spawnGraphNodesRecursively(sourceFile, depth)


def getDotPicture(graph, engine):
    if not executableExists(engine):
        eprint("No 'dot' executable!")

    dotFileName = None
    pngFileName = None

    with tempfile.NamedTemporaryFile(delete=False) as dotFile:
        dotFileName = os.path.abspath(dotFile.name)
        dotFile.write(graph)

    with tempfile.NamedTemporaryFile(delete=False) as pngFile:
        pngFileName = os.path.abspath(pngFile.name)

    runCommand("%s -Tpng -o %s %s" % (engine, pngFileName, dotFileName))

    with open(pngFileName, "r") as graphFile:
        return graphFile.read()


@pony.db_session
def createGraphText(engine):
    graph = ""
    graph += "    graph [overlap=\"false\"]\n"

    for node in GraphNode.select():
        fmt = "    \"%s\" [color=%s, label=\"%s\", style=%s];\n"
        style = "dashed" if node.dashed else "solid"
        graph += fmt % (node.identifier, node.color, node.name, style)

    for node in GraphNode.select():
        for link in node.linksTo:
            fmt = "    \"%s\" -> \"%s\" [style=%s];\n"
            style = "dashed" if link.dashed else "solid"
            graph += fmt % (node.identifier, link.identifier, style)

    return "digraph G {\n" + graph + "}"


def saveGraph(engine, name, path):
    createIntermediateDirs(path)
    graph = createGraphText(engine)

    with open(os.path.join(path, name + ".dot"), "w") as graphFile:
        graphFile.write(graph)

    with open(os.path.join(path, name + ".png"), "w") as imageFile:
        imageFile.write(getDotPicture(graph, engine))


@pony.db_session
def generateDependenciesGraph(engine="dot", depth=1, name="graph", path="."):
    GraphNode.select().delete(bulk=True)
    spawnGraphNodes(depth=depth)
    saveGraph(engine=engine, name=name, path=path)
