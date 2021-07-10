import os
import sys

basePath = os.getcwd()
pipsqueakAnalPath = basePath + "/PipSqueakAnal/"
pipsqueakDataPath = pipsqueakAnalPath + "data/"

# Get subjects from their directory names
subjects = []
if os.path.isdir(pipsqueakDataPath):
    print(pipsqueakDataPath)
    subjects = os.listdir(pipsqueakDataPath)
    subjects.remove('.DS_Store')  # fucking macs
    print(subjects)
else:
    print("Data path not found. Got: " + pipsqueakDataPath)
    sys.exit(1)

# Setup possible values
brainRegions = ['LeftIL', 'LeftPL', 'RightIL', 'RightPL']
brainSections = ['1', '2', '3', '4']
numericStainTypes = ['1', '2', '3']
stainTypes = {
    "Parvalbumin": "1",
    "c-Fos": "2",
    "WFA": "3"
}

# file structure that must be validated within "data/" folder
# subject#/ (ex: 70.02)
# -deep/
#   -(subject#)_(brain_region [LeftIL, LeftPL, RightIL, RightPL])_(brain_section [1-4])_(stain_type [1-3])/
#       -(subject#)_(brain_region)_(brain_section)_(stain_type)_limitedArea_{single}_(brain_stain_name [{WFA},{Parvalbumin},{c-Fos}])_measurements.csv
#   -double-label_results/
#       -(subject#)_(brain_region [LeftIL, LeftPL, RightIL, RightPL])_(brain_section [1-4])_(stain_type [1-3])_limitedArea_{double}_(colocalized_stains [{parvalbumin_coloc_with_c-Fos}, {parvalbumin_coloc_with_WFA}, {c-Fos_coloc_with_parvalbumin}, {c-Fos_coloc_with_WFA}, {WFA_coloc_with_c-Fos}, {WFA_coloc_with_parvalbumin}])_measurements.csv
#   -triple-label_results/
#       -(subject#)_(brain_region [LeftIL, LeftPL, RightIL, RightPL])_(brain_section [1-4])_(stain_type [1-3])_limitedArea_{triple}_(triple_label_stains [{Parvalbumin}, {c-Fos}, {WFA}])
# -sup/
#   -(subject#)_(brain_region [LeftIL, LeftPL, RightIL, RightPL])_(brain_section [1-4])_(stain_type [1-3])/
#       -(subject#)_(brain_region)_(brain_section)_(stain_type)_limitedArea_{single}_(brain_stain_name [{WFA},{Parvalbumin},{c-Fos}])_measurements.csv
#   -double-label_results/
#       -(subject#)_(brain_region [LeftIL, LeftPL, RightIL, RightPL])_(brain_section [1-4])_(stain_type [1-3])_limitedArea_{double}_(colocalized_stains [{parvalbumin_coloc_with_c-Fos}, {parvalbumin_coloc_with_WFA}, {c-Fos_coloc_with_parvalbumin}, {c-Fos_coloc_with_WFA}, {WFA_coloc_with_c-Fos}, {WFA_coloc_with_parvalbumin}])_measurements.csv
#   -triple-label_results/
#       -(subject#)_(brain_region [LeftIL, LeftPL, RightIL, RightPL])_(brain_section [1-4])_(stain_type [1-3])_limitedArea_{triple}_(triple_label_stains [{Parvalbumin}, {c-Fos}, {WFA}])

# VALIDATION
for subject in subjects:
    # for either "deep" or "sup" layers
    for layer in ['deep', 'sup']:
        for brainRegion in brainRegions:
            for brainSection in brainSections:
                for key in stainTypes:
                    singleLabelDirPath = subject + "/" + layer + "/"
                    singleLabelDirName = subject + "_" + brainRegion + \
                        "_" + brainSection + "_" + stainTypes[key]
                    singleLabelFileName = singleLabelDirName + \
                        "_limitedArea_{single}_" + \
                        "{" + key + "}_measurements.csv"
                    singleLabelFullPath = pipsqueakDataPath + singleLabelDirPath + singleLabelDirName + "/"
                    if not(os.path.isdir(singleLabelFullPath)):
                        print("ERROR Missing Directory: " + singleLabelFullPath)
                    if not(os.path.isfile(singleLabelFullPath + singleLabelFileName)):
                        print("ERROR Missing File: " + singleLabelFullPath + singleLabelFileName)

            # os.path.isfile(path)
            # os.listdir(path)
