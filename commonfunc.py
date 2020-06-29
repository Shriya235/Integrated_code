import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import re
from itertools import chain
from collections import Counter
from  datetime import datetime
import matplotlib
import statistics
import itertools
import matplotlib as mpl
import copy
#import datetime
import config1 as conf
import math
import time


#................CPU and Memory utilization graphs from log file.......................

def mem(sub,logfile):
    mem = []
    newlistmem = []
    memtime=[]
    tim=[]
    substr = sub                                              
    with open (logfile, 'rt') as myfile:
        for line in myfile:
            if line.find(substr) != -1:          
                mem.extend(re.split(r'[|\s]\s*', line))                                      
    for (value,total) in zip(mem[2::10],mem[1::10]):
        new_elem = int(value)/int(total)                                
        newlistmem.append(new_elem*100)
    for d,t in zip(mem[7::10],mem[8::10]):
       tim.append(d+" "+t)
    date_obj = []
    for temp in tim:
        date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
    dates = md.date2num(date_obj)
    Data_Printing(newlistmem,substr)
    Data_Plotting(dates,newlistmem,"Memory Utilisation","Memory","Memory_Utilisation.png")
    
def cpu(str1,logfile):
    cpu=[]
    newlistcpu=[]
    cputime=[]
    word=[]
    substr1=str1
    valu=substr1.split()
    with open (logfile, 'rt') as myfile:
        for line in myfile:
            if line.find(valu[0])!= -1 and line.find(valu[1])!= -1:
                cpu.append(line)
    for x in cpu:
        word.append(re.split(r'[|\s]\s*', x))
    for y in word:
        if y[0] == valu[0] and y[1]==valu[1]:
            l=len(y)
            newlistcpu.append(100-float(y[l-4]))
            cputime.append(y[l-3]+" "+y[l-2])    
    date_obj = []
    for temp in cputime:
        date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
    dates = md.date2num(date_obj)
    Data_Printing(newlistcpu,str1)
    Data_Plotting(dates,newlistcpu,"CPU Utilisation for Avg "+valu[1],"CPU Values","CPU_Utilisation"+valu[1]+".png")

  
def Data_Printing(value,string1):
    if string1 == "Mem:      ":
       print("Maximum memory utilisation: ",max(value),"%")
       print("Minimum memory utilisation: ",min(value),"%")
       print("Average memory utilisation : ",statistics.mean(value),"%")  
    else:
       val=string1.split()
       print("Maximum CPU utilisation for Average "+val[1]+": ",max(value),"%")
       print("Minimum CPU utilisation for Average "+val[1]+": ",min(value),"%")
       print("Average CPU utilisation for Average "+val[1]+": ",statistics.mean(value),"%")

def Data_Plotting(x,y,title,yaxis,sa):
    ax=plt.gca()
    #fig = plt.figure()
    plt.subplots_adjust(bottom=0.3)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks( rotation=30, horizontalalignment='right' )
    if "Memory" == yaxis or "CPU Values" == yaxis:
        plt.ylim(ymax = 100, ymin = 0)
    plt.plot(x,y)
    plt.title(title)
    plt.xlabel('Duration')
    plt.ylabel(yaxis)
    plt.savefig(sa,bbox_inches='tight')
    plt.clf() 
    #plt.show()                                                             
    

    
def Data_preparation(fname,avg,memory):
    mem(memory,fname)    
    for i in avg:
        cpu(i,fname)


#............(a) Number of clients connected to each VAP over time
#            (b) Plot the number of clients connected to VAP over time
#            (c) List the unique clients connected to each VAP and percentage duration...........................................    

def dataspecific(catch_start, catch_end,logfile,inter):
    results = []
    mac =[]
    m=[]
    uniq=[]
    c=[]
    per=[]
    t=0
    time1=[]
    clients_no=[]
    tim=[]
    p=re.compile(r'(?:[0-9a-fA-F]:?){12}')
    with open(logfile, 'r') as f1:
        lines = f1.readlines()
    i = 0
    while i < len(lines):
        if catch_start in lines[i]:
            t+=1
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    for a in results:
        for b in a:
            if re.findall(p,b):
               m.append(b)
    for x in m:
        mac.append(re.split(r'[|\s]\s*', x))
    singlelist = list(chain.from_iterable(mac))
    for ti in mac:
        tim.append(ti[26]+" "+ti[27])
    date_obj = []
    for temp in tim:
        date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
    dates = md.date2num(date_obj)
    length=len(singlelist[0::29])
    if length == 0:
        print("wlanconfig "+inter+" list sta is not found")
    else:
        s = Counter(singlelist[0::29])
        for uniquemac in s:
            uniq.append(uniquemac)
            c.append(s[uniquemac])
        for x in c:
            percent= (x/t)*100
            per.append(percent)
        no_of_clients = Counter(dates)
        for client in no_of_clients:
            time1.append(client)
            clients_no.append(no_of_clients[client])
        print("Number of clients connected to "+inter+" is: ",length)
        print("The unique clients connected to "+inter+" is: ")
        print (" \n" .join(str(x) for x in uniq))
        print("The Percentage duration of unique clients connected to "+inter+" is: ")
        print (" \n" .join(str(x) for x in per))
        Data_Plotting(dates,singlelist[0::29],"wlanconfig "+inter+" list sta","Mac Address","WLAN_"+inter+".png")
        Data_Plotting(time1,clients_no,"No. of clients connected to "+inter+" over time","No. of clients","WLAN_"+inter+" no.of clients .png")

def Call_dataspecific(interface_list,fname):
  for interface in interface_list:
     dataspecific(":/# wlanconfig "+interface+" list sta",  ":/# ",fname,interface)


#..............For each client, calculate: 
#               1. Whether it has disconnected and 
#               2. Total number of such disconnections..................................................

def uptime_check(lis,mac,len_ath,interf):
    time_list=lis
    new_list=[]
    c=0
    disconnect=0
    for x in time_list:                                                  #converting all times to minutes
        [h, m, s] = x.split(':')
        result=int(h)*60+int(m)+(int(s)/60)
        new_list.append(result)
    for a in range(len(new_list)-1):                                     #checking for adjacent times(min)
        if new_list[a]<new_list[a+1]:
            c=+1
        else:
            disconnect+=1
    print("Client= "+mac+" of interface "+interf)
    if len_ath != len(time_list):
       print('Disconnection observed due to no connection to the interface')
    else:
       print('No disconnections observed as the interface is connected')
    if disconnect!=0:
       print('No. of disconnections as uptime decreased =',disconnect)
    print('\n')   
   
def ath_mac_uptimelist(catch_start, catch_end,logfile,inter):
    results = []
    mac =[]
    m=[]
    ups=[]
    lists=[]
    upti=[]
    t=0
    every=[]
    p=re.compile(r'(?:[0-9a-fA-F]:?){12}')
    with open(logfile, 'r') as f1:
        lines = f1.readlines()
    i = 0
    while i < len(lines):
        if catch_start in lines[i]:
            t+=1
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    for a in results:
        for b in a:
            if re.findall(p,b):
               m.append(b)
    for x in m:
        mac.append(re.split(r'[|\s]\s*', x))
    singlelist = list(chain.from_iterable(mac))
    length=len(singlelist)
    if length ==0:
        print("wlanconfig "+inter+" list sta is not found")
    else:
        mac_address=list(set(singlelist[0::29]))               #unique clients attached is found
        for p in range(len(mac_address)):                      #as the unique clients attached will vary for each interface, creating only unique no. of empty lists
            lists.append([])
            upti.append([])
        count=0
        for single_mac in mac_address:                         #taking each client
            count+=1
            for c in mac:                                      #checking for the selected client in each line having all mac address line
              if single_mac in c:             
                lists[count-1].append(c)                       #appending all the lines of 1 client in each emptylist
        for p in range(len(mac_address)):
           for abc in lists[p]:
              upti[p].append(abc[19::29])                      #accessing only uptimes of 1 client in each emptylist
        for p in range(len(mac_address)):
            uptime_check(list(chain.from_iterable(upti[p])),mac_address[p],t,inter)             #calling function to check for uptime
    
def Call_uptimelist(interface_list,fname):
  for interface in interface_list:
     ath_mac_uptimelist(":/# wlanconfig "+interface+" list sta",":/# ",fname,interface)

#.................Channel Utilisation Eg: 3,48 etc................................................

def graphs(no_list,title,sa):
    y=[]
    for x in range(len(no_list)):
        y.append(x)
    plt.plot(y,no_list,'.', color='blue')
    plt.title(title)
    plt.xlabel('No.s')
    plt.ylabel('Measured vakues')
    plt.savefig(sa,bbox_inches='tight')
    plt.clf() 
    #plt.show()                                                             
    
    
def channel_utilisation(catch_start, catch_middle, catch_end,fname):
    results =[]
    channel_lines =[]
    word_chnline =[]
    lists=[]
    lists1=[]
    measure=[]
    with open(fname, 'r') as f1:
        lines = f1.readlines()
    i = 0
    while i < len(lines):
        if catch_start in lines[i]:
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j]  and catch_middle not in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    for a in results:                                                                   #for loop for extracting lines having the word channel
        for b in a:
            if "Channel " in b:
               word_chnline.extend(b.split())
               channel_lines.append(b)
    channel_nos =list(set(word_chnline[1::10]))                                         #to extract unique channel no.s Eg=3,48
    for x in range(len(channel_nos)):                                                   #to to create unique no. of empty lists
        lists.append([])
        lists1.append([])
        measure.append([])
    count=0
    for a in channel_nos :                                                              #to seperate each channel data into each empty list
        count+=1
        for b in channel_lines:
            if "Channel "+a in b:                                                       #"channel 3" or "channel 48" line is checked as these no.s may be 'Measured' values too
                lists[count-1].append(b)
    c=0
    for x in lists:                                                                     #channel lines list are split into words list                                                                    
       c+=1
       for s in x:
           lists1[c-1].extend(s.split())              
    for abc in range(len(channel_nos)):                                                  #function call for plotting graph, sends measured values
        measure=lists1[abc]
        graphs(measure[4::10],'Channel '+channel_nos[abc],'Channel '+channel_nos[abc]+'.png')
    
#access_data('(echo "bandmon s"; sleep 1) | hyt' , '@ Blackout state ' , '@ ')


    

#................1)sum of all VSZ values vs time
#                2)used (memory) vs time.............................................................


def tocalsum(list1):
    single_ps=[]
    vsz=[]
    sum1=0
    for b in list1:
        single_ps.append(re.split(r'[|\s]\s*', b))
    for x in single_ps:
        for y in range(len(x)):
            if x[y]=='root' and x[y+2]=='S':
                vsz.append(x[y+1])
    for a in vsz:
        sum1=sum1+int(a)
    return sum1
        
def process_sum(logfile,catch_start,catch_end):
    results = []
    t=0
    pstime=[]
    vsz_sum=[]
    diffvsz=[]
    tim=[]
    used=[]
    bufcach=[]
    diff_used=[]
    with open(logfile, 'r') as f1:
        lines = f1.readlines()
    i = 0
    while i < len(lines):
        if '-/+ buffers/cache:' in lines[i]:
           bufcach.append(re.split(r'[|\s]\s*',lines[i])) 
        if catch_start in lines[i]:
            pstime.append(re.split(r'[|\s]\s*',lines[i]))
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    k=0
    for a in results:
        vsztot = tocalsum(a)
        vsz_sum.insert(k,vsztot)
        k=k+1
    for d in range(len(vsz_sum)-1):
        diffvsz.append(abs(vsz_sum[d]-vsz_sum[d+1]))
    for e in bufcach:
        used.append(e[2])
    for d in range(len(used)-1):
        diff_used.append(abs(int(used[d])-int(used[d+1])))
    for m in pstime:
           tim.append(m[2]+" "+m[3])
    tim.remove(tim[0])
    date_obj = []
    for temp in tim:
        date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
    dates = md.date2num(date_obj)
    
    Data_Plotting(dates,diffvsz,'Difference in sum of VSZ values','Consecutive diff in sum of vsz','Diff_sum_of_VSZ.png' )
    Data_Plotting(dates,diff_used,'Difference in Used vaues','Consecutive diff in used memory','Diff_used_memory.png')
   

#................Prints the CPU% , date and time, Process name for values=>threshold......................................
    
def top_cmd(catch_start,catch_end,logfile,thresh):
    results=[]
    line=[]
    per=[]
    final=[]
    threshold=thresh
    with open(logfile, 'r') as f1:
        lines = f1.readlines()
        i = 0
        while i < len(lines):
            if catch_start in lines[i]:
              for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i+1:j])
                    i = j
                    break
            else:
              i += 1

    for a in results:
        for b in a:
           if 'root' in b:
              line.append(re.split(r'[|\s]\s*',b))
    print("CPU%         Date & Time                        Process") 
    for b in line:
        if int(b[6].rstrip("%")) >= threshold:
            pro= " ".join(b[7:(len(b)-3)])
            final.append(" %-12s %-35s %s" %(b[6],b[(len(b)-3)]+" "+b[(len(b)-2)],pro))
    if len(final)==0:
        print("No values are found")
    else:
        for v in final:
            print(v)




#........................VSZ first and last delta values for given process...............................................

def process_data(catch_start,catch_end,process_name,logfile):           #accesses the data portion specified by the parameters
    results = []
    pro=[]
    vsz=[]
    date_time=[]
    variations=[]
    with open(logfile, 'r') as f1:
        lines = f1.readlines()
    i = 0
    while i < len(lines):                                               
        if catch_start in lines[i]:
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    c=0
    d=0
    for a in results:                                               #accessed the part of data, now to find the portions of data having the req process name
        for b in a:
            d+=1                                                    #to keep a count of all lines having process names
            if process_name in b:
                pro.append(re.split(r'[|\s]\s*', b))                #appended the lines of req process in a list(=pro)
            else:
                c+=1                                                #to keep a count if process name is not present in the file
    if c==d:                                                        #if no line has the process name then display the following else do required steps
        print(process_name+" process is not found in this file\n")
    else:
        for x in pro:
            for y in range(len(x)):
                if x[y] == 'root':
                   vsz.append(x[y+1])                               #get VSZ values
        length=len(x)
        date_time.append(x[length-3]+" "+x[length-2])
        date_obj = []
        for temp in date_time:
            date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
        dates = md.date2num(date_obj)
        vsz_len= len(vsz)                                           
        val=list(set(vsz))
        last=int(vsz[vsz_len-1])
        first=int(vsz[0])
        delta= last-first                                           #for each process, find difference between its first and last VSZ value i.e delta
        print('Process: '+process_name)
        if last > first:
            print("VSZ lastvalue is more than firstvalue.")
            #Data_Plotting(dates,vsz,process_name)
        elif last < first:
            print("VSZ lastvalue is less than firstvalue.")
        elif last == first:
            print("The first and last VSZ value are same.")
        if len(val)==1:                                             #to check if there are variations in vsz values or not
            print("All the VSZ values are same")
        else:
            print("There are variations seen in VSZ values across all values")    
        print("Delta: ",delta)
        print('\n')
                       
    
#fname=logfile, process_list=takes process list from config file,vsz_start & vsz_end= start and end strings, data between them will be used           
def access_pro(fname,process_list,vsz_start,vsz_end):           
    for x in process_list:
        process_data(vsz_start,vsz_end,x,fname)


#....................Wifistats wifi 9 and 10:
#                    1)Pie Chart of MCS Values at the "end of test" for Tx and Rx and for each radio
#                    2) % Usage of each MCS value as a function of time for Tx and Rx..........................................................

def to_cal_percent(rate):
    rates=rate
    tminus1=[]
    t=[]
    delta_list=[]
    percent=[]
    curve=[]
    for z in range(len(rates)-1):                                       #make empty lists to append the delta values and %s
            delta_list.append([])
            percent.append([])
    count=0
    for x in range(len(rates)-1):                                       #Here 2 adjacent lists and their elements are subtracted
            count+=1
            tminus1=rates[x]
            t=rates[x+1]
            for (m,n) in zip(tminus1,t):
                delta=int(n)-int(m)
                delta_list[count-1].append(delta)
    co=0
    for s in delta_list:                                                #to find the %
            sum1=0
            co+=1
            for r in s:
                sum1=sum1+int(r)
            if sum1!=0:                
                for r in s:
                    per=int(r)/sum1
                    percent[co-1].append(per)                   
            else:
                break
    mcs_size=len(percent[0])
    for x in range(mcs_size):
        curve.append([])
    coun=0
    for y in range(mcs_size):                                           #to collect all 0:values, 1:values in seperate lists            
        coun+=1                             
        for z in percent:                   
            curve[coun-1].append(z[y])
    
    return curve

def curves(yaxis,times,start,end):                                      #to plot the graph
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks( rotation=30, horizontalalignment='right' )
    #colormap = plt.cm.gist_ncar
    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, len(yaxis)+1))))
    for i in range(len(yaxis)):
        plt.plot(times,yaxis[i],label=i)
        lis=yaxis[i]
        plt.text(times[i],lis[i],i)
     
    plt.title(start.replace(end,' '))    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('CURVES'+start.replace(end,' ')+'.png',bbox_inches='tight')
    plt.clf()
    #plt.show()
        
    
def wifistats(catch_start,catch_end,file):
    results = []
    mcs=[]
    last=[]
    rates=[]
    curv=[]
    tim=[]
    time1=[]
    with open(file, 'r') as f1:
        lines = f1.readlines()        
    i = 0
    while i < len(lines):
        if catch_start in lines[i]:
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    if(len(results))==0:
        print("No values are read for wifistats"+catch_start.replace(catch_end,' '))
    else:
        if "9" in catch_start:                                                        #tx_mcs classification
            for a in results:
                for b in a:
                    if 'tx_mcs' in b and not 'ac_mu_mimo_tx_mcs' in b and not "ax_mu_mimo_tx_mcs" in b and not "ofdma_tx_mcs" in b :
                        mcs.append(re.split(r'[:,\s]\s*', b))
                        time1.append(re.split(r'[|\s]\s*',b))

            for a in mcs:
                rates.append(a[3:30:2])                                             #list only of rates
            curv= to_cal_percent(rates)                                             #function call and recieves %tx_mcs
            del time1[0]
            for l in time1:                                                         #time axis
                tim.append(l[16]+" "+l[17])
            date_obj = []
            for temp in tim:
                date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
            dates = md.date2num(date_obj)
            curves(curv,dates,catch_start,catch_end)                                #calls for the graph
            last=mcs[len(mcs)-1]
            labels = last[2:29:2]                                                   #collect last values for piechart
            for i in range(0, len(labels)): 
                labels[i] = int(labels[i])
            sizes = last[3:30:2]
            for j in range(0, len(sizes)):
                sizes[i] = int(sizes[i])        
        elif "10" in catch_start:                                                   #rx_mcs classification
            for a in results:
                for b in a:
                    if 'rx_mcs' in b and not "ul_ofdma_rx_mcs" in b:
                        mcs.append(re.split(r'[:,\s]\s*', b))
                        time1.append(re.split(r'[|\s]\s*',b))
            for a in mcs:
                rates.append(a[3:26:2])
            curv= to_cal_percent(rates)
            del time1[0]
            for l in time1:
                tim.append(l[14]+" "+l[15])
            date_obj = []
            for temp in tim:
                date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
            dates = md.date2num(date_obj)
            curves(curv,dates,catch_start,catch_end)
            last=mcs[len(mcs)-1]
            labels = last[2:25:2]
            for i in range(0, len(labels)): 
                labels[i] = int(labels[i])
            sizes = last[3:26:2]  
            for j in range(0, len(sizes)):
                sizes[i] = int(sizes[i])    
        fig1, ax1 = plt.subplots()
        plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, len(curv)))))
        ax1.pie(sizes , labels=labels,shadow=False, startangle=90)                  #piechart plot       
        ax1.axis('equal')
        ax1.set_title(catch_start.replace(catch_end,' '))
        plt.savefig('Piechart_'+catch_start.replace(catch_end,' ')+'.png')
        plt.clf()
        #plt.show()

def wifistats_call(logfile,wifi):
    for a in wifi:
        wifistats(":/# wifistats "+a ,":/#",logfile)

"""cmap = plt.get_cmap('Paired')
    colors = [cmap(i) for i in np.linspace(0, 1, len(yaxis))]
    for i,color in zip(range(len(yaxis)),colors):
        plt.plot(times,yaxis[i],color=color, label=i)
"""

#...................Command: ":/# cat /proc/meminfo" plots multiple parameters curves (kB) vs time

def Data_Plotting_withoutclf(x,y,title,yaxis,sa):
    ax=plt.gca()
    #fig = plt.figure()
    plt.subplots_adjust(bottom=0.3)
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks( rotation=30, horizontalalignment='right' )
    if "Memory" == yaxis or "CPU Values" == yaxis:
        plt.ylim(ymax = 100, ymin = 0)
    plt.plot(x,y,label =yaxis)
    plt.title(title)
    plt.xlabel('Duration')
    plt.ylabel(yaxis)
    plt.legend()
    plt.savefig(sa,bbox_inches='tight')
    #plt.clf() 
    #plt.show()                                                             
    

def cat_proc_meminfo(catch_start,catch_end,plot_parameter,logfile):           #accesses the data portion specified by the parameters
    lisst=[]
    values=[]
    results=[]
    tim=[]
    with open(logfile, 'r') as f1:
        lines = f1.readlines()
    i = 0
    while i < len(lines):                                               
        if catch_start in lines[i]:
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    for a in results:
        for b in a:
            if plot_parameter in b:
                lisst.append(re.split(r'[|\s]\s*', b))
    for x in lisst:
        for y in range(len(x)):                                             # access the values of the parameter specified
            if x[y] == 'kB':
                values.append(int(x[y-1]))
                tim.append(x[len(x)-3]+" "+x[len(x)-2])
    date_obj = []
    for temp in tim:
        date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
    dates = md.date2num(date_obj)
    Data_Plotting_withoutclf(dates,values,"curves",plot_parameter+" (in kB)","cat_proc_meminfo")
    
    
def call_cat_proc_meminfo(catch_start,catch_end,logfile,parameter_list):
    for i in parameter_list:
        cat_proc_meminfo(catch_start,catch_end,i,logfile)


#Pooja....................calculate: a)total process ids
#                                    b)number of unique process ids
#                                    c)for each unique process id calculate percentage duration command used - "ps"

'''
input : log_file
output : percentage duration of each unique process id
'''

def perpid(fname , process):
    #open ,read and extract the process id information from log-file
    infile =open(fname,"r")
    lines= infile.readlines()
    temp = open("temp.txt",'w+')
    v=False

    for i in lines:
        i=i.strip()
        if conf.device_prompt+" ps" in i:
            v=True
        elif conf.device_prompt in i:
            v=False
        elif v:
            temp.write(i+"\n")
    temp.close()
    temp = open("temp.txt",'r+')
    out =open("out.txt","w+")
    pid=[]

    olines=temp.readlines()
    
    #extract all process-ids into list
    for i in olines:
        i=i.strip()
        if re.match(r'^[0-9].*',i):
            out.write(i+"\n")
            pid.append(i.split(' ')[0])

    print("total pid under ps command : ",len(pid))
    
    #get unique process-ids
    upid = [] 
    for x in pid:
        if x not in upid:
            upid.append(x) 
                
    print("total count of unqiue pid is : ",len(upid))

    
    freq = {} 
    for i in pid:
        if i in upid:
            if (i in freq): 
                freq[i] += 1
            else: 
                freq[i] = 1
                
    res=open("result.txt",'w+')
    for key, value in freq.items():
        print("percentage duration of PID ",key," is \t ", value,file=res)

    res.close()


    res=open("result.txt",'r')

    #altercode-->percentage duration of each process given in list
    a={}
    for i in process:
         a[i] = []
    ol=open("out.txt","r")
    olr=ol.readlines()
    for j in process:
        for i in olr:
            if  j in i and i.split(' ')[0] not in a[j]:
                a[j].append(i.split(' ')[0])
    
    
    for j in process:     
        res=open("result.txt",'r')
        print("\npercentage duration of process ",j," : ")
        t1=0
        for line in res:
            for x in a[j]:      
                if re.match(r"percentage duration of PID  "+x+"  is.* ",line):
                    t1+=int(line[38:])
                    break
        print("total matched process : " ,t1)
        res=open("result.txt",'r')
        for line in res:
            for p in a[j]:
                if re.match(r"percentage duration of PID  "+p+"  is.* ",line):
                    print("pid : ",p," -> ",(int(line[38:])/t1)*100)
                    break
        res.close()   
    
    infile.close()
    temp.close()
    out.close()

#.................Process "uptime" parameter to find if device rebooted;input:log-file;output:print if device has rebooted.....................


'''
input : log-file
output: print if device rebooted 
'''

def uptime(fname):
    #open and read lines from log-file
    infile=open(fname,"r")
    lines=infile.readlines()
    upout=open("uptime.txt","w+")
    v = False

    for line in lines:
        line=line.strip()
        if conf.device_prompt+" uptime" in line:
            v=True
        elif conf.device_prompt+" free" in line:
            v=False
        elif v:
            upout.write(line+"\n")

    upout.close()
    upout=open("uptime.txt","r")
    upl=upout.readlines()

    tmp=[]

    uptemp=open("uptime.txt","r")
    uplt=uptemp.readlines()
    for i in uplt:
        j=i.find("load")
        tmp.append(i[12:j-3])

    tmp3=[]
    
    #convert the sliced value of uptime into integer and reduce it into seconds
    for i in tmp:
        if "min" in i and ":" not in i and "day" not in i :
            m=i[0:2]
            tmp3.append(int(m)*60)
        elif ":" in i and "day" not in i and "min" not in i:
            h, m = i.split(':')
            tmp3.append(int(h) * 3600 + int(m)*60)
        elif "day" in i and "min" in i:
            tmp3.append(int(i[0])*24*3600+int(i[7:9])*60 )
        elif "day"  in i and ":" in i:
            d=int(i[0])
            m,s=int(i[7:9]),int(i[10:12])
            tmp3.append(d*24*3600+m*3600+s*60 )
    tmp2=copy.deepcopy(tmp3)  
    tmp2.sort()
    c=0
    #compare if items in orginal list(containing seconds) to get number of restarts
    for i in range(1,len(tmp3)-1):
        if tmp3[i]<tmp3[i+1]:
           continue
        else:
            c=c+1
    print("number of reboots : ",c)
    if len(tmp2) !=0 and len(tmp3) != 0:
        
        if tmp2==tmp3:
            print("No problem in uptime")
        else:
            print(" Device has rebooted   ")
    else:
        print("error !!! either value assigned to logfile or device_prompt is incorrect \n")
    infile.close()

      
#..........Calculate and plot throughput graph for Wireless interface(throughput calculated interms of Mbps).....

'''
input : log-file
output: throughput graphs for Tx,Rx,Tx+Rx databytes
'''

def throughput(fname):
    print(" Throughput Graphs \n") 
    infile=open(fname,"r")
    lines=infile.readlines()
    txfile=open("txfile.txt","w+")
    rxfile=open("rxfile.txt","w+")
    
    #gather lines Tx Databytes and Rx Databytes into seperate files 
    for line in lines:
        if "Tx Data Bytes" in line:
            txfile.write(line)
        elif "Rx Data Bytes" in line:
            rxfile.write(line)

    txb=[]
    txt=[]
    txfile=open("txfile.txt","r")
    tl=txfile.readlines()

    #separate Databytes and time_series on given line
    for i in tl:
        txb.append(i.split('=')[1].split('|')[0])
        txt.append(i.split('|')[1].split('.')[0])

    #throughput calculation for Tx
    txt1=copy.deepcopy(txt)  
    txb = [int(i) for i in txb]
    txt = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in txt]
    
    
    tdelb = [txb[i + 1] - txb[i] for i in range(len(txb)-1)]
    tdelt = [(txt[i + 1] - txt[i]).total_seconds() for i in range(len(txt)-1)]

    
    
    tput=[((tdelb[i])*8)/(tdelt[i]*math.pow(10,6)) for i in range(0,len(tdelb))]
    

    txt1 = [datetime.strptime(txt1[x],'%Y-%m-%d %H:%M:%S') for x in range(len(txt1)-1)]
        
    dates = md.date2num(txt1)

    Data_Plotting(dates,tput,"Througput graph for tx databytes",'Mbps',"txtput.png") #Data_Plotting(x,y,title,yaxis,savefig1)

    #throughput calculation for Tx
    rxb=[]
    rxt=[]
    rxfile=open("rxfile.txt","r")
    rl=rxfile.readlines()

    for i in rl:
        rxb.append(i.split('=')[1].split('|')[0])
        rxt.append(i.split('|')[1].split('.')[0])
    rxt1=copy.deepcopy(rxt)  
    rxb = [int(i) for i in rxb]
    rxt = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in rxt]
    

    rdelb = [rxb[i + 1] - rxb[i] for i in range(len(rxb)-1)]
    rdelt = [(rxt[i + 1] - rxt[i]).total_seconds() for i in range(len(rxt)-1)]

    rtput=[((rdelb[i])*8)/(rdelt[i]*math.pow(10,6)) for i in range(0,len(rdelb))]
    

    ttput=[(tput[i]+rtput[i]) for i in range(len(tput))] 
    #print(" check : ",tput[0]," ",rtput[0] ," is " ,ttput[0])
    
    rxt1 = [datetime.strptime(rxt1[x],'%Y-%m-%d %H:%M:%S') for x in range(len(rxt1)-1)]
        
    dates = md.date2num(rxt1)
    
    Data_Plotting(dates,rtput,"Througput graph for rx databytes",'Mbps',"rxtput.png")
    Data_Plotting(dates,ttput,"Througput graph for tx+rx databytes",'Mbps',"tot_throughput_1.png")

#.........................1)track changes in network topology
#    2)track:a.number of satellites connected to the router b.type of network topology used c.check if there is a change in network.......


'''
input:log-file
output:printing network topology information and checking for change in topology
'''

def network(fname):
    file1 = open(fname,"r")
    lines = file1.readlines()
    file2 = open("temp.txt","w+")
    for i in lines:
        if i!="\n":
            file2.write(i)
    file2.close()
    f3=open("temp.txt","r")
    line=f3.readlines()
    dno=[]
    ip=[]
    for i in line:
        i=i.strip()
        if re.match(r"^-- DB (.*):",i):
            dno.append(i[7:9])
        elif re.match(r"^QCA IEEE 1905.1 device:.*",i):
                ip.append(i[24:41])
    
    
    f3.close()
    dno=[int(i) for i in dno]
    ul=[]
    for x in dno: 
        if x not in ul: 
            ul.append(x) 
    ul.sort(reverse=True)
    
    g = globals()
    for i in range(1,ul[0]+1):
         g['sat_{}'.format(i)] = []
         g['rel_{}'.format(i)] = []
         g['ups_{}'.format(i)] = []
         
    f3=open("temp.txt","r")
    line=f3.readlines()
    f4=open("tmp1.txt","w+")
    for i in line:
        for j in range(1,ul[0]+1):
            i=i.strip()
            if re.match(r"^#"+str(j)+".*",i):
                      f4.write(i+"\n")
                      break
            elif re.match(r"^Upstream Device:.*",i):
                      f4.write(i+"\n")
                      break
    f4=open("tmp1.txt","r")
    lines=f4.readlines()
    pre=""
    #fetching satellite address,relation,upstream info
    for i in lines:
        for j in range(1,ul[0]+1):
            if re.match(r"^Upstream Device:.*",i)and re.match(r"^#"+str(j)+".*",pre):
                  g['ups_%s' % j].append(i[17:34])
        pre=i
    f3=open("temp.txt","r")
    line=f3.readlines()
    prev=""

    for i in line:
        for j in range(1,ul[0]+1):
            i=i.strip()
            if re.match(r"^#"+str(j)+".*",i):
                  g['sat_%s' % j].append(i[28:45])
                
            elif re.match(r"Relation:.*",i) and re.match(r"^#"+str(j)+".*",prev):
                g['rel_%s' % j].append(i[10:25])
            
        prev=i
    f3.close()
    
    f=False
    trel=[]
    #checking if there is any change in topology
    for i in range(0,len(ip)):
        for j in range(1,ul[0]+1):
            if g['rel_%s' % j][i]=="Direct Neighbor" :
                f=True
                continue
            else:
                f=False
                break
        if f==True:
            trel.append("Star")
            
        else:
            trel.append("Daisy chain")

    #printing the router-satellite connectivities
    for i in range(0,len(ip)):
            print("\niteration ",i+1)
            print("router : "+ip[i]+" is connected to "+str(dno[i])+" satellites ")
            if trel[i]=="Star":
                    print("Satellites follows Star topology ")
                    
            else:
                    print("Satellites follows Daisy Chain topology ")
                    
       
    print("\n")
    m=0
    #check for change in topology (considering attributes such as MAC address,number_of_satellites,upstream,type_of topology)
    for i in range(1,ul[0]+1):
            if all(ele == g['sat_%s' % str(i)][0] for ele in g['sat_%s' % str(i)]):
                m+=1
                print("No change in MAC address of satellite: "+str(i))
                continue
            else:
            
                print("Change in MAC address of satellite: "+str(i))
                continue
    print("\n")
    for i in range(0,len(dno)-1):
        if dno[i]!=dno[i+1]:
                print("change in number of satellite")
                break
        else:
            print("No change in number of satellite")
            break
    print("\n")
    u=0
    for i in range(1,ul[0]+1):
            if all(ele == g['ups_%s' % str(i)][0] for ele in g['ups_%s' % str(i)]):
                u+=1
                print("No change in upstream of satellite: "+str(i))
                continue
            else:
                
                print("Change in upstream of satellite: "+str(i))
                continue
    print("\n")
    t=0
    for i in range(0,len(ip)-1):
        if trel[i]!=trel[i+1]:
            t+=1
    
    for i in range(0,len(dno)-1):
            if u!=ul[0] and m!=ul[0] and t!=len(ip)-1 :
                print("change in topology ")
                break
            else:
                print("No change in topology ")
                break

#............

'''
input: log-file
output : visualization of the network
'''


def picrep(fname):
    f1=open(fname,"r")
    lines=f1.readlines()
    f2=open("tm.txt","w+")
    c=False
    #open the file and pick lines that are necessary for network visualization
    for i in lines:
        if "-- ME:" in i:
            c=True
        elif "/# exit" in i or re.match(r"@$",i):
            c=False
        elif c==True:
            f2.write(i)
    f2.close()
    f2=open("tm.txt","r")
    line=f2.readlines()
    n=0
    for i in line:
        i=i.strip()
        if re.match(r"^QCA IEEE .*",i):
            ip=i[24:41]
        elif  re.match(r"^-- DB (.*):",i):
            n=int(i[7:9])
    
    f2=open("tm.txt","r")
    line=f2.readlines()
    sat=[]
    rel=[]
    ups=[]
    j=1
    #slicing the previously processed lines to get satellite address,its relation and to which device it is connected
    for i in line:
        i=i.strip()
        if re.match(r"^#"+str(j)+": QCA IEEE .*",i):
                sat.append(i[28:45])
                j=j+1
        elif re.match(r"^Relation: .*",i):
                rel.append(i[10:25])
        elif re.match(r"^Upstream Device:.*",i)and "Upstream Device: None" not in i:
                ups.append(i[17:34])
    #printing the contents of list in required format
    for i in range(n):
        if rel[i]=="Direct Neighbor" and sat[i] not in ups:
            print(ip+"(Router) <----- "+sat[i]+"(Satellite "+str(i+1)+")")
        else:
            for j in range(n):
                if ups[i]==sat[j]:
                    print(ip+"(Router)<----- "+ups[i]+"(Satellite "+str(j+1)+") <----- "+sat[i]+"(Satellite "+str(i+1)+")")
                    break
                
#...............


def throughputeth(fname,thl):
    print(" Throughput Graphs \n") 
    infile=open(fname,"r")
    lines=infile.readlines()

    txfile=open("txfile.txt","w+")
    rxfile=open("rxfile.txt","w+")
    ttfile=open("tmp3.txt","w+")
    tmp=open("tmp2.txt","w+")
    ttt=open("ttt.txt","w+")
    ttr=open("ttr.txt","w+")
    
    c=False
    j=0
    prev=""
    txb=[]
    txt=[]
    rxb=[]
    rxt=[]
    l1=[]
    l2=[]
    #group first instance
    for k in thl:
            for i in range(len(lines)) :
                lines[i]=lines[i].strip()
                if re.match(r"^"+k+" .*",lines[i]):
                    l1.append(k)
                    break
                elif k in lines[i] and not re.match(r"^"+k+" .*",lines[i]):
                    l2.append(k)
                    break

    infile=open(fname,"r")
    lines=infile.readlines()           
    for k in l1:
            print("\n\nThroughput graph for "+k)
            for i in range(len(lines)) :
                lines[i]=lines[i].strip()
                
                if re.match(r"^"+k+" .*",lines[i]) and "no wireless extensions." not  in lines[i]:
                        for j in range(i,len(lines)):
                        
                            if re.match(r"^RX bytes.*",lines[j]):
                                txb.append(lines[j].split("TX bytes:")[1].split(' ')[0])
                                rxb.append(lines[j].split('RX bytes:')[1].split(' ')[0])
                                txt.append(lines[j].split("|")[1].split('.')[0])
                                rxt.append(lines[j].split("|")[1].split('.')[0])
                                break
                
   
            
            tdelb=[]
            txt1=copy.deepcopy(txt)  
            txb = [int(i) for i in txb]
            txt = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in txt]
            ndata=0
            for i in range(1,len(txb)):
                if txb[i]<txb[i-1]:
                    ndata=4294967295-txb[i-1]+txb[i]
                    #x=ndata-txb[i-1]
                    tdelb.append(ndata)
                    #print(i)
                    
                else:
                    x = txb[i] - txb[i-1]
                    tdelb.append(x)
                    
 
            
            #tdelb = [txb[i+1]-txb[i] for i in range(len(txb)-1) ]
            tdelt = [(txt[i + 1] - txt[i]).total_seconds() for i in range(len(txt)-1)]
          
            
            tput=[((tdelb[i])*8)/(tdelt[i]*math.pow(10,6)) for i in range(0,len(tdelb))]
            
            
            txt1 = [datetime.strptime(txt1[x],'%Y-%m-%d %H:%M:%S') for x in range(len(txt1)-1)]
                
            dates = md.date2num(txt1)
            Data_Plotting(dates,tput,"Througput graph for tx databytes",'Mbps',"txtput_1.png")
        
            rdelb=[]
            rdata=0
            rxt1=copy.deepcopy(rxt)  
            rxb = [int(i) for i in rxb]
            rxt = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in rxt]
            for i in range(1,len(rxb)):
                if rxb[i]<rxb[i-1]:
                    rdata=4294967295-rxb[i-1]+rxb[i]
                    #x=rdata-rxb[i-1]
                    rdelb.append(rdata)
                    #rdelb.append(x)
                    
                else:
                    x = rxb[i] - rxb[i-1]
                    rdelb.append(x)

          
            rdelt = [(rxt[i + 1] - rxt[i]).total_seconds() for i in range(len(rxt)-1)]

            rtput=[((rdelb[i])*8)/(rdelt[i]*math.pow(10,6)) for i in range(0,len(rdelb))]
            
            
            ttput=[(tput[i]+rtput[i]) for i in range(len(tput))] 

            

            rxt1 = [datetime.strptime(rxt1[x],'%Y-%m-%d %H:%M:%S') for x in range(len(rxt1)-1)]
                
            dates = md.date2num(rxt1)
            Data_Plotting(dates,rtput,"Througput graph for rx databytes",'Mbps',"rxtput_1.png")
            Data_Plotting(dates,ttput,"Througput graph for tx+rx databytes",'Mbps',"tot_throughput_1.png")
    
      
            txb=[]
            txt=[]
            rxb=[]
            rxt=[]

    for i in l2:
        print("\n\n"+i+" is not a valid interface")

#...............


