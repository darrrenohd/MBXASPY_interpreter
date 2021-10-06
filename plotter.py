import csv
import pandas as pd
import matplotlib.pyplot as plt

#Converting each .dat file date to csv

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

#Plotting each .csv file and saving as 'xas.png'

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

xas = plt.gcf()
plt.axis(xmin=280, xmax=300)
plt.plot(x_xas,y_xas, label='spec_xas_all', linewidth='0.5')
plt.plot(x_i,y_i, label='spec0_i_all', linewidth='0.5')
plt.plot(x_f,y_f, label='spec0_f_all', linewidth='0.5')
plt.margins(0.01)
plt.legend()

plt.show()
xas.savefig('xas.png')
