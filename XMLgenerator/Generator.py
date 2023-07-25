
# required packages
import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import pandas as pd


GradeB = ['AEM_35494_015L', 'AEM_35494_016L', 'AEM_35494_027L', 'HPK_35494_003R','HPK_35494_032L','HPK_35494_033L','HPK_35494_044L']
GradeC = ['AEM_35494_002L','AEM_35494_008L', 'HPK_35494_002R','HPK_35494_005R']

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
    with open('/uscms/home/wjaidee/nobackup/MaPSA_database/XMLgenerator/'+txtfilename) as file:
        AEMlist = file.read()
        filename = AEMlist.split('\n')
        for line in filename:
            filename_list.append(line)
        print(filename_list)
    return filename_list

def AEM_Kapval(name):
    noKap = ["AEM_35494_079L","AEM_35494_078L","AEM_35494_077L","AEM_35494_007L","AEM_35494_008L","AEM_35494_002L"]
    if name in noKap:
        value = "No"
    else:
        value = "Yes"
    return value

def AEMtoXML(filename):
    with open('/uscms/home/wjaidee/nobackup/MaPSA_database/'+filename) as file:
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
    
#    GradeB = ['AEM_35494_015L', 'AEM_35494_016L', 'AEM_35494_027L', 'HPK_35494_003R','HPK_35494_032L','HPK_35494_033L','HPK_35494_044L']
#    GradeC = ['AEM_35494_002L','AEM_35494_008L', 'HPK_35494_002R','HPK_35494_005R']
 
    attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
    ET.SubElement(attr2, "NAME").text = "Grade"
    if AEM_mapsaname(filename) in GradeB:
        Grade = 'B'
    elif AEM_mapsaname(filename) in GradeC:
        Grade = 'C'
    else:
        Grade = 'A'
    ET.SubElement(attr2, "VALUE").text = Grade
        
    #Rework candidate
    attr3 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
    ET.SubElement(attr3, "NAME").text = "Status"
    if filename in ["ReworkCandidateNames"]:
        ET.SubElement(attr3, "VALUE").text = "Needs repair"
    else:
        ET.SubElement(attr3, "VALUE").text = "Good"
    

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
    
    print(AEM_mapsaname(filename))
    ET.indent(ET.ElementTree(root),'   ')
    aem = open('/uscms/home/wjaidee/nobackup/MaPSA_database/XMLgenerator/XMLnew/'+AEM_mapsaname(filename)+'.xml', "wb")
    ET.ElementTree(root).write(aem)


############################################################################

#for AEM second data set (csv, no file names)
file = 'MissingAEM.csv'
import pandas as pd

def AEM_split(sheetname):
    MapSub = {'1':'AEM_35494_002L','2': 'AEM_35494_030L', '3':'AEM_35494_029L', '4':'AEM_35494_028L'}
    raw = pd.read_csv(sheetname, names = ['No.', 'Module','Bondposition','MPA','Wafer ID','Row','Column','Bin'])
    data = pd.DataFrame(raw).tail(-1)
    k= int(len(data)/16)
    print(k)
    size = 16 #16 MPA chips
    
    for i in range(k):
        df = data[size*i:size*(i+1)]
        df.to_csv('/uscms/home/wjaidee/nobackup/MaPSA_database/'+MapSub[str(i+1)]+'.csv', index=False) 
        print(df)
    return 
    
def getName(chip_data, no):
    name = chip_data['Wafer ID'][no][:6] + '_'+  chip_data['Wafer ID'][no][6:8]
    row = abs(int(chip_data['Row'][no]))
    col = chip_data['Column'][no]
    coor = str(int(col)-9).zfill(2)
    if int(coor) < 0:
        col = abs(int(coor))
        coor =str(1)+str(col)
    return str(name)+'_'+str(row)+coor

def getPosn(data, no):
    mod = data['Module'][no]
    D = data['Bondposition'][no][0:2]
    if D == 'D2':
        Posn = 17 - int(mod)
    else: 
        Posn = mod
    return Posn

def AEM_Kapval(name):
    noKap = ["AEM_35494_079L","AEM_35494_078L","AEM_35494_077L","AEM_35494_007L","AEM_35494_008L","AEM_35494_002L"]
    if name in noKap:
        value = "No"
    else:
        value = "Yes"
    return value

    
def AEM_csvgetXML(file):
    data = pd.read_csv(file)
    data = pd.read_csv(file, names= ['No.', 'Module', 'Bondposition', 'MPA','Wafer ID', 'Row', 'Column', 'Bin'])
    df = pd.DataFrame(data)
    df = df.tail(-1)
    grouped = df.groupby('No.')
    AEM_split(file)
    group_dict = {}
    for group_name, group_data in grouped:
        group_data = group_data.reset_index(drop=True)
        group_dict[f'Data{group_name}'] = group_data

    Data1 = group_dict['Data1']
    Data2 = group_dict['Data2']
    Data3 = group_dict['Data3']
    Data4 = group_dict['Data4']

    datalist = [Data1, Data2, Data3, Data4]
    MapSub = {'1':'AEM_35494_002L','2': 'AEM_35494_030L', '3':'AEM_35494_029L', '4':'AEM_35494_028L'}

    for data in datalist:
        Mapsaname = MapSub.get(str(data['No.'][0]))
        df= pd.DataFrame(data)
        root = ET.Element("ROOT")
        parts = ET.SubElement(root, "PARTS")

        # MaPSA block
        MAPSA = ET.SubElement(parts, "PART", mode="auto") #use ElementTree to add mode='auto'
        ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
        ET.SubElement(MAPSA, "NAME_LABEL").text = Mapsaname
        ET.SubElement(MAPSA, "MANUFACTURER").text = "AEMtec"
        ET.SubElement(MAPSA, "LOCATION").text = "AEMtec"
        ET.SubElement(MAPSA, "VERSION").text = "2.0"

        predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
        attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr1, "NAME").text = "Has Kapton isolation"
        ET.SubElement(attr1, "VALUE").text = AEM_Kapval(Mapsaname)       
    
        attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        GradeB = ['AEM_35494_015L', 'AEM_35494_016L', 'AEM_35494_027L', 'HPK_35494_003R','HPK_35494_032L','HPK_35494_033L','HPK_35494_044L']
        GradeC = ['AEM_35494_002L','AEM_35494_008L', 'HPK_35494_002R','HPK_35494_005R']
        ET.SubElement(attr2, "NAME").text = "Grade"
        if Mapsaname in GradeB:
            Grade = 'B'
        elif Mapsaname in GradeC:
            Grade = 'C'
        else:
            Grade = 'A'
        ET.SubElement(attr2, "VALUE").text = Grade
        
        
        #Rework candidate
        attr3 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr3, "NAME").text = "Status"
        if Mapsaname in ["ReworkCandidateNames"]:
            ET.SubElement(attr3, "VALUE").text = "Needs repair"
        else:
            ET.SubElement(attr3, "VALUE").text = "Good"

        #MPA chips
        child = ET.SubElement(MAPSA, "CHILDREN")
    
        for index, row in df.iterrows():
            child_sub = ET.SubElement(child, "PART", mode="auto")
            ET.SubElement(child_sub, "KIND_OF_PART").text = "MPA Chip"
            ET.SubElement(child_sub, "NAME_LABEL").text = str(getName(data, index))
            #Predefined attributes of child
            child_predef = ET.SubElement(child_sub, "PREDEFINED_ATTRIBUTES")
            child_predef_attr = ET.SubElement(child_predef, "ATTRIBUTE")
            ET.SubElement(child_predef_attr, "NAME").text = "Chip Posn on Sensor"
            ET.SubElement(child_predef_attr, "VALUE").text = str(getPosn(data, index))
                                                        
        sensor_sub = ET.SubElement(child, "PART", mode="auto")
        ET.SubElement(sensor_sub, "KIND_OF_PART").text = Mapsaname[4:13]+'_PSP_MAINL'
        ET.SubElement(sensor_sub, "NAME_LABEL").text = 'MaPSA name'
    
        ET.indent(ET.ElementTree(root),'   ')
        f = open('/uscms/home/wjaidee/nobackup/MaPSA_database/XMLgenerator/XMLnew/'+Mapsaname+'.xml', "wb")
        ET.ElementTree(root).write(f)
    
        xmlstr = ET.tostring(root)
        dom = xml.dom.minidom.parseString(xmlstr)
        xmlfinal = dom.toprettyxml(indent="   ")
        print(xmlfinal)

############################################################################
#for HPK first data set

def HPK_getdata(filename):
    chip_data = pd.read_csv('/uscms/home/wjaidee/nobackup/MaPSA_database/'+filename+'.csv')
    return chip_data

def HPK_MapsaName(filename):
    return 'HPK_'+filename[0:9]+filename[-1:]

def HPK_getPosn(num):
    if num>8:
        Posn=25-num
    else:
        Posn=num
    return Posn

def HPK_Kapval(name):
    noKap = ["HPK_35494_032L","HPK_35494_033L","HPK_35494_040L","HPK_35494_041L","HPK_35494_042L","HPK_35494_036L","HPK_35494_037L","HPK_35494_038L","HPK_35494_039L"]
    if name in noKap:
        value = "No"
    else:
        value = "Yes"
    return value

def HPK_getNameLabel1(chip_data, no):
    name = chip_data['WaferID'][no][:6] + '_'+  chip_data['WaferID'][no][6:8]
    row = abs(int(chip_data['Waferrow'][no]))
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
    raw = pd.read_csv('/uscms/home/wjaidee/nobackup/MaPSA_database/XMLgenerator/'+sheetname, names =['number', 'location','WaffelPackno','WaffelPackrow','WaffelPackcol', 'WaferID','Waferrow','Wafercol','BINcode'])
    data = pd.DataFrame(raw).tail(-1)
    filename_list = data.dropna()['number'].tolist()
    print(filename_list)
    k = len(filename_list)
    size = 16
    for n in range(k):
        df = data[size*n:size*(n+1)]
        df.to_csv('/uscms/home/wjaidee/nobackup/MaPSA_database/'+filename_list[n]+'.csv',index=False)

    print(filename_list)
    return filename_list


#for HPK sheet 
def HPK_getXML1(sheetname):
    filename_list = HPK_split1(sheetname) #split,save csv files
    for filename in filename_list:
        chip_data = HPK_getdata(filename)
        print(chip_data)
        root = ET.Element("ROOT")
        parts = ET.SubElement(root, "PARTS")

        # MaPSA block
        MAPSA = ET.SubElement(parts, "PART", mode="auto") #use ElementTree to add mode='auto'
        ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
        ET.SubElement(MAPSA, "NAME_LABEL").text = HPK_MapsaName(filename)
        ET.SubElement(MAPSA, "MANUFACTURER").text = Loc
        ET.SubElement(MAPSA, "LOCATION").text = Loc
        ET.SubElement(MAPSA, "VERSION").text = "2.0"

        # MaPSA attributes
        predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
        attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr1, "NAME").text = "Has Kapton isolation"
        ET.SubElement(attr1, "VALUE").text = HPK_Kapval(HPK_MapsaName(filename))
        
        attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr2, "NAME").text = "Grade"
        if HPK_MapsaName(filename) in GradeB:
            Grade = 'B'
        elif HPK_MapsaName(filename) in GradeC:
            Grade = 'C'
        else:
            Grade = 'A'
        ET.SubElement(attr2, "VALUE").text = Grade
        
        #Rework candidate
        attr3 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr3, "NAME").text = "Status"
        if filename in ["ReworkCandidateNames"]:
            ET.SubElement(attr3, "VALUE").text = "Needs repair"
        else:
            ET.SubElement(attr3, "VALUE").text = "Good"
        
        #Kapton block
        #attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        #ET.SubElement(attr2, "NAME").text = "Kapton"
        #ET.SubElement(attr2, "VALUE").text = str(HPK_Kapval(HPK_MapsaName(filename)))
        #print(str(Kapval(HPK_MapsaName(filename))))
        
        child = ET.SubElement(MAPSA, "CHILDREN")
    
        df = HPK_getdata(filename)
        for index, row in df.iterrows():
            child_sub = ET.SubElement(child, "PART", mode="auto")
            ET.SubElement(child_sub, "KIND_OF_PART").text = "MPA Chip"
            ET.SubElement(child_sub, "NAME_LABEL").text = str(HPK_getNameLabel1(chip_data, index))
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
        
        ET.indent(ET.ElementTree(root),'   ')
        f = open('/uscms/home/wjaidee/nobackup/MaPSA_database/XMLgenerator/XMLnew/'+HPK_MapsaName(filename)+'.xml', "wb")
        ET.ElementTree(root).write(f)
        print(HPK_MapsaName(filename))
    return 

########################################################################
#for HPK missing data
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
        df.to_csv('/uscms/home/wjaidee/nobackup/MaPSA_database/'+filename_list[i]+'.csv', index=False) #reset index values
    return filename_list

def HPK_getXML2(sheetname):
    filename_list = HPK_split(sheetname) #split,save csv files
    for filename in filename_list:
        chip_data = HPK_getdata(filename)
       
        root = ET.Element("ROOT")
        parts = ET.SubElement(root, "PARTS")

        # MaPSA block
        MAPSA = ET.SubElement(parts, "PART", mode="auto") #use ElementTree to add mode='auto'
        ET.SubElement(MAPSA, "KIND_OF_PART").text = "MaPSA"
        ET.SubElement(MAPSA, "NAME_LABEL").text = HPK_MapsaName(filename)
        ET.SubElement(MAPSA, "MANUFACTURER").text = Loc
        ET.SubElement(MAPSA, "LOCATION").text = Loc
        ET.SubElement(MAPSA, "VERSION").text = "2.0"
        
        # MaPSA attributes
        predefMapsa1 = ET.SubElement(MAPSA, "PREDEFINED_ATTRIBUTES")
        attr1 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr1, "NAME").text = "Has Kapton isolation"
        ET.SubElement(attr1, "VALUE").text = HPK_Kapval(HPK_MapsaName(filename))
        
        attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr2, "NAME").text = "Grade"
        if HPK_MapsaName(filename) in GradeB:
            Grade = 'B'
        elif HPK_MapsaName(filename) in GradeC:
            Grade = 'C'
        else:
            Grade = 'A'
        ET.SubElement(attr2, "VALUE").text = Grade

        
        #Rework candidate
        attr3 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        ET.SubElement(attr3, "NAME").text = "Status"
        if filename in ["ReworkCandidateNames"]:
            ET.SubElement(attr3, "VALUE").text = "Needs repair"
        else:
            ET.SubElement(attr3, "VALUE").text = "Good"
        
        
        #Kapton block
        #attr2 = ET.SubElement(predefMapsa1, "ATTRIBUTE")
        #ET.SubElement(attr2, "NAME").text = "Kapton"
        #ET.SubElement(attr2, "VALUE").text = str(HPK_Kapval(HPK_MapsaName(filename)))
        
        child = ET.SubElement(MAPSA, "CHILDREN")
    
        df = HPK_getdata(filename)
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
        f = open('/uscms/home/wjaidee/nobackup/MaPSA_database/XMLgenerator/XMLnew/'+HPK_MapsaName(filename)+'.xml', "wb")
        ET.ElementTree(root).write(f)
        print(HPK_MapsaName(filename))
    return 

################################################################
Loc = input('Enter LOCATION:')
Loc_dict = {'H':'HAMAMATSU','A':'AEMtec'}
Loc = Loc_dict[Loc]
print(Loc)

sheet_dict = {'A':'AEMnamelists.txt','B': 'MissingAEM.csv' ,'C':'HPKSheet1.csv', 'D':'hpk2.csv'}
print(sheet_dict)
sheetname = input('Which file:')
if sheetname in list(sheet_dict.keys()):
    sheetname = sheet_dict[sheetname]
else:
    sheetname = sheetname

if Loc == 'AEMtec':
    typeoffile = input('Is the input file in txt? [y/n]')
    if  typeoffile == 'y':
        filename_list = AEM_getfilename(sheetname)
        for filename in filename_list:
            AEMtoXML(filename)
    elif typeoffile == 'n':
        AEM_csvgetXML(sheetname)
    
elif Loc == 'HAMAMATSU':
    Chipnum = input('Is the chip name in rows, cols? [y/n]')
    if Chipnum == 'y':
        HPK_getXML1(sheetname)
    elif Chipnum == 'n':
        HPK_getXML2(sheetname)
