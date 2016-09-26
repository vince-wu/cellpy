# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 10:43:35 2015

FetchArbinData
@author: jepe
"""
import sys,os,csv,itertools
from cellpy import arbinreader

FileName  = r"C:\Scripting\MyFiles\dev_arbindata\abdel\20141030_LBCM5_6_cc_01.res"
Mass      = 0.982
OutFolder = r"C:\Scripting\MyFiles\dev_arbindata\abdel\processed"

try:
    os.chdir(OutFolder)
    print "Output will be sent to folder:"
    print OutFolder
except:
    print "OutFolder does not exits"
    sys.exit(-1)

# Loading arbin-data
d = arbinreader.arbindata(FileName)
d.loadres()
d.set_mass(Mass)
d.make_summary()
d.create_step_table()
print "\nexporting raw-data and summary"
d.exportcsv(OutFolder)

# Extracting cycles
list_of_cycles = d.get_cycle_numbers()
number_of_cycles = len(list_of_cycles)
print "you have %i cycles" % (number_of_cycles)

FileName0 = os.path.basename(FileName)
outfile = "%s_cycles.csv" % (FileName0)
out_data = []

for cycle in list_of_cycles:
    try:
        c,v = d.get_cap(cycle)
        c = c.tolist()
        v = v.tolist()
        header_x = "cap cycle_no %i" % cycle
        header_y = "voltage cycle_no %i" % cycle
        c.insert(0,header_x)
        v.insert(0,header_y)
        out_data.append(c)
        out_data.append(v)  
    except:
        print "could not extract cycle %i" % (cycle)
        

# Saving cycles in one .csv file (x,y,x,y,x,y...)
delimiter = ";"
print "saving the file with delimiter '%s' " % (delimiter)
with open(outfile, "wb") as f:
    writer=csv.writer(f,delimiter=delimiter)
    writer.writerows(itertools.izip_longest(*out_data))
    # star (or asterix) means transpose (writing cols instead of rows)

print "saved the file",
print outfile
print "bye!"
