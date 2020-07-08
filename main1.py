import config1 as conf
import commonfunc as cf


cf.Data_preparation(conf.logfile,conf.avg,conf.memory)     #CPU N MEM
cf.Call_dataspecific(conf.interface_list,conf.logfile)     #WLAN CONFIG
cf.Call_uptimelist(conf.interface_list,conf.logfile)       #UPTIME
cf.channel_utilisation(conf.channel_start_cmd,conf.middle,conf.channel_end_cmd,conf.fname)          #CHANNEL UTILISATION
cf.access_pro(conf.logfile,conf.process_lis,conf.vsz_start,conf.vsz_end)               #SPECIFIC PROCESS
cf.process_sum(conf.logfile,conf.vsz_start,conf.vsz_end)   #VSZ SUM AND FREE COMMAND
cf.top_cmd(conf.st,conf.ed,conf.logfile,conf.thresh)       #CPU%>THRES
cf.wifistats_call(conf.logfile,conf.wifi)                  #WIFISTATS WIFI(0/1)
cf.call_cat_proc_meminfo(conf.cs,conf.ce,conf.logfile,conf.pp)
cf.console(conf.fil,conf.key)
cf.perpid(conf.logfile,conf.process_list)
cf.uptime(conf.logfile)
cf.throughput(conf.thrad)
cf.network(conf.nwfile)
cf.picrep(conf.topo)
cf.throughputeth(conf.logfile,conf.thl)




