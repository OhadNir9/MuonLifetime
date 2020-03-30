import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt
import time
R=5000
NUMBER_OF_POINTS=1000000
def ThetaGenerator():
    #This function generates theta from the distribution of 2/pi * cos^2(x) in the range (-pi/2,pi/2)
    #Using Acceptence - Rejection method.
    while(True):
        y=np.random.uniform(-(math.pi)/2,(math.pi)/2)
        u=np.random.uniform(0,2/(math.pi))
        if (u<=(2/math.pi)*math.pow(math.cos(y),2)):
            return (math.pi)/2-y
            #y is the angle relative to the normal to earth (0 when perpendicular to earth)
            #We want the angle relative to the horizon, so we return theta = pi/2 - y
def RadiusGenerator(R):
    while(True):
        y=np.random.uniform(0,R)
        u=np.random.uniform(0,2/R)
        if(u<=2*y/(math.pow(R,2))):
            return y



def IsItInside(r,theta):
    if(r<7.5):
        return True #That's a muon just above the scintillator
    else:
        if(theta>(math.pi)/2):
            return False #That's a muon goes to the right
        else:
            d=r-7.5
            theta_c=np.arctan(12.5/d)
            if(theta<theta_c):
                return True #Goes in from the side
            else:
                return False #goes to the ground

#Our main program


start=time.time()
for RAD in range(500,3000,100): #Trying for multiple radiuses in the range 500 - 3000 cm
    NUMBER_OF_POINTS=10000*RAD
    in_counter = 0
    for i in range(NUMBER_OF_POINTS):
        theta = ThetaGenerator()
        r = RadiusGenerator(R)
        if (IsItInside(r, theta)):
            in_counter += 1
    effective_surface = (math.pi) * math.pow(R, 2) * (in_counter) / (NUMBER_OF_POINTS)
    print("R=" + str(RAD) + " | N=" + str(NUMBER_OF_POINTS))
    print("Got inside: " + str(in_counter))
    print("effective surface is [" + str(effective_surface) + "]")
end=time.time()
print ("execution time: "+str(end-start)+" seconds")
"""
arr=[]
arr2=[]
for i in range(NUMBER_OF_POINTS):
    arr.append(ThetaGenerator())
    arr2.append(RadiusGenerator(R))
theta_arr=np.array(arr)
r_arr=np.array(arr2)

sns.distplot(theta_arr)
plt.show()
plt.title("Theta distribution (relative to horizonal)")

sns.distplot(r_arr)
plt.title("Radius distribution")
plt.show()
"""