#!/usr/bin/env python
# coding: utf-8

# # AEM

# ## FINAL for multiple files

# In[3]:


import xml.etree.ElementTree as ET
import xml.dom.minidom

def AEM_mapsaname(filename):
    Mapsaname = 'AEM_'+filename[0:9]+filename[:-4][-1:]
    return Mapsaname

#Get name label
def AEM_getNameLabel(line):
    myelements = line.split(';')
    name = myelements[4][:6] + '_'+ myelements[4][6:8]
    row = myelements[4][-1:]
    col = myelements[5]
    coor = int(col)-9
    
    #col 0-9
    if 0<= int(coor) <=9:
        col = abs(int(coor))
        coor =str(col).zfill(2)
    
    #negative col 19-11 (-9 to -1)
    if int(coor) < 0:
        col = abs(int(coor))
        coor =str(1)+str(col)
        
    #col 10-13
    elif int(coor) == 10:
        coor = '0A'
    elif int(coor) == 11:
        coor = '0B'
    elif int(coor) == 12:
        coor = '0C'
    elif int(coor) == 13:
        coor = '0D'
    return name+'_'+row+coor

#get position (convert rows,cols to 1-16)
def AEM_getPosn(line):
    myelements = line.split(';')
    MPArow, MPAcol = myelements[2], myelements[3][0:2]
    MPAcoor = MPArow+MPAcol
    
    if MPAcol == 'D1':
        MPAcoor_num = MPArow
    elif MPAcol == 'D2':
        MPAcoor_num = str(17-int(MPArow))
    return MPAcoor_num

def addsensor(filename):
    sensor_sub = ET.SubElement(child, "PART", mode="auto")
    ET.SubElement(sensor_sub, "KIND_OF_PART").text = "PS-p Sensor"
    ET.SubElement(sensor_sub, "NAME_LABEL").text = filename[:-4]
    print(filename)
    return sensor_sub


print('Enter LOCATION:')
Loc = input()

#####input txt file that contains filename lists
txtfilename = 'AEMnamelists.txt'
#####

filename_list = []
with open(txtfilename) as file:
    AEMlist = file.read()
    filename = AEMlist.split('\n')
    for line in filename:
        filename_list.append(line)

for filename in filename_list:
    with open(filename) as file:
        myfile = file.read()
        mylines = myfile.split('\n')
        del mylines[16]

    root = ET.Element("ROOT")
    parts = ET.SubElement(root, "PARTS")

# MaPSA block
    MAPSA = ET.SubElement(parts, "PART", mode="auto") #use ElementTree to add mode='auto'
    ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
    ET.SubElement(MAPSA, "NAME_LABEL").text = AEM_mapsaname(filename)
    ET.SubElement(MAPSA, "MANUFACTURER").text = Loc
    ET.SubElement(MAPSA, "LOCATION").text = Loc
    ET.SubElement(MAPSA, "VERSION").text = "2.0"

    predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
    attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
    ET.SubElement(attr1, "NAME").text = "Status"
    ET.SubElement(attr1, "VALUE").text = "Good"
    """
    attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
    ET.SubElement(attr2, "NAME").text = "Kapton"
    ET.SubElement(attr2, "VALUE").text = "1"
    """
    child = ET.SubElement(MAPSA, "CHILDREN")
    for line in mylines:
        child_sub = ET.SubElement(child, "PART", mode="auto")
        ET.SubElement(child_sub, "KIND_OF_PART").text = "MPA Chip"
        ET.SubElement(child_sub, "NAME_LABEL").text = AEM_getNameLabel(line)
        child_predef = ET.SubElement(child_sub, "PREDEFINED_ATTRIBUTES")
        child_predef_attr = ET.SubElement(child_predef, "ATTRIBUTE")
        ET.SubElement(child_predef_attr, "NAME").text = "Chip Posn on Sensor"
        ET.SubElement(child_predef_attr, "VALUE").text = AEM_getPosn(line)   
     
    addsensor(filename)
    xmlstr = ET.tostring(root)
    dom = xml.dom.minidom.parseString(xmlstr)
    xmlfinal = dom.toprettyxml(indent="   ")
    print(xmlfinal)
    
    ET.indent(ET.ElementTree(root),'   ')
    aem = open(AEM_mapsaname(filename)+'.xml', "wb")
    ET.ElementTree(root).write(aem)
    


# In[ ]:





# In[ ]:





# In[ ]:


import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import pandas as pd


#for AEM
def AEM_mapsaname(filename):
    Mapsaname = 'AEM_'+filename[0:9]+filename[:-4][-1:]
    return Mapsaname

#Get name label
def AEM_getNameLabel(line):
    myelements = line.split(';')
    name = myelements[4][:6] + '_'+ myelements[4][6:8]
    row = myelements[4][-1:]
    col = myelements[5]
    coor = int(col)-9
    
    #col 0-9
    if 0<= int(coor) <=9:
        col = abs(int(coor))
        coor =str(col).zfill(2)
    
    #negative col 19-11 (-9 to -1)
    if int(coor) < 0:
        col = abs(int(coor))
        coor =str(1)+str(col)
        
    #col 10-13
    elif int(coor) == 10:
        coor = '0A'
    elif int(coor) == 11:
        coor = '0B'
    elif int(coor) == 12:
        coor = '0C'
    elif int(coor) == 13:
        coor = '0D'
    return name+'_'+row+coor

#get position (convert rows,cols to 1-16)
def AEM_getPosn(line):
    myelements = line.split(';')
    MPArow, MPAcol = myelements[2], myelements[3][0:2]
    MPAcoor = MPArow+MPAcol
    
    if MPAcol == 'D1':
        MPAcoor_num = MPArow
    elif MPAcol == 'D2':
        MPAcoor_num = str(17-int(MPArow))
    return MPAcoor_num


#####input txt file that contains filename lists
txtfilename = 'AEMnamelists.txt'
#####

def AEMtoXML(txtfilename):
    filename_list = []
    with open(txtfilename) as file:
        AEMlist = file.read()
        filename = AEMlist.split('\n')
        for line in filename:
            filename_list.append(line)

    for filename in filename_list:
        with open(filename) as file:
            myfile = file.read()
            mylines = myfile.split('\n')
            del mylines[16]

        root = ET.Element("ROOT")
        parts = ET.SubElement(root, "PARTS")

# MaPSA block
        MAPSA = ET.SubElement(parts, "PART", mode="auto") #use ElementTree to add mode='auto'
        ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
        ET.SubElement(MAPSA, "NAME_LABEL").text = AEM_mapsaname(filename)
        ET.SubElement(MAPSA, "MANUFACTURER").text = Loc
        ET.SubElement(MAPSA, "LOCATION").text = Loc
        ET.SubElement(MAPSA, "VERSION").text = "2.0"
        ET.SubElement(MAPSA, "VERSION").text = "2.0"
        
        predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
        attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr1, "NAME").text = "Status"
        ET.SubElement(attr1, "VALUE").text = "Good"
        """
        attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr2, "NAME").text = "Kapton"
        ET.SubElement(attr2, "VALUE").text = "1"
        """
        child = ET.SubElement(MAPSA, "CHILDREN")
        for line in mylines:
            child_sub = ET.SubElement(child, "PART", mode="auto")
            ET.SubElement(child_sub, "KIND_OF_PART").text = "MPA Chip"
            ET.SubElement(child_sub, "NAME_LABEL").text = AEM_getNameLabel(line)
            child_predef = ET.SubElement(child_sub, "PREDEFINED_ATTRIBUTES")
            child_predef_attr = ET.SubElement(child_predef, "ATTRIBUTE")
            ET.SubElement(child_predef_attr, "NAME").text = "Chip Posn on Sensor"
            ET.SubElement(child_predef_attr, "VALUE").text = AEM_getPosn(line)   
     
        sensor_sub = ET.SubElement(child, "PART", mode="auto")
        ET.SubElement(sensor_sub, "KIND_OF_PART").text = "PS-p Sensor"
        ET.SubElement(sensor_sub, "NAME_LABEL").text = filename[:-4]
        
        xmlstr = ET.tostring(root)
        dom = xml.dom.minidom.parseString(xmlstr)
        xmlfinal = dom.toprettyxml(indent="   ")
        print(xmlfinal)
        
        """
        ET.indent(ET.ElementTree(root),'   ')
        aem = open(AEM_mapsaname(filename)+'.xml', "wb")
        ET.ElementTree(root).write(aem)
        """
        
#for HPK
def getHPKdata(filename):
    chip_data = pd.read_csv(filename+".csv", names = ['number', 'location','WaffelPackno','WaffelPackrow','WaffelPackcol', 'WaferID','Waferrow','Wafercol','BINcode'])
    return chip_data

def getMapsaName(filename):
    return 'HPK_'+filename[0:9]+filename[-1:]

def HPK_getPosn(num):
    if num>8:
        Posn=25-num
    else:
        Posn=num
    return Posn

def HPK_Kapval(name):
    noKap = ["HPK_35494_032L","HPK_35494_033L","HPK_35494_040L","HPK_35494_041L","HPK_35494_042L","HPK_35494_36L","HPK_35494_37L","HPK_35494_38L","HPK_35494_39L"]
    if name in noKap:
        value = 0
    else:
        value = 1
    return value

def HPK_getNameLabel(chip_data, no):
    name = chip_data['WaferID'][no][:6] + '_'+  chip_data['WaferID'][no][6:8]
    row = abs(chip_data['Waferrow'][no])
    col = chip_data['Wafercol'][no]
    coor = str(int(col)-9).zfill(2)
    if int(coor) < 0:
        col = abs(int(coor))
        coor =str(1)+str(col)
    return str(name)+'_'+str(row)+coor

#HPK split
def HPK_split(sheetname):
    with open(sheetname, 'r') as file:
        raw = file.read()
        raw = raw.strip(raw[0:115])
    rows = raw.split('\n')
    delim = str(rows[1].split(',')[0].split('_')[0]) #use 35494 as delimeter
    sections = re.split(delim, raw)
    sections.pop(0)
    filename_list = []

    for section in sections:
        data = delim+section
        filename = data.split(',')[0]
        filename_list.append(filename)
        with open(filename + '.csv', 'w') as output_file:
            output_file.write(data)
    #print(filename_list)
    return filename_list

#for HPK sheet 
def HPKtoXML(sheetname):
    filename_list = HPK_split(sheetname) #split,save csv files
    for filename in filename_list:
        chip_data = getHPKdata(filename)
       
        root = ET.Element("ROOT")
        parts = ET.SubElement(root, "PARTS")

        # MaPSA block
        MAPSA = ET.SubElement(parts, "PART", mode="auto") #use ElementTree to add mode='auto'
        ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
        ET.SubElement(MAPSA, "NAME_LABEL").text = getMapsaName(filename)
        ET.SubElement(MAPSA, "MANUFACTURER").text = Loc
        ET.SubElement(MAPSA, "LOCATION").text = Loc
        ET.SubElement(MAPSA, "VERSION").text = "2.0"
    
        predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
        attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr1, "NAME").text = "Status"
        ET.SubElement(attr1, "VALUE").text = "Good"
        
        #Kapton block
        attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr2, "NAME").text = "Kapton"
        ET.SubElement(attr2, "VALUE").text = str(HPK_Kapval(getMapsaName(filename)))
        #print(str(Kapval(getMapsaName(filename))))
        
        child = ET.SubElement(MAPSA, "CHILDREN")
    
        df = getHPKdata(filename)
        for index, row in df.iterrows():
            child_sub = ET.SubElement(child, "PART", mode="auto")
            ET.SubElement(child_sub, "KIND_OF_PART").text = "MPA Chip"
            ET.SubElement(child_sub, "NAME_LABEL").text = str(HPK_getNameLabel(chip_data, index))
            #Predefined attributes of child
            child_predef = ET.SubElement(child_sub, "PREDEFINED_ATTRIBUTES")
            child_predef_attr = ET.SubElement(child_predef, "ATTRIBUTE")
            ET.SubElement(child_predef_attr, "NAME").text = "Chip Posn on Sensor"
            ET.SubElement(child_predef_attr, "VALUE").text = str(HPK_getPosn(row['location']))

    
        sensor_sub = ET.SubElement(child, "PART", mode="auto")
        ET.SubElement(sensor_sub, "KIND_OF_PART").text = "PS-p Sensor"
        ET.SubElement(sensor_sub, "NAME_LABEL").text = chip_data['number'][0]
        xmlstr = ET.tostring(root)
        dom = xml.dom.minidom.parseString(xmlstr)
        xmlfinal = dom.toprettyxml(indent="   ")
        
        print(xmlfinal)
        """
        ET.indent(ET.ElementTree(root),'   ')
        f = open(getMapsaName(filename)+'.xml', "wb")
        ET.ElementTree(root).write(f)
        print(getMapsaName(filename))
        """
    return 


Loc = input('Enter LOCATION:')
filename = input('Enter txt file with filenamelist:')
if Loc == 'AEMtec':
    AEMtoXML(filename)
elif Loc == 'Hamamatsu':
    HPKtoXML(filename)


# In[11]:





# In[ ]:




