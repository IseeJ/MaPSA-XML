# required packages
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
    coordict = {10:'0A',11:'0B',12:'0C',13:'0D'}
    #col 0-9
    if 0<= int(coor) <=9:
        col = abs(int(coor))
        coor =str(col).zfill(2)
    
    #negative col 19-11 (-9 to -1)
    elif int(coor) < 0:
        col = abs(int(coor))
        coor =str(1)+str(col)
    #ABCD col
    elif coor in coordict:
        coor = str(coordict[coor])

    return name+'_'+str(row)+str(coor)

#get position (convert rows,cols to 1-16)
def AEM_getPosn(line):
    myelements = line.split(';')
    MPArow, MPAcol = myelements[2], myelements[3][0:2]
    
    if MPAcol == 'D1':
        MPAcoor_num = MPArow
    elif MPAcol == 'D2':
        MPAcoor_num = str(17-int(MPArow))
    return MPAcoor_num

def AEM_getfilename(txtfilename):
    filename_list = []
    with open(txtfilename) as file:
        AEMlist = file.read()
        filename = AEMlist.split('\n')
        for line in filename:
            filename_list.append(line)
    return filename_list

def AEM_Kapval(name):
    noKap = ["AEM_35494_079L","AEM_35494_078L","AEM_35494_077L","AEM_35494_007L","AEM_35494_008L","AEM_35494_002L"]
    if name in noKap:
        value = "No"
    else:
        value = "Yes"
    return value

def AEMtoXML(filename):
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

    # MaPSA attributes
    predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
    attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
    ET.SubElement(attr1, "NAME").text = "Has Kapton isolation"
    ET.SubElement(attr1, "VALUE").text = AEM_Kapval(AEM_mapsaname(filename))       
    
    attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
    ET.SubElement(attr2, "NAME").text = "Grade"
    ET.SubElement(attr2, "VALUE").text = "A"
        
    #Rework candidate
    attr3 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
    ET.SubElement(attr3, "NAME").text = "Status"
    if filename in ["ReworkCandidateNames"]:
        ET.SubElement(attr3, "VALUE").text = "Needs repair"
    else:
        ET.SubElement(attr3, "VALUE").text = {}
    

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
         
    ET.indent(ET.ElementTree(root),'   ')
    aem = open(AEM_mapsaname(filename)+'.xml', "wb")
    ET.ElementTree(root).write(aem)


############################################################################
#for HPK first data set

def getHPKdata1(filename):
    chip_data = pd.read_csv(filename+".csv", names = ['number', 'location','WaffelPackno','WaffelPackrow','WaffelPackcol', 'WaferID','Waferrow','Wafercol','BINcode'])
    return chip_data

def HPK_MapsaName(filename):
    return 'HPK_'+filename[0:9]+filename[-1:]

def HPK_getPosn1(num):
    if num>8:
        Posn=25-num
    else:
        Posn=num
    return Posn

def HPK_Kapval1(name):
    noKap = ["HPK_35494_032L","HPK_35494_033L","HPK_35494_040L","HPK_35494_041L","HPK_35494_042L","HPK_35494_036L","HPK_35494_037L","HPK_35494_038L","HPK_35494_039L"]
    if name in noKap:
        value = "No"
    else:
        value = "Yes"
    return value

def HPK_getNameLabel1(chip_data, no):
    name = chip_data['WaferID'][no][:6] + '_'+  chip_data['WaferID'][no][6:8]
    row = abs(chip_data['Waferrow'][no])
    col = chip_data['Wafercol'][no]
    coor = int(col)-9
    coordict = {10:'0A',11:'0B',12:'0C',13:'0D'}
    #col 0-9
    if 0<= int(coor) <=9:
        col = abs(int(coor))
        coor =str(col).zfill(2)
    #negative col 19-11 (-9 to -1)
    elif int(coor) < 0:
        col = abs(int(coor))
        coor =str(1)+str(col)
    #ABCD col
    elif coor in coordict:
        coor = str(coordict[coor])
    return str(name)+'_'+str(row)+coor

#HPK split
def HPK_split1(sheetname):
    with open(sheetname, 'r') as file:
        raw = file.read()[116:]
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
def HPK_getXML1(sheetname):
    filename_list = HPK_split1(sheetname) #split,save csv files
    for filename in filename_list:
        chip_data = getHPKdata1(filename)
       
        root = ET.Element("ROOT")
        parts = ET.SubElement(root, "PARTS")

        # MaPSA block
        MAPSA = ET.SubElement(parts, "PART", mode="auto") #use ElementTree to add mode='auto'
        ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
        ET.SubElement(MAPSA, "NAME_LABEL").text = HPK_MapsaName(filename)
        ET.SubElement(MAPSA, "MANUFACTURER").text = "Hamamatsu"
        ET.SubElement(MAPSA, "LOCATION").text = "Hamamatsu"
        ET.SubElement(MAPSA, "VERSION").text = "2.0"

        # MaPSA attributes
        predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
        attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr1, "NAME").text = "Has Kapton isolation"
        ET.SubElement(attr1, "VALUE").text = HPK_Kapval1(HPK_MapsaName(filename))
        
        attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr2, "NAME").text = "Grade"
        ET.SubElement(attr2, "VALUE").text = "A"
        
        #Rework candidate
        attr3 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr3, "NAME").text = "Status"
        if filename in ["ReworkCandidateNames"]:
            ET.SubElement(attr3, "VALUE").text = "Needs repair"
        else:
            ET.SubElement(attr3, "VALUE").text = {}
        
        #Kapton block
        #attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        #ET.SubElement(attr2, "NAME").text = "Kapton"
        #ET.SubElement(attr2, "VALUE").text = str(HPK_Kapval(getMapsaName(filename)))
        #print(str(Kapval(getMapsaName(filename))))
        
        child = ET.SubElement(MAPSA, "CHILDREN")
    
        df = getHPKdata1(filename)
        for index, row in df.iterrows():
            child_sub = ET.SubElement(child, "PART", mode="auto")
            ET.SubElement(child_sub, "KIND_OF_PART").text = "MPA Chip"
            ET.SubElement(child_sub, "NAME_LABEL").text = str(HPK_getNameLabel1(chip_data, index))
            #Predefined attributes of child
            child_predef = ET.SubElement(child_sub, "PREDEFINED_ATTRIBUTES")
            child_predef_attr = ET.SubElement(child_predef, "ATTRIBUTE")
            ET.SubElement(child_predef_attr, "NAME").text = "Chip Posn on Sensor"
            ET.SubElement(child_predef_attr, "VALUE").text = str(HPK_getPosn1(row['location']))

    
        sensor_sub = ET.SubElement(child, "PART", mode="auto")
        ET.SubElement(sensor_sub, "KIND_OF_PART").text = "PS-p Sensor"
        ET.SubElement(sensor_sub, "NAME_LABEL").text = chip_data['number'][0]
        xmlstr = ET.tostring(root)
        dom = xml.dom.minidom.parseString(xmlstr)
        xmlfinal = dom.toprettyxml(indent="   ")
        
        print(xmlfinal)
        
        ET.indent(ET.ElementTree(root),'   ')
        f = open(HPK_MapsaName(filename)+'.xml', "wb")
        ET.ElementTree(root).write(f)
        print(HPK_MapsaName(filename))
    return 

########################################################################
#for HPK missing data
"""
MPA2_Remap = {
    1: "000", 2: "001", 3: "002", 4: "003", 5: "004",
    6: "109", 7: "108", 8: "107", 9: "106", 10: "105", 11: "104", 12: "103", 13: "102", 14: "101", 15: "100", 16: "111", 17: "112", 18: "113", 19: "114", 20: "115", 21: "217",
    22: "216", 23: "215", 24: "214", 25: "213", 26: "212", 27: "211", 28: "200", 29: "201", 30: "202", 31: "203", 32: "204", 33: "205", 34: "206", 35: "207", 36: "208", 37: "209", 38: "20a", 39: "20b", 40: "30c",
    41: "30b", 42: "30a", 43: "309", 44: "308", 45: "307", 46: "306", 47: "305", 48: "304", 49: "303", 50: "302", 51: "301", 52: "300", 53: "311", 54: "312", 55: "313", 56: "314", 57: "315", 58: "316", 59: "317", 60: "318",
    61: "419", 62: "418", 63: "417", 64: "416", 65: "415", 66: "414", 67: "413", 68: "412", 69: "411", 70: "400", 71: "401", 72: "402", 73: "403", 74: "404", 75: "405", 76: "406", 77: "407", 78: "408", 79: "409", 80: "40a", 81: "40b", 82: "40c", 83: "40d",
    84: "50d", 85: "50c", 86: "50b", 87: "50a", 88: "509", 89: "508", 90: "507", 91: "506", 92: "505", 93: "504", 94: "503", 95: "502", 96: "501", 97: "500", 98: "511", 99: "512", 100: "513", 101: "514", 102: "515", 103: "516", 104: "517", 105: "518", 106: "519",
    107: "619", 108: "618", 109: "617", 110: "616", 111: "615", 112: "614", 113: "613", 114: "612", 115: "611", 116: "600", 117: "601", 118: "602", 119: "603", 120: "604", 121: "605", 122: "606", 123: "607", 124: "608", 125: "609", 126: "60a", 127: "60b", 128: "60c", 129: "60d",
    130: "70c", 131: "70b", 132: "70a", 133: "709", 134: "708", 135: "707", 136: "706", 137: "705", 138: "704", 139: "703", 140: "702", 141: "701", 142: "700", 143: "711", 144: "712", 145: "713", 146: "714", 147: "715", 148: "716", 149: "717", 150: "718",
    151: "817", 152: "816", 153: "815", 154: "814", 155: "813", 156: "812", 157: "811", 158: "800", 159: "801", 160: "802", 161: "803", 162: "804", 163: "805", 164: "806", 165: "807", 166: "808", 167: "809", 168: "80a", 169: "80b",
    170: "908", 171: "907", 172: "906", 173: "905", 174: "904", 175: "903", 176: "902", 177: "901", 178: "900", 179: "911", 180: "912", 181: "913", 182: "914",
    183: "a00", 184: "a01", 185: "a02", 186: "a03", 187: "a04"}
"""

MPA2_Remap = {
    1: "000", 2: "001", 3: "002", 4: "003", 5: "004",
    6: "109", 7: "108", 8: "107", 9: "106", 10: "105", 11: "104", 12: "103", 13: "102", 14: "101", 15: "100", 16: "111", 17: "112", 18: "113", 19: "114", 20: "115", 21: "217",
    22: "216", 23: "215", 24: "214", 25: "213", 26: "212", 27: "211", 28: "200", 29: "201", 30: "202", 31: "203", 32: "204", 33: "205", 34: "206", 35: "207", 36: "208", 37: "209", 38: "20A", 39: "20B", 40: "30C",
    41: "30B", 42: "30A", 43: "309", 44: "308", 45: "307", 46: "306", 47: "305", 48: "304", 49: "303", 50: "302", 51: "301", 52: "300", 53: "311", 54: "312", 55: "313", 56: "314", 57: "315", 58: "316", 59: "317", 60: "318",
    61: "419", 62: "418", 63: "417", 64: "416", 65: "415", 66: "414", 67: "413", 68: "412", 69: "411", 70: "400", 71: "401", 72: "402", 73: "403", 74: "404", 75: "405", 76: "406", 77: "407", 78: "408", 79: "409", 80: "40A", 81: "40B", 82: "40C", 83: "40D",
    84: "50D", 85: "50C", 86: "50B", 87: "50A", 88: "509", 89: "508", 90: "507", 91: "506", 92: "505", 93: "504", 94: "503", 95: "502", 96: "501", 97: "500", 98: "511", 99: "512", 100: "513", 101: "514", 102: "515", 103: "516", 104: "517", 105: "518", 106: "519",
    107: "619", 108: "618", 109: "617", 110: "616", 111: "615", 112: "614", 113: "613", 114: "612", 115: "611", 116: "600", 117: "601", 118: "602", 119: "603", 120: "604", 121: "605", 122: "606", 123: "607", 124: "608", 125: "609", 126: "60A", 127: "60B", 128: "60C", 129: "60D",
    130: "70C", 131: "70B", 132: "70A", 133: "709", 134: "708", 135: "707", 136: "706", 137: "705", 138: "704", 139: "703", 140: "702", 141: "701", 142: "700", 143: "711", 144: "712", 145: "713", 146: "714", 147: "715", 148: "716", 149: "717", 150: "718",
    151: "817", 152: "816", 153: "815", 154: "814", 155: "813", 156: "812", 157: "811", 158: "800", 159: "801", 160: "802", 161: "803", 162: "804", 163: "805", 164: "806", 165: "807", 166: "808", 167: "809", 168: "80A", 169: "80B",
    170: "908", 171: "907", 172: "906", 173: "905", 174: "904", 175: "903", 176: "902", 177: "901", 178: "900", 179: "911", 180: "912", 181: "913", 182: "914",
    183: "A00", 184: "A01", 185: "A02", 186: "A03", 187: "A04"}

#functions
def getHPKdata(filename):
    chip_data = pd.read_csv(filename+".csv")
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
    noKap = ["HPK_35494_032L","HPK_35494_033L","HPK_35494_040L","HPK_35494_041L","HPK_35494_042L","HPK_35494_036L","HPK_35494_037L","HPK_35494_38L","HPK_35494_039L"]
    if name in noKap:
        value = "No"
    else:
        value = "Yes"
    return value

def HPK_getNameLabel(chip_data, no):
    name = chip_data['WaffelNumber'][no]
    coor = MPA2_Remap.get( chip_data['ChipNumber'][no])
    return str(name)+'_'+str(coor)


#HPK split files (split every 16 rows)
def HPK_split(sheetname):
    raw = pd.read_csv(sheetname, names = ['Name', 'Posn','WaffelPackno','WaffelNumber','ChipNumber'])
    data = pd.DataFrame(raw).tail(-1)
    filename_list = data.dropna()['Name'].tolist()
    print(filename_list)

    k = len(filename_list)
    size = 16 #16 MPA chips
    
    for i in range(k):
        df = data[size*i:size*(i+1)]
        df.to_csv(filename_list[i]+'.csv', index=False) #reset index values
    return filename_list

#for HPK sheet 
def HPK_getXML2(sheetname):
    filename_list = HPK_split(sheetname) #split,save csv files
    for filename in filename_list:
        chip_data = getHPKdata(filename)
       
        root = ET.Element("ROOT")
        parts = ET.SubElement(root, "PARTS")

        # MaPSA block
        MAPSA = ET.SubElement(parts, "PART", mode="auto") #use ElementTree to add mode='auto'
        ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
        ET.SubElement(MAPSA, "NAME_LABEL").text = getMapsaName(filename)
        ET.SubElement(MAPSA, "MANUFACTURER").text = "Hamamatsu"
        ET.SubElement(MAPSA, "LOCATION").text = "Hamamatsu"
        ET.SubElement(MAPSA, "VERSION").text = "2.0"
        
        # MaPSA attributes
        predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
        attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr1, "NAME").text = "Has Kapton isolation"
        ET.SubElement(attr1, "VALUE").text = HPK_Kapval(getMapsaName(filename))
        
        attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr2, "NAME").text = "Grade"
        ET.SubElement(attr2, "VALUE").text = "A"
        
        #Rework candidate
        attr3 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr3, "NAME").text = "Status"
        if filename in ["ReworkCandidateNames"]:
            ET.SubElement(attr3, "VALUE").text = "Needs repair"
        else:
            ET.SubElement(attr3, "VALUE").text = {}
        
        
        #Kapton block
        #attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        #ET.SubElement(attr2, "NAME").text = "Kapton"
        #ET.SubElement(attr2, "VALUE").text = str(HPK_Kapval(getMapsaName(filename)))
        
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
            ET.SubElement(child_predef_attr, "VALUE").text = str(HPK_getPosn(row['Posn']))

    
        sensor_sub = ET.SubElement(child, "PART", mode="auto")
        ET.SubElement(sensor_sub, "KIND_OF_PART").text = "PS-p Sensor"
        ET.SubElement(sensor_sub, "NAME_LABEL").text = chip_data['Name'][0]
        xmlstr = ET.tostring(root)
        dom = xml.dom.minidom.parseString(xmlstr)
        xmlfinal = dom.toprettyxml(indent="   ")
        
        print(xmlfinal)
        
        ET.indent(ET.ElementTree(root),'   ')
        f = open(getMapsaName(filename)+'.xml', "wb")
        ET.ElementTree(root).write(f)
        print(getMapsaName(filename))
        
        
    return 

Loc = input('Enter LOCATION:')
Loc_dict = {'H':'Hamamatsu','A':'AEMtec'}
Loc = Loc_dict[Loc]

filename = input('Enter txt file with filenamelist:')
file_dict = {'A':'AEMnamelists.txt','B': 'MissingAEM.csv' ,'C':'HPKSheet1.csv', 'D':'hpk2.csv'}
filename = file_dict[filename]

if Loc == 'AEMtec':
    typeoffile = input('Is the input file in txt? [y/n]')
    if  typeoffile == 'y':
        filename_list = AEM_getfilename(filename)
        for filename in filename_list:
            AEMtoXML(filename)
    elif typeoffile == 'n':
        AEM_csvgetXML(filename)
    
elif Loc == 'Hamamatsu':
    Chipnum = input('Is the chip name in rows, cols? [y/n]')
    if Chipnum == 'y':
        HPK_getXML1(filename)
    elif Chipnum == 'n':
        HPK_getXML2(filename)
