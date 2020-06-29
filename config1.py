logfile='alpha_board_router_stats.txt'

avg=['Average:          all','Average:          0','Average:          1','Average:          2','Average:          3']
memory= "Mem:      "

interface_list=['ath0','ath1','ath2']

fname='router_stats.txt'
channel_start_cmd='(echo "bandmon s"; sleep 1) | hyt'
middle='@ Blackout state '
channel_end_cmd='@ '

#logfile1='alpha_board_router_stats_one.txt'

vsz_start=":/# ps"
vsz_end=":/#"

process_lis=['hostapd -g', 'wpa_supplicant -g', 'check_fw','dal_cb_handler','check_ra','guster/guster -c guster.yaml -c ','/opt/xagent/xagent -w -d --log_debug --ca_file /opt/',
'/opt/xagent/xagent -w -d --log_debug --ca_file /opt/','d2 -w XagentCtrl.xcenv','/upagent --log_debug --log_file /','./aws_json','/hyd-lan.conf -P 7777 -cfg80','/hostapd-wifi2 -P /',
'/dalh --log_debug --log_file /','/bst_daemon --log_debug --log_file /','/bdcrashd -start -no-detach','/bdsetter -start -no-detach -sav','/bdexchanged -start -no-detach',
'/bdcloudd -start -no-detach','/bdboxsettings -start -no-detach','/bddevicediscovery -start -no-de','/bdbrokerd -start -no-detach','/bdvad -start -no-detach',
'/bdgusterupdd -start -no-detach','/bdgusterd -start -no-detach','/bdheartbeatd -start -no-detach','dal_ash --log_debug --log_file /','/bdpush -c /','hyd-guest.conf',
'/bdavahi -scan -interfaces=br-la','/bdupnp -scan -ifname=br-lan','/bdleases','/guster/gusterupd -r /','/wsplcd-lan.conf    -cfg8021','/wsplcd-guest.conf  -cfg8021']


st=':/# top -b -n'
ed=':/# ps'
thresh=5

#logfile2='alpha_board_router_stats_two.txt'
wifi=['wifi0 9',"wifi0 10"]

cs=":/# cat /proc/meminfo"
ce=":/# "
pp=["MemTotal","MemFree"]

#Pooja's prog
#logfile='alpha_board_router_stats.txt'
process_list=['hyd-guest.conf','hyd-main.conf','hyd-lan.conf','wsplcd-lan.conf','wsplcd-guest.conf','/tmp/udhcpd.conf','hostapd_cli -i ath01']
device_prompt='root@RBR850:/#'

#logfile='alpha_board_router_stats.txt'
#device_prompt='root@RBR850:/#

thrad="radio_0_stats.txt"

nwfile="Router_Topology_Stats.txt"

topo="topo_stats.txt"

#thfile="alpha_board_router_stats_1.txt"
thl=['eth0      Link encap:Ethernet','br-lan    Link encap:Ethernet','wifi0     Link encap:UNSPEC','eth']
