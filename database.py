#!/usr/bin/env python

from pony import orm as pony


db = pony.Database()


class SourceFile(db.Entity):
    fullPath = pony.PrimaryKey(str)
    fileName = pony.Required(str)
    includes = pony.Set('Include', reverse='owner')
    includedBy = pony.Set('Include', reverse='link')
    isTarget = pony.Required(bool)
    isHeader = pony.Required(bool)

    dependenciesCount = pony.Optional(int)
    includersCount = pony.Optional(int)


class Include(db.Entity):
    path = pony.Required(str)
    fileName = pony.Required(str)
    owner = pony.Required('SourceFile', reverse='includes')
    link = pony.Optional('SourceFile', reverse='includedBy')
    pony.PrimaryKey(path, owner)


class GraphNode(db.Entity):
    identifier = pony.PrimaryKey(str)
    name = pony.Required(str)
    color = pony.Required(str)

    processed = pony.Optional(bool)
    dashed = pony.Optional(bool)

    linksTo = pony.Set('GraphNode', reverse='linksFrom')
    linksFrom = pony.Set('GraphNode', reverse='linksTo')


db.bind(provider='sqlite', filename=':memory:')
db.generate_mapping(create_tables=True)
