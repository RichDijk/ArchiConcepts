#!/usr/bin/python
#
# Archimate to Concepts
#
__author__ = 'morrj140'
__VERSION__ = '0.3'

from al_lib.Logger import *
logger = setupLogging(__name__)
logger.setLevel(INFO)

from al_lib.Constants import *
from al_lib.ArchiLib import ArchiLib


# Note : all columns should have a header with an Archimate Object
# Can also use Property.<whatever>

import pytest

# Properties
# <element xsi:type="archimate:BusinessProcess" id="0ad0bac9" name="06.0 Activity Reports">
#        <property key="ExampleName" value="ExampleValue"/>
# </element>
#
# child2 = etree.SubElement(root, "child2")
#


def ImportCSVIntoArchi(fileArchimate, folder, fileMetaEntity):

    start_time = ArchiLib.startTimer()

    logger.info(u"Using : %s" % fileArchimate)
    al = ArchiLib(fileArchimate)

    al.logTypeCounts()

    # insertNColumns(self, folder, subfolder, fileMetaEntity):
    al.insertNColumns(u"Application", folder, fileMetaEntity)

    al.outputXMLtoFile()

    ArchiLib.stopTimer(start_time)

if __name__ == u"__main__":
    fileArchimate = u"/Users/morrj140/Documents/SolutionEngineering/Archimate Models/DVC v47.archimate"

    fileMetaEntity = u"LAT_export_sections.csv" # LANSA.csv"
    folder = u"V4 All Processes Data Analysis"

    logger.info(u"dir : %s" % os.getcwd())
    ImportCSVIntoArchi(fileArchimate, folder, fileMetaEntity)