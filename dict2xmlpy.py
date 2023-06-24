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
