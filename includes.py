#!/usr/bin/env python

from __future__ import print_function

import argparse
from source_files_finder import spawnSourceFiles
from header_deps import recalculateDependencies, averageDependenciesCount, getDependencies
from link_includes import linkIncludes
from database import SourceFile
from pony import orm as pony


if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='+', type=str, help="One or more files/dirs to be analyzed.")
    parser.add_argument('-r', '--repository', nargs='*', type=str, help="One or more files/dirs of code.")
    parser.add_argument('-sh', '--system-headers', dest='system_headers', action='store_true', help="Include system headers.")
    parser.add_argument('-l', '--list', dest='list', action='store_true', help="Also print all included headers.")
    parser.set_defaults(system_headers=False)
    parser.set_defaults(list=False)
    args = parser.parse_args()

    spawnSourceFiles(args.input, isTarget=True, systemHeaders=args.system_headers)
    spawnSourceFiles(args.repository, isTarget=False, systemHeaders=args.system_headers)
    linkIncludes(systemHeaders=args.system_headers)
    recalculateDependencies(allSourceFiles=True)

    print('')
    print('Average dependencies count: %.1f' % averageDependenciesCount())
    print('')

    with pony.db_session:
        sourceFiles = [sourceFile for sourceFile in SourceFile.select(lambda f: f.isTarget)]
        sourceFiles.sort(key=lambda sf: sf.dependenciesCount, reverse=True)

        maxLength = max([len(sf.fullPath) for sf in sourceFiles])
        tableLine = '-----+-' + '-' * (1 + maxLength)

        if not args.list:
            print(tableLine)

        for sourceFile in sourceFiles:
            if args.list:
                print(tableLine)

            print('%4d | %s' % (sourceFile.dependenciesCount, sourceFile.fullPath))

            if args.list:
                print(tableLine)

            dependencies = sorted(getDependencies(sourceFile))
            dependencies.remove(sourceFile.fullPath)

            if args.list and len(dependencies) > 0:
                for dependency in dependencies:
                    print('     | %s' % dependency)

                print(tableLine)
                print('')

        if not args.list:
            print(tableLine)
