#MBXAS utility for finding dominant orbitals from a spectrum
#Subhayan Roychoudhury, LBNL, April 2020
#----------------------------------------------------------------------------------------------------
# USAGE INSTRUCTION :
#python MBXAS_pp_utility.py ElementIndex:Spin1_Kpoint1_Direction1,Spin2_Kpoint2_Direction2... ElementIndex:Spin1_Kpoint1_Direction1,Spin2_Kpoint2_Direction2... ...
#Different excited species must be separated by space
#Different (spin_kpoint_direction) combination for the same excited species must be separated by comma
#Note that indices for k-point and spin start from 0
#Orbital-index starts from 1 in the output
#----------------------------------------------------------------------------------------------------
# USAGE EXAMPLE :
#python MBXAS_pp_utility.py Li1:0_0_x,0_1_y,0_2_x,0_124_z,1_0_x,1_20_x,1_124_y Li69:0_0_x,0_124_y,1_0_x,1_124_z
#----------------------------------------------------------------------------------------------------
import sys
import csv
import glob
import re
import numpy as np
from scipy.signal import argrelextrema
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#####################
thrshld=0.3 #tolerance between orbital energy and peak energy
#####################
for narg in range(1,len(sys.argv)): #loop over each excited atom provided as command line argument.
 atom=str(sys.argv[narg]).split(':')[0]
 res1 = " ".join(re.split("[^a-zA-Z]*", atom)).strip()#atom symbol
 res2=" ".join(re.split("[^0-9]*", atom)).strip()#atom index
 #Find FINAL_SHIFT from shift.report
 shiftfile="shift.report"
 shift_line = open(shiftfile)
 for line in shift_line:
  if ((line.split()[1] == res1) and (line.split()[2] == res2)):
   FINAL_SHIFT = float(line.split()[-1])
   #print("FINAL_SHIFT is "+str(FINAL_SHIFT)) 
 #Analyze spectra for various input (spin+kpoint) combinations
 for isk in str(sys.argv[narg]).split(':')[1].split(','):
  band_ind = 0
  ispin=isk.split('_')[0]
  ik=isk.split('_')[1]
  axis=isk.split('_')[2]
  if (axis == 'x'):
   iaxis=2
  if (axis == 'y'):
   iaxis=3
  if (axis == 'z'):
   iaxis=4
  dirpath="XAS/*/"+res1+res2
  dirpath=glob.glob(dirpath)[0]
  #Read the spectrum
  isk_file=dirpath+"/spec_xas_ik0.dat"
  print(' ')
  #print("Reading from "+isk_file)
  #print('_________________________________________________________')
  f=open(isk_file,"r")
  lines=f.readlines()
  result=[]
  for x in lines:
    result.append(float(x.split(' ')[iaxis]))
  result=np.array(result)
  #Find the local maxima of the spectrum
  ofile = argrelextrema(result, np.greater)
  bfile=ofile[0]
  type(bfile)
  LocalEnMax = []
  orb = {}
  for i in bfile:
   LocalEnMax += [float(lines[int(i)].split()[0])-FINAL_SHIFT]
  #print("Shifted Local Energy Maxima Are "+str(LocalEnMax))
  print(' ')
  #Read *.mbxas.out
  outpath=dirpath+"/*.mbxas.out"
  for filename in glob.glob(outpath):
   #print("Reading from "+filename)
   print('_________________________________________________________')
   mbxas_out  =open(filename)
   iaxis = int(iaxis-2)
   iskTrue = False
   iaxisTrue = False
   canPrintLines = False
   lumoline=int(0)
   for line in mbxas_out:
     #Find LUMO from *.mbxas.out
     if "Energy of LUMO" in line:  
      lumoline = lumoline + 1
      if ( int(lumoline) == int(2) ):
       LUMO = float(line.split()[3])
       #print("FCH LUMO is "+str(LUMO))
     isk_begin = "Processing (ispin, ik) = ("+ispin+","+ik+")"
     iaxis_begin = "ixyz = "+str(iaxis).strip()
     if isk_begin in line:
      iskTrue = True
     if not iskTrue:
      continue #Find the right isk
     #############################
     if "Band energies (eV):" in line:
      band_ind = band_ind + 1
      line_next_to_band = 0
     if (band_ind == 2):
      line_next_to_band = line_next_to_band + 1
     if (band_ind == 2 and line_next_to_band == 2):
      local_lumo = float(line.split()[5])
     #############################
     if iaxis_begin in line:
      iaxisTrue = True
      print("######################################################")
      print("For spin = "+ispin+" ik = "+ik+" axis = "+axis)
     if not iaxisTrue:
      continue #Find the right axis
     if line.startswith("f^(1) major contributions"):
        canPrintLines = True #start printing from "f^(1) major contributions"
     if canPrintLines:
       if line.startswith("max_conf:"):#no need to go further once you've reached "max_conf:
        break
       #LUMO=0
       if "major contributions" not in line and "amplitude" not in line:
	    for i in range(len(LocalEnMax)):
            #print("i is "+str(i))
              if (abs(float(line.split()[1])-(float(LocalEnMax[i])-(local_lumo-LUMO))) < thrshld ):
                #print("local_lumo = " + str(local_lumo) + " and LUMO = " + str(LUMO))
                print("Local maximum index: "+str(i+1)+" -----> Energy: "+str(float(LocalEnMax[i])+float(FINAL_SHIFT))+" -----> orbital index "+str(int(line.split()[0].replace(':',''))+1))
                #print((LocalEnMax[i])+float(FINAL_SHIFT))
	        orb.update({int(line.split()[0].replace(':',''))+1:float(LocalEnMax[i])+float(FINAL_SHIFT)})
		#print(orb)

#Creating orbital and max energy arrays for use in plots

orbital = orb.keys()
print("The relevant orbitals are:")
print(orbital)
en_max = orb.values()
print("The corresponding energies are:")
print(en_max)

#Plotting all spectra

with open("spec_xas_all.dat") as xas_infile, open("spec_xas_all.csv", "w") as xas_outfile:
    csv_writer = csv.writer(xas_outfile)
    prev = ''
    csv_writer.writerow(['x_xas','y_xas'])
    for line in xas_infile.read().splitlines():
        csv_writer.writerow([line, prev])

with open("spec0_i_all.dat") as i_infile, open("spec0_i_all.csv", "w") as i_outfile:
    csv_writer = csv.writer(i_outfile)
    prev = ''
    csv_writer.writerow(['x_i','y_i'])
    for line in i_infile.read().splitlines():
        csv_writer.writerow([line, prev])
    
with open("spec0_f_all.dat") as f_infile, open("spec0_f_all.csv", "w") as f_outfile:
    csv_writer = csv.writer(f_outfile)
    prev = ''
    csv_writer.writerow(['x_f','y_f'])
    for line in f_infile.read().splitlines():
        csv_writer.writerow([line, prev])

#Plotting csv file

x_xas = []
y_xas = []

x_i = []
y_i = []

x_f = []
y_f = []

with open('spec_xas_all.csv','r') as xas_csvfile:
    xas_plots = csv.reader(xas_csvfile, delimiter=' ')
    next(xas_plots)
    for row in xas_plots:
        x_xas.append(float(row[0]))
        y_xas.append(float(row[1]))

with open('spec0_i_all.csv','r') as i_csvfile:
    i_plots = csv.reader(i_csvfile, delimiter=' ')
    next(i_plots)
    for row in i_plots:
        x_i.append(float(row[0]))
        y_i.append(float(row[1]))

with open('spec0_f_all.csv','r') as f_csvfile:
    f_plots = csv.reader(f_csvfile, delimiter=' ')
    next(f_plots)
    for row in f_plots:
        x_f.append(float(row[0]))
        y_f.append(float(row[1]))

#Find points at peaks

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


x_peaks = []
y_peaks =[]



for i in en_max:
    x_peaks.append(find_nearest(x_xas, i))
    x_peaks_pos = x_xas.index(i)
    y_peaks.append(y_xas[x_peaks_pos])
    
#print(x_peaks)
#print(y_peaks)


xas = plt.gcf()
#plt.axis(xmin=280, xmax=300)
plt.plot(x_xas,y_xas, label='spec_xas_all', linewidth='0.5')
plt.plot(x_i,y_i, label='spec0_i_all', linewidth='0.5')
plt.plot(x_f,y_f, label='spec0_f_all', linewidth='0.5')
plt.plot(x_peaks, y_peaks, 'o', markersize=3)

print(orb)
orb_annotate=[]

for i in range(len(orbital)):
        seen = set()
        uniq = []
        for x in x_peaks:
                if x not in seen:
                        uniq.append(x)
                        seen.add(x)

print(uniq)

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys

orb_annotate=[]
for i in en_max:
	print(i)
	L = (getKeysByValue(orb, i))
	y = " ".join(str(x) for x in L)
	orb_annotate.append(y)

print(orb_annotate)

for i in range(len(orbital)):
    plt.annotate(str(orb_annotate[i]), (x_peaks[i],y_peaks[i]))

plt.margins(0.01)
plt.legend()

#plt.show()
xas.savefig('xas.png')
