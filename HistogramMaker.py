import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import scipy.interpolate
from matplotlib import cm

THRESHOLD=40000.0
datafile=open('muon_data_II.csv','r')
data = np.array(list(csv.reader(datafile)))
new_data=data[1:,1:2] #only the lifetimes column
lifetimes=(np.squeeze(np.asarray(new_data)).astype(float)).ravel()
good_lifetimes=[]
for lifetime in lifetimes:
    if lifetime<THRESHOLD:
        good_lifetimes.append(lifetime)
good_lifetimes=np.array(good_lifetimes)
print(good_lifetimes.max())
histo,bin_edges=np.histogram(good_lifetimes,bins=45)
f=plt.figure(1)
plt.hist(good_lifetimes,bins=45)
f.show()
s=plt.figure(2)
plt.hist(good_lifetimes,bins=60)
s.show()
t=plt.figure(3)
plt.hist(good_lifetimes,bins=100)
t.show()
"""""
rows=zip(histo,bin_edges)
with open('HistoResults.csv', 'w', ) as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for row in rows:
        wr.writerow(row)
myfile.close()
"""