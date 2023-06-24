from dict2xml import dict2xml as d2x
data = {
    'PARTS' : {
        'PART mode="auto': {
            'KIND_OF_PART': 'MaPSA',
            'NAME_LABEL': 'AEM_35494_016L',
            'LOCATION': 'AEMtec',
            'VERSION': '2.0'
        }
    }
  }
print (d2x(data, wrap="all", indent="  "))
