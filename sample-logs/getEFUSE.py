def getEFUSE(logfilename):
    with open(logfilename) as file:
        lograw = file.read()
        EFUSE = lograw.split('\n')[2][1:19]
    return EFUSE
