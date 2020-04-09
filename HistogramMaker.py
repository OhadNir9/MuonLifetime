import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import scipy.interpolate
from matplotlib import cm
from scipy.optimize import curve_fit

#Constructing the lifetimes vector
THRESHOLD=40000.0
datafile=open('muon_data_II.csv','r')
data = np.array(list(csv.reader(datafile)))
new_data=data[1:,1:2] #only the lifetimes column
lifetimes=(np.squeeze(np.asarray(new_data)).astype(float)).ravel()
datafile.close()

#Filtering the >40000 lifetimes (successing arrivales)
good_lifetimes=[]
for lifetime in lifetimes:
    if lifetime<THRESHOLD:
        good_lifetimes.append(lifetime)
good_lifetimes=np.array(good_lifetimes)

#generate histogram data and plot (45 bins, one can change the number of bins or
#enter array of bins values)
#also centering the bins in the histogram data with fixed_bin_edges

histo_values, bin_edges=np.histogram(good_lifetimes, bins=45)
fixed_bin_edges=[]
for i in range(len(bin_edges)-1):
    fixed_bin_edges.append((bin_edges[i]+bin_edges[i+1])/2.0)
plt.subplot(2,2,1)
plt.gca().set_title('Built in histogram - 45 bins')
plt.hist(good_lifetimes,bins=45)


#Extra code for outputting the histogram results to csv file.
""""
rows=zip(histo_values,fixed_bin_edges)
with open('HistoResults.csv', 'w', ) as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for row in rows:
        wr.writerow(row)
myfile.close()
"""

#Define the function structure to fit to (exponential decay with constant)
def func(x,a,b,c):
    return a*np.exp(-b*x)+c

#Fit with some initial guess
popt, pcov = curve_fit(func, fixed_bin_edges, histo_values, p0=(100, 0.0005, 5))
xx=np.linspace(0,25000,500)
yy=func(xx, *popt)
plt.subplot(2,2,2)
ax2=plt.gca()
ax2.set_title('Curve fitting - 45 fixed bins')
ax2.set_ylabel('frequency')
ax2.set_xlabel('lifetime [ns]')
plt.plot(fixed_bin_edges, histo_values, 'ko') #plot the data iteslf
plt.plot(xx, yy) #plot the fitted function
print("popt is: "+str(popt)) #the fit values (a,b,c)

#Trying to fit without the first bin (too short lifetime seems to be unreliable)
print("Now trying without the first bin")
popt1,pcov1=curve_fit(func,fixed_bin_edges[1:], histo_values[1:], p0=(100, 0.0005, 5))
yy1=func(xx,*popt1)
plt.subplot(2,2,3)
ax3=plt.gca()
ax3.set_title('Curve fitting without first bin')
ax3.set_ylabel('frequency')
ax3.set_xlabel('lifetime [ns]')
plt.plot(fixed_bin_edges[1:], histo_values[1:], 'ko')
plt.plot(xx, yy1)
print("New popt is: "+str(popt1))

#Same plot as before(without first bin), now y axis is logscaled.
plt.subplot(2,2,4)
ax4=plt.gca()
ax4.set_title('Log scaled')
ax4.set_ylabel('frequency')
ax4.set_xlabel('lifetime [ns]')
plt.plot(fixed_bin_edges[1:], histo_values[1:], 'ko')
plt.plot(xx, yy1)
plt.yscale('log')
plt.show()

plt.savefig('Lifetime data.png', dpi=300)