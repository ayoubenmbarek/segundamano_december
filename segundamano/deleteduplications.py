from more_itertools import unique_everseen
with open('/home/databiz41/segundamano/segundamano/segundamanowithout.csv','r') as f, open('/home/databiz41/segundamano/segundamano/segundamanowithout3.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
