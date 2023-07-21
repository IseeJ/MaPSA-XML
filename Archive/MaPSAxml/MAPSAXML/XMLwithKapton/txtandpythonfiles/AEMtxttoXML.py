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



#####

txtfilename = 'AEMnamelists.txt'
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
    ET.SubElement(MAPSA, "MANUFACTURER").text = "AEMtec"
    ET.SubElement(MAPSA, "LOCATION").text = "AEMtec"
    ET.SubElement(MAPSA, "VERSION").text = "2.0"

    predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
    attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
    ET.SubElement(attr1, "NAME").text = "Status"
    ET.SubElement(attr1, "VALUE").text = "Good"
    attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
    ET.SubElement(attr2, "NAME").text = "Kapton"
    ET.SubElement(attr2, "VALUE").text = "1"
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
