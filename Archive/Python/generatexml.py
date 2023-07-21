##Using dict2aml##

from dict2xml import dict2xml as d2x
data = {
    'PARTS' : {
        'PART mode="auto': {
            'KIND_OF_PART': 'MaPSA',
            'NAME_LABEL': 'AEM_35494_016L',
            'LOCATION': 'AEMtec',
            'VERSION': '2.0',
            'CHILDREN':{
                'PART mode="auto"':{
                    'KIND_OF_PART':'MPA Chip',
                    'SERIAL_NUMBER':'805315419',
                    'NAME_LABEL':'N6Y215_03_506'
                },
            'PREDEFINED_ATTRIBUTES':{
                'ATTRIBUTE':{
                    'NAME':'Chip Posn on Sensor',
                    'VALUE':'1'
                }
                }
            }
        }
    }
  }
print(d2x(data, wrap="all", indent="  "))





##Using Elementree##

#repeating MaPSA part  (maybe do for loop instead of copy,paste?)

import xml.etree.ElementTree as ET
import xml.dom.minidom

root = ET.Element("ROOT")
parts = ET.SubElement(root, "PARTS")

# MaPSA 1
MAPSA = ET.SubElement(parts, "PART", mode="auto")
ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
ET.SubElement(MAPSA, "NAME_LABEL").text = "AEM_35494_016L"
ET.SubElement(MAPSA, "MANUFACTURER").text = "AEMtec"
ET.SubElement(MAPSA, "LOCATION").text = "AEMtec"
ET.SubElement(MAPSA, "VERSION").text = "2.0"

predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
ET.SubElement(attr1, "NAME").text = "Status"
ET.SubElement(attr1, "VALUE").text = "Good"

#MPA chip 1
child1 = ET.SubElement(MAPSA, "CHILDREN")
#Sub element of child1
child1_sub = ET.SubElement(child1, "PART", mode="auto")
ET.SubElement(child1_sub, "KIND_OF_PART").text = "MPA Chip"
ET.SubElement(child1_sub, "SERIAL_NUMBER").text = "805315419"
ET.SubElement(child1_sub, "NAME_LABEL").text = "N6Y215_03_506"
#Predefined attributes of child1
child1_predef = ET.SubElement(child1_sub, "PREDEFINED_ATTRIBUTES")
child1_predef_attr = ET.SubElement(child1_predef, "ATTRIBUTE")
ET.SubElement(child1_predef_attr, "NAME").text = "Chip Posn on Sensor"
ET.SubElement(child1_predef_attr, "VALUE").text = "1"

#############################################################
# MaPSA 2
MAPSA2 = ET.SubElement(parts, "PART", mode="auto")
ET.SubElement(MAPSA2, "KIND_OF_PART").text = "MaPSA"
ET.SubElement(MAPSA2, "NAME_LABEL").text = "AEM_35494_016L"
ET.SubElement(MAPSA2, "MANUFACTURER").text = "AEMtec"
ET.SubElement(MAPSA2, "LOCATION").text = "AEMtec"
ET.SubElement(MAPSA2, "VERSION").text = "2.0"

predefMapsa2 = ET.SubElement(MAPSA2, "PREDEFINED_ATTRIBUTES")
attr2 = ET.SubElement(predefMapsa2, "ATTRIBUTE")
ET.SubElement(attr2, "NAME").text = "Status"
ET.SubElement(attr2, "VALUE").text = "Good"

#MPA chip 2
child2 = ET.SubElement(MAPSA2, "CHILDREN")
child2_sub = ET.SubElement(child2, "PART", mode="auto")
ET.SubElement(child2_sub, "KIND_OF_PART").text = "MPA Chip"
ET.SubElement(child2_sub, "SERIAL_NUMBER").text = "1207968604"
ET.SubElement(child2_sub, "NAME_LABEL").text = "N6Y215_03_505"

child2_predef = ET.SubElement(child2_sub, "PREDEFINED_ATTRIBUTES")
child2_predef_attr = ET.SubElement(child2_predef, "ATTRIBUTE")
ET.SubElement(child2_predef_attr, "NAME").text = "Chip Posn on Sensor"
ET.SubElement(child2_predef_attr, "VALUE").text = "16"

#############################################################
#..........

# MaPSA 17
MAPSA17 = ET.SubElement(parts, "PART", mode="auto")
ET.SubElement(MAPSA17, "KIND_OF_PART").text = "MaPSA"
ET.SubElement(MAPSA17, "NAME_LABEL").text = "AEM_35494_016L"
ET.SubElement(MAPSA17, "MANUFACTURER").text = "AEMtec"
ET.SubElement(MAPSA17, "LOCATION").text = "AEMtec"
ET.SubElement(MAPSA17, "VERSION").text = "2.0"

predefMapsa17 = ET.SubElement(MAPSA17, "PREDEFINED_ATTRIBUTES")
attr17 = ET.SubElement(predefMapsa17, "ATTRIBUTE")
ET.SubElement(attr17, "NAME").text = "Status"
ET.SubElement(attr17, "VALUE").text = "Good"

#Sensor 
child17 = ET.SubElement(MAPSA17, "CHILDREN")
child17_sub = ET.SubElement(child17, "PART", mode="auto")
ET.SubElement(child17_sub, "KIND_OF_PART").text = "PS-p Sensor"
ET.SubElement(child17_sub, "SERIAL_NUMBER").text = "|0000|0000|0000|0000|0110|0101|"
ET.SubElement(child17_sub, "NAME_LABEL").text = "35494_016_PSP_MAINL"
ET.SubElement(child17_sub, "BARCODE").text = "35494_016_PSP_MAINL"
ET.SubElement(child17_sub, "MANUFACTURER").text = "Hamamatsu"

child17_predef = ET.SubElement(child17_sub, "PREDEFINED_ATTRIBUTES")
child17_predef_attr = ET.SubElement(child17_predef, "ATTRIBUTE")
ET.SubElement(child17_predef_attr, "NAME").text = "Chip Posn on Sensor"
ET.SubElement(child17_predef_attr, "VALUE").text = "16"


###########################################################
#print xml format
xmlstr = ET.tostring(root)

dom = xml.dom.minidom.parseString(xmlstr)
xmlfinal = dom.toprettyxml(indent="  ")
print(xmlfinal)
