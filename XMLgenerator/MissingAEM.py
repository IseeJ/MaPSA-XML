file = 'MissingAEM.csv'
import pandas as pd
data = pd.read_csv(file)
#print(data)
data = pd.read_csv(file, names= ['No.', 'Module', 'Bondposition', 'MPA','Wafer ID', 'Row', 'Column', 'Bin'])

df = pd.DataFrame(data)
df = df.tail(-1)
print(df)

grouped = df.groupby('No.')

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
    
AEM_split(file)

group_dict = {}
for group_name, group_data in grouped:
    group_data = group_data.reset_index(drop=True)
    group_dict[f'Data{group_name}'] = group_data

Data1 = group_dict['Data1']
Data2 = group_dict['Data2']
Data3 = group_dict['Data3']
Data4 = group_dict['Data4']

import xml.etree.ElementTree as ET
import xml.dom.minidom

datalist = [Data1, Data2, Data3, Data4]
MapSub = {'1':'AEM_35494_002L','2': 'AEM_35494_030L', '3':'AEM_35494_029L', '4':'AEM_35494_028L'}

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

    
def AEM_csvgetXML(datalist):
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
    
AEM_csvgetXML(datalist)
