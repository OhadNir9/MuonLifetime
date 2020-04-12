import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import scipy.interpolate
from matplotlib import cm
from scipy.optimize import curve_fit

#Constructing the lifetimes vector
THRESHOLD=40000.0

def raw_lifetimes_extractor():
    datafile=open('muon_data_II.csv','r')
    data = np.array(list(csv.reader(datafile)))
    new_data=data[1:,1:2] #only the lifetimes column
    raw_lifetimes=(np.squeeze(np.asarray(new_data)).astype(float)).ravel()
    datafile.close()
    return raw_lifetimes

#Filtering the >40000 lifetimes (successing arrivales)
def lifetime_filter(raw_lifetimes):
    good_lifetimes=[]
    for lifetime in raw_lifetimes:
        if lifetime<THRESHOLD:
            good_lifetimes.append(lifetime)
    good_lifetimes=np.array(good_lifetimes)
    return good_lifetimes

#generate histogram data and plot (N_BINS bins, one can change the number of bins or
#enter array of bins values)
#also centering the bins in the histogram data with fixed_bin_edges

def histogram_builder(n_bins,lifetimes):
    histo_values, bin_edges=np.histogram(lifetimes, bins=n_bins)
    fixed_bin_edges=[]
    for i in range(len(bin_edges)-1):
        fixed_bin_edges.append((bin_edges[i]+bin_edges[i+1])/2.0)
    plt.subplot(2,2,1)
    plt.gca().set_title('Built in histogram - '+str(n_bins)+' bins')
    plt.hist(lifetimes,bins=n_bins)
    return histo_values,fixed_bin_edges


#Extra code for outputting the histogram results to csv file.
def histogram_export(histo_values,fixed_bin_edges):
    rows=zip(histo_values,fixed_bin_edges)
    with open('hist_res_'+str(len(fixed_bin_edges))+'_bins.csv', 'w', ) as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for row in rows:
            wr.writerow(row)
    myfile.close()



#Define the function structure to fit to (exponential decay with constant)
def func(x,a,b,c):
    return a*np.exp(-b*x)+c

def Fitter(histo_values, fixed_bin_edges, first_bin=False, add_log_scale=False, no_const_fit=False,microsec=False):
    #Fit with some initial guess
    p0=(150, 0.0005, 4)
    if microsec:
        fixed_bin_edges=[x/1000 for x in fixed_bin_edges]
        p0=(150,0.5,4)

    if first_bin:
        popt, pcov = curve_fit(func, fixed_bin_edges, histo_values, p0=p0)
    elif no_const_fit:
        popt, pcov = curve_fit(func, fixed_bin_edges[1:round(0.5*len(fixed_bin_edges))], histo_values[1:round(0.5*len(histo_values))], p0=p0)
    else:
        popt, pcov = curve_fit(func, fixed_bin_edges[1:], histo_values[1:], p0=p0)
    if not microsec:
        xx=np.linspace(0,25000,500)
    else:
        xx=np.linspace(0,25,1)
    yy=func(xx, *popt)
    plt.subplot(2,2,2)
    ax2=plt.gca()
    ax2.set_title('Curve fitting - '+str(len(fixed_bin_edges))+' fixed bins')
    ax2.set_ylabel('frequency')
    if not microsec:
        ax2.set_xlabel('lifetime [ns]')
    else:
        ax2.set_xlabel('lifetime [us]')
    # plot the data iteslf
    if first_bin:
        plt.plot(fixed_bin_edges, histo_values, 'ko')
    else:
        plt.plot(fixed_bin_edges[1:], histo_values[1:], 'ko')
    plt.plot(xx, yy) #plot the fitted function
    print("popt is: "+str(popt)) #the fit values (a,b,c)"""
    if microsec:
        print("lifetime is: "+str(1/popt[1])+" microsecs")
    else:
        print("lifetime is: " + str(1 / (1000*popt[1])) + " microsecs")
    if add_log_scale:
        plt.subplot(2, 2, 3)
        ax4 = plt.gca()
        ax4.set_title('Log scaled')
        ax4.set_ylabel('frequency')
        ax4.set_xlabel('lifetime [ns]')
        if first_bin:
            plt.plot(fixed_bin_edges, histo_values, 'ko')
        else:
            plt.plot(fixed_bin_edges[1:], histo_values[1:], 'ko')
        plt.plot(xx, yy)
        plt.yscale('log')

lifetimes=lifetime_filter(raw_lifetimes_extractor())
histo_values,fixed_bin_edges=histogram_builder(25,lifetimes)
Fitter(histo_values, fixed_bin_edges, add_log_scale=True)

plt.show()