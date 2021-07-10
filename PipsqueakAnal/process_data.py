import os

basePath = os.getcwd()
pipsqueakAnalPath = basePath + "/PipSqueakAnal"
pipsqueakDataPath = pipsqueakAnalPath + "/Pipsqueak_data"
print(pipsqueakDataPath)

# os.path.isfile('')
isPath = os.path.isdir(pipsqueakDataPath)
print(isPath)
