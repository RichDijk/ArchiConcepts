#!/usr/bin/python
#
# Natural Language Processing of Concepts to Neo4J Information
#
__author__ = 'morrj140'
__VERSION__ = '0.1'

import os
from subprocess import call
import time
import logging
from nl_lib import Logger
from nl_lib.Concepts import Concepts
from nl_lib.ConceptGraph import Neo4JGraph
from nl_lib.Constants import *

logger = Logger.setupLogging(__name__)
logger.setLevel(logging.INFO)

from al_ArchiLib.Constants import *
from al_ArchiLib.ArchiLib import ArchiLib
from al_ArchiLib.Neo4JLib import Neo4JLib

class ConceptsImportNeo4J(object):

    def __init__(self, ClearNeo4J=False):

        if CleanNeo4j == True:
            self.clearNeo4J()

        logger.info("Neo4J instance : %s" % gdb)
        self.graph = Neo4JGraph(gdb)

        if CleanNeo4j == True:
            self.graph.clearGraphDB()

        self.al = ArchiLib()
        self.nj = Neo4JLib()

    def addGraphNodes(self, concepts, n=0, threshold=1):
        n += 1
        for c in concepts.getConcepts().values():
            logger.debug("%d : %d Node c : %s:%s" % (n, len(c.getConcepts()), c.name, c.typeName))

            self.al.cleanConcept(c)

            c.name = c.name.replace("\"", "'")

            self.graph.addConcept(c)

            if len(c.getConcepts()) > threshold:
                self.addGraphNodes(c, n)

    def addGraphEdges(self, concepts, n=0):
        n += 1

        self.graph.addConcept(concepts)

        for c in concepts.getConcepts().values():

            logger.debug("%d : %d %s c : %s:%s" % (n, len(c.getConcepts()), concepts.name, c.name, c.typeName))

            self.al.cleanConcept(c)

            c.name = c.name.replace("\"", "'")

            self.graph.addConcept(c)

            self.graph.addEdge(concepts, c, c.typeName)

            self.addGraphEdges(c, n)

    def logGraph(self, gl, title, scale=1):
        pr = 0
        len_pr = len(gl)
        sum_pr = 0.0
        try:
            logger.info("---%s---[%d]" % (title, len(gl)))

            n = 0
            for x in gl:
                n += 1
                if isinstance(gl, dict) and x != None:
                    sum_pr = gl[x]
                    if gl[x] > pr:
                        pr = gl[x]

                    logger.info("%s [%d]:%s=%3.4f" % (title, n, x, gl[x]*scale))

                else:
                    logger.info("%s [%d]" % (x, n))
        except:
            logger.warn("Ops...")

        logger.info("Len gl[x]=%3.4f" % len_pr)
        logger.info("Max gl[x]=%3.4f" % pr)
        logger.info("Avg gl[x]=%3.4f" % (sum_pr / len_pr))

    def clearNeo4J(self):
        if gdb == LocalGBD:
            logger.info("Reset Neo4J Graph DB")
            call([self.al.resetNeo4J])

    def importNeo4J(self, concepts, ClearNeo4J=False):

        logger.info("Adding Neo4J nodes to the graph ...")
        self.addGraphNodes(concepts)

        logger.info("Adding Neo4J edges to the graph ...")
        self.addGraphEdges(concepts)

        self.graph.setNodeLabels()

        if ClearNeo4J:
            DropNode = "MATCH (n { name: 'Node' })-[r]-() DELETE n, r"
            self.nj.cypherQuery(DropNode)

            DropDuplicates = "match p=(n)--(r0:Relation), q=(m)--(r1:Relation) where n.name = m.name and n.typeName = m.typeName delete m, r1"
            self.nj.cypherQuery(DropDuplicates)

        CountRequirements = "MATCH (n {typeName:'BusinessObject'}) -- m -- (o {typeName:'Requirement' }) with n, count(o) as rc  set n.RequirementCount=rc RETURN n.name, rc order by rc desc"
        self.nj.cypherQuery(CountRequirements)

if __name__ == "__main__":

    start_time = ArchiLib.startTimer()

    importConcepts = Concepts.loadConcepts(ArchiLib.fileConceptsExport)

    in4j = ConceptsImportNeo4J()

    in4j.importNeo4J(importConcepts, ClearNeo4J=True)

    ArchiLib.stopTimer(start_time)








