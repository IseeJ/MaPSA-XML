#!/usr/bin/env python
# coding: utf-8

# # ElementTree

# In[9]:


#same as before
with open('mapsa.txt') as file:
    mapsaraw = file.read()
    filename = mapsaraw.split(',')[1]
print(filename)

with open('35494_016_PSP_MANL.txt') as file:
    myfile = file.read()
    mylines = myfile.split('\n\n')
    del mylines[16]
    
#get name label from a line
def getNameLabel(line):
    myelements = line.split(';')
    name = myelements[4][:6] + '_'+ myelements[4][6:8]
    row = myelements[4][-1:]
    col = myelements[5]
    coor = str(int(col)-9).zfill(2)
    if int(coor) < 0:
        col = abs(int(coor))
        coor =str(1)+str(col)
    return name+'_'+row+coor

#get position (convert rows,cols to 1-16)
def getPosn(line):
    myelements = line.split(';')
    MPArow, MPAcol = myelements[2], myelements[3][0:2]
    MPAcoor = MPArow+MPAcol
    
    if MPAcol == 'D1':
        MPAcoor_num = MPArow
    elif MPAcol == 'D2':
        MPAcoor_num = str(17-int(MPArow))
    return MPAcoor_num


# In[10]:


import xml.etree.ElementTree as ET
import xml.dom.minidom

root = ET.Element("ROOT")
parts = ET.SubElement(root, "PARTS")

# MaPSA block
MAPSA = ET.SubElement(parts, "PART", mode="auto") #use ElementTree to add mode='auto'
ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
ET.SubElement(MAPSA, "NAME_LABEL").text = "AEM_35494_016L"
ET.SubElement(MAPSA, "MANUFACTURER").text = "AEMtec"
ET.SubElement(MAPSA, "LOCATION").text = "AEMtec"
ET.SubElement(MAPSA, "VERSION").text = "2.0"

predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
ET.SubElement(attr1, "NAME").text = "Status"
ET.SubElement(attr1, "VALUE").text = "Good"


# In[11]:


def process(line):
    #MPA chip
    child = ET.SubElement(MAPSA, "CHILDREN")
    #Sub element of child
    child_sub = ET.SubElement(child, "PART", mode="auto")
    ET.SubElement(child_sub, "KIND_OF_PART").text = "MPA Chip"
    ET.SubElement(child_sub, "SERIAL_NUMBER").text = "Inpuit Serial Number"
    ET.SubElement(child_sub, "NAME_LABEL").text = getNameLabel(line)
    
    #Predefined attributes of child
    child_predef = ET.SubElement(child_sub, "PREDEFINED_ATTRIBUTES")
    child_predef_attr = ET.SubElement(child_predef, "ATTRIBUTE")
    ET.SubElement(child_predef_attr, "NAME").text = "Chip Posn on Sensor"
    ET.SubElement(child_predef_attr, "VALUE").text = getPosn(line)
    return child


# In[13]:


for line in mylines:
    process(line)

xmlstr = ET.tostring(root)

dom = xml.dom.minidom.parseString(xmlstr)
xmlfinal = dom.toprettyxml(indent="  ")
print(xmlfinal)


# # Dict2xml

# In[14]:


#create dictionary
final_dict = {}
final_dict['PARTS'] = {}
final_dict['PARTS']['PART mode="auto"'] = {} #doesnt work
final_dict['PARTS']['PART mode="auto"']['KIND_OF_PART'] = 'MaPSA'
final_dict['PARTS']['PART mode="auto"']['NAME_LABEL'] = mapsaraw.split(',')[0]
final_dict['PARTS']['PART mode="auto"']['MANUFACTURER'] = 'AEMtec'
final_dict['PARTS']['PART mode="auto"']['LOCATION'] = 'AEMtec'
final_dict['PARTS']['PART mode="auto"']['VERSION'] = '2.0'

final_dict['PARTS']['PART mode="auto"']['CHILDREN'] ={}

#Add to child dictionary
def process(line):
    child = {}
    child['PART'] = {}
    child['PART']['KIND_OF_PART'] = 'MPA Chip'
    child['PART']['SERIAL_NUMBER'] = {}
    child['PART']['NAME_LABEL'] = getNameLabel(line)
    child['PART']['PREDEFINED_ATTRIBUTES'] = {}
    child['PART']['PREDEFINED_ATTRIBUTES']['ATTRIBUTE']= {}
    child['PART']['PREDEFINED_ATTRIBUTES']['ATTRIBUTE']['NAME'] = 'Chip Posn on Sensor'
    child['PART']['PREDEFINED_ATTRIBUTES']['ATTRIBUTE']['VALUE'] = getPosn(line)
    return child

from dict2xml import dict2xml
for line in mylines:
    final_dict['PARTS']['PART mode="auto"']['CHILDREN'] = process(line) 
    print(dict2xml(final_dict))


# In[ ]:




