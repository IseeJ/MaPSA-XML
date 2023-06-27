#!/usr/bin/env python
# coding: utf-8

# In[1]:


#same as before
with open('mapsa.txt') as file:
    mapsaraw = file.read()
    filename = mapsaraw.split(',')[1]
print(filename)

with open('35494_016_PSP_MAINL.txt') as file:
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


# # ElementTree

# In[2]:


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

def process(line):
    #MPA chip
    child = ET.SubElement(MAPSA, "CHILDREN")
    #Sub element of child
    child_sub = ET.SubElement(child, "PART", mode="auto")
    ET.SubElement(child_sub, "KIND_OF_PART").text = "MPA Chip"
    ET.SubElement(child_sub, "SERIAL_NUMBER").text = "Input Serial Number"
    ET.SubElement(child_sub, "NAME_LABEL").text = getNameLabel(line)
    
    #Predefined attributes of child
    child_predef = ET.SubElement(child_sub, "PREDEFINED_ATTRIBUTES")
    child_predef_attr = ET.SubElement(child_predef, "ATTRIBUTE")
    ET.SubElement(child_predef_attr, "NAME").text = "Chip Posn on Sensor"
    ET.SubElement(child_predef_attr, "VALUE").text = getPosn(line)
    return child


#Sensor block
def addsensor(filename):
    sensor = ET.SubElement(MAPSA, "CHILDREN")
    sensor_sub = ET.SubElement(sensor, "PART", mode="auto")
    ET.SubElement(sensor_sub, "KIND_OF_PART").text = "PS-p Sensor"
    ET.SubElement(sensor_sub, "SERIAL_NUMBER").text = "|0000|0000|0000|0000|0110|0101|"
    ET.SubElement(sensor_sub, "NAME_LABEL").text = filename[:-4]
    ET.SubElement(sensor_sub, "Barcode").text = filename[:-4]
    ET.SubElement(sensor_sub, "MANUFACTURER").text = 'Hamamatsu'
    return sensor


#Create xml
for line in mylines:
    process(line)
addsensor(filename)

xmlstr = ET.tostring(root)
dom = xml.dom.minidom.parseString(xmlstr)
xmlfinal = dom.toprettyxml(indent="  ")
print(xmlfinal)


# # Dict2xml

# In[8]:


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

#Sensor block
def addsensor(filename):
    child = {}
    child['PART'] = {}
    child['PART']['KIND_OF_PART'] = 'PS-p sensor'
    child['PART']['SERIAL_NUMBER'] = '|0000|0000|0000|0000|0110|0101|'
    child['PART']['NAME_LABEL'] =  filename[:-4]
    child['PART']['BARCODE'] =  filename[:-4]
    child['PART']['MANUFACTURER'] =  'Hamamatsu'
    return child

from dict2xml import dict2xml
for line in mylines:
    final_dict['PARTS']['PART mode="auto"']['CHILDREN'] = process(line) 
    print(dict2xml(final_dict))
    
final_dict['PARTS']['PART mode="auto"']['CHILDREN'] = addsensor(filename)
print(dict2xml(final_dict))


# In[ ]:





# In[ ]:




