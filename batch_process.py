import csv

def processSubject(path, cellCount):
    with open(path, 'r') as csvdatafile:
        subjectreader = csv.reader(csvdatafile, delimiter=',')
        next(subjectreader) # skip over header

        # sort data in each file by branches
        branchdec = sorted(subjectreader, key=lambda item: int(item[1]), reverse=True)
        
        # truncate all rows that occur after cellCount # of rows
        branchtrunc = branchdec[:cellCount]

        # calculate sums/avgs for each relevant column
        branchSum, junctionSum, endpointSum, avgbranchSum = 0,0,0,0
        # ,# Branches,# Junctions,# End-point voxels,# Junction voxels,# Slab voxels,Average Branch Length,# Triple points,# Quadruple points,Maximum Branch Length
        # for id, branches, junctions, endpoint, junk1, junk2, avgbranchLen, junk3, junk4, junk5 in branchtrunc:
        for branches, junctions, endpoint, junk1, junk2, avgbranchLen, junk3, junk4, junk5 in branchtrunc:
            branchSum += int(branches)
            junctionSum += int(junctions)
            endpointSum += int(endpoint)
            avgbranchSum += float(avgbranchLen)

        return { "length":len(branchtrunc),
                 "branchSum": branchSum,
                 "junctionSum": junctionSum,
                 "endpointSum": endpointSum,
                 "avgbranchSum": avgbranchSum,
                 "branchSumCell": branchSum/cellCount,
                 "junctionSumCell": junctionSum/cellCount,
                 "endpointSumCell": endpointSum/cellCount,
                 "avgbranchSumCell": avgbranchSum/cellCount }


# write totals out to output.csv
with open('output.csv', 'w') as writefile:
    fieldnames = ["filename", "cellCount", "branchSum", "junctionSum", "endpointSum", "avgbranchSum", "branchSumCell", "junctionSumCell", "endpointSumCell", "avgbranchSumCell"]
    writer = csv.DictWriter(writefile, fieldnames=fieldnames)
    writer.writeheader()
    with open('Hipp_cell_count.csv', 'r') as csvfile:
         cellcountreader = csv.reader(csvfile, delimiter=',', quotechar='|')

         # skip header
         next(cellcountreader)

         # for each row in 'Hipp_cell_count.csv'
         for row in cellcountreader:
            filename = row[0]
            cellCount = int(row[1])

            print("PROCESSING: filename: "+filename+", cellCount: "+ str(cellCount))
            subject = processSubject("data/"+filename+".csv", cellCount)

            writer.writerow({'filename': filename,
                     'cellCount': cellCount,
                     'branchSum': subject['branchSum'],
                     'junctionSum': subject['junctionSum'],
                     'endpointSum': subject['endpointSum'],
                     'avgbranchSum': subject['avgbranchSum'],
                     'branchSumCell': subject['branchSumCell'],
                     'junctionSumCell': subject['junctionSumCell'],
                     'endpointSumCell': subject['endpointSumCell'],
                     'avgbranchSumCell': subject['avgbranchSumCell']})
