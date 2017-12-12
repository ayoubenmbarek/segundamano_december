lines_seen = set() # holds lines already seen
outfile = open('/home/databiz41/segundamano/segundamano/segundamanowithout2.csv', "w")
for line in open('/home/databiz41/segundamano/segundamano/segundamanowithout.csv', "r"):
    if line not in lines_seen: # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
