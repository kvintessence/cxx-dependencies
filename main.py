#!/usr/bin/env python

from __future__ import print_function

import argparse
from source_files_finder import spawnSourceFiles
from header_deps import recalculateDependencies, averageDependenciesCount
from link_includes import linkIncludes
from dependencies_graph import generateDependenciesGraph
from database import SourceFile
from pony import orm as pony


if __name__ == "__main__":
    engines = ["dot", "circo", "neato", "twopi", "fdp"]

    # Command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='+', type=str, help="One or more files/dirs to be analyzed.")
    parser.add_argument('-r', '--repository', nargs='*', type=str, help="One or more files/dirs of code.")
    parser.add_argument('-n', '--name', type=str, default="graph", help="Output base file name.")
    parser.add_argument('-o', '--output', type=str, default=".", help="Output directory.")
    parser.add_argument('-d', '--depth', type=int, default=1, help="Include traverse depth.")
    parser.add_argument('-e', '--engine', type=str, default="dot", choices=engines, help="Graph layout type.")
    args = parser.parse_args()

    spawnSourceFiles(args.input, isTarget=True)
    spawnSourceFiles(args.repository, isTarget=False)
    linkIncludes()
    recalculateDependencies(allSourceFiles=True)

    print('')

    with pony.db_session:
        for sourceFile in SourceFile.select(lambda f: f.isTarget):
            print(sourceFile.fullPath, ' | count = ', sourceFile.dependenciesCount)

    print('')
    print('Average dependencies count: %.1f' % averageDependenciesCount())

    generateDependenciesGraph(engine=args.engine, depth=args.depth, name=args.name, path=args.output)
