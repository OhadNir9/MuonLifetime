import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import scipy.interpolate
from matplotlib import cm
datafile=open('muon_calibration_II.csv','r')
data = np.array(list(csv.reader(datafile)))
new_data=data[1:,1:] #without the titles line and the index column
th,hv,n_5=new_data[:,:1],new_data[:,1:2],new_data[:,-1] #x contains TH,HV , y contains N[5min]
x = (np.squeeze(np.asarray(th)).astype(float))
y = (np.squeeze(np.asarray(hv)).astype(float))
z = (np.squeeze(np.asarray(n_5)).astype(float))
plt.scatter(x,y,z)
plt.gray()
plt.show()

