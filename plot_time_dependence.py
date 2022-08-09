# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 17:36:30 2022

@author: redin
"""

from scipy import *
from numpy import *
import numpy as np
import matplotlib
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import os
matplotlib.pyplot.close("all")
mpl.rcParams['figure.dpi'] = 300

def Read_In_komma(Datei):
    Daten=[]
    for line in open(Datei).readlines():
        Daten.append(line.split(','))
    return(Daten)

def save_data(results,name,folder): 
    f_Daten= open(folder+'daten//'+ name +'.txt', "w")
    for i in range(0,len(results)):
        f_Daten.write(str(results[i])+"\n")
    f_Daten.close()
    print('Output file saved')
    return() 






# Open the folder where the images are
current_folder=(r"\\atlas\FSTC_SPM\Ajay\MASI_33i44\light")
files = os.listdir(current_folder)

filename=[]
for i in range(0,len(files)):
    temp=''
    for j in range(19,len(files[i])-4):
        temp=temp+files[i][j]
    #print (temp)
    filename.append(temp)
filename=array(filename)

sort_index = np.argsort(filename)



count=[]    
open_files=True
if open_files==True:
    images=[]
    image_crop=[]
    for i in range(1,len(files)):
        if i%1==0:
            #print (i)
            for k in range(0,len(sort_index)):
                if i==0:
                    i=str(0)
                if filename[k]==str(i):
                    found=k
        
            temp=plt.imread(current_folder+"//"+files[found])
            count.append((i*120)/3600) # time between 2 images
            if i <159:                 # Until when do you keep the same interation time
                temp=temp-(4240/2**16)      # enter correct background; bg is devided by 2E16 in order to convert counts to an value between 0 and 1  
            if i >=159 and i<1738:           # idem for all the rest
                temp=(temp-(4260/2**16))/4.13
            if i >=1738 and i<1745:
                    temp=(temp-(4290/2**16))/4.3
            if i >=1745:
                    temp=(temp-(4390/2**16))/4.3
            images.append(temp)
            







      #Average the images
    for i in range(0,len(images)):
        image_crop.append(images[i][180:380, 50:250])
        #image_crop.append(images[i][0:600, 0:600])
    averageing=[]
    
    for i in range(0,len(images)):
        #averageing.append(np.average(image_crop[i]))   # This is in counts / 50ms
        #averageing.append(np.average(image_crop[i])*20) # This is in counts/ seconds
        #averageing.append(np.average(image_crop[i])*20*3.3E9) # This is in photons/cm2 s
        # At 532nm Laserpower: 66mW/cm2  
        # This gives: 660/((636262E-34*3E8)/(532E-9))=1.766E21 photons/m2 s
        averageing.append((np.average(image_crop[i])*20*3.3E9)/1.766E17)
        
        
        
    averageing=(array(averageing))*2**16
  
    
fig = plt.figure()
ax0=fig.add_subplot(1,1,1)

# Saving

#for i in range(0,len(image_crop)):
#    print (i)
#    plt.imsave("MASI_33i49_"+str(i)+".png",image_crop[i],cmap='afmhot')
    
plt.colorbar(ax0.imshow(image_crop[1000],cmap='afmhot',vmin=0))#,format=ticker.FuncFormatter(fmt))#,vmin=5,vmax=100))
ax0.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
ax0.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)

fig2, (ax1) = plt.subplots(1, 1, sharex=True, figsize=(3, 3))
fig2.subplots_adjust(hspace=0.05)  
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
#For ax1
for tick in ax1.xaxis.get_major_ticks():
    tick.label1.set_fontsize(7)
for tick in ax1.yaxis.get_major_ticks():
    tick.label1.set_fontsize(7) 
ax1.tick_params(direction='in', length=3, width=1, colors='black',
               grid_color='black', grid_alpha=0.5)
ax1.yaxis.get_offset_text().set_fontsize(7)#

ax1.set_xlabel("time [h]",fontsize=10)
ax1.set_ylabel("PLQY",fontsize=10)


ax1.plot(count,averageing)
#ax1.semilogy()

result=[]

result.append("time dependence of the PLQY"+"\t")
result.append("time [h]"+'\t'+ "PLQY()")
for i in range(0,len(count)):
    result.append((str(count[i])+'\t'+str(averageing[i])))
#save_data(result,"time_dependence_MASI_33i49",r"\\atlas\users\alex.redinger\Attract\paper last author\Sn-no 4+\result time dependence\\")



    
plt.subplots_adjust(top=0.947,
bottom=0.238,
left=0.243,
right=0.95,
hspace=0.05,
wspace=0.2)

plt.show()