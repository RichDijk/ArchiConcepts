#!/usr/bin/python
#
# Concept Logging
#
__author__ = 'morrj140'

import os
from nl_lib.Constants import *
from nl_lib import Logger
from nl_lib.Concepts import Concepts
import time

logger = Logger.setupLogging(__name__)

from al_ArchiLib import *

if __name__ == "__main__":
    #conceptFile = "documents.p"
    #conceptFile = "words.p"
    #conceptFile = "chunks.p"
    #conceptFile = "topicChunks.p"
    #conceptFile = "topicsDict.p"
    #conceptFile = "documentsSimilarity.p"
    #conceptFile = "NVPChunks.p"
    #conceptFile = "ngrams.p"
    #conceptFile = "ngramscore.p"
    #conceptFile = "ngramsubject.p"
    #conceptFile = "archi.p"
    #conceptFile = "traversal.p"
    #conceptFile = "batches.p"
    conceptFile = "export.p"
    #conceptFile = "req.p"
    #conceptFile = "Systems.p"
    #conceptFile = "Contract Management.p"
    #conceptFile = "Estimation20142212_180938.p"
    #conceptFile = "pptx.p"

    fileExport="export" + time.strftime("%Y%d%m_%H%M%S") +".csv"

    #dir = "/Users/morrj140/Development/GitRepository/DirCrawler/CodeGen/Research_20141709_104529"
    directory = os.getcwd()

    #filePath = dir + os.sep + conceptFile
    filePath = directory + os.sep + conceptFile

    logger.info("Loading :" + filePath)
    concepts = Concepts.loadConcepts(filePath)

    concepts.logConcepts()

    #concepts.printConcepts()

    #Concepts.outputConceptsToCSV(concepts, fileExport)



        




