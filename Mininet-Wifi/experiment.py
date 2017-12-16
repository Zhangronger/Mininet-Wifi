# !/usr/bin/python

"""
Network Management Spring Semester 17 - Project
Team Members:
Giorgos Kallis 1115201200046
Alkiviadis Kwtsas 1115200900072
Vasilopoulos Petros 1115201000218
Ananias Potamitis 1115200900239

Task 1: Implementation of the experiment described in the paper with title: 
"From Theory to Experimental Evaluation: Resource Management in Software-Defined Vehicular Networks"

##################################################################
Total packets sent/received,packets dropped,throughput and latency 
are calculated and demonstrated graphically inside this script.
##################################################################
 To get rssi,channel and frequency, from CLI type:
 py car0.params['rssi']
 py car0.params['channel']
 py car0.params['frequency']
##################################################################
 To get jitter and bandwidth, from CLI type:
 xterm client  ---->  iperf -s -u -i 1
 xterm car0    ---->  iperf -c 200.0.10.2 -u -i 1
"""

import os
import time
import matplotlib.pyplot as plt
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.link import TCLink
from mininet.log import setLogLevel, debug
from mininet.cli import CLI

import sys
gnet=None

client_packets = 'client-packets.data'
client_throughput = 'client-throughput.data'
client_loss = 'client-loss.data'
car0_packets = 'car0-packets.data'
car0_throughput = 'car0-throughput.data'
car0_loss = 'car0-loss.data'
client_bandwidth = 'client-bandwidth.data'
client_jitter = 'client-jitter.data'
client_latency = 'client-latency.data'

#how many seconds each phase lasts
PhaseTime = 5

# Implement the graphic function in order to demonstrate the network measurements
# Hint: You can save the measurement in an output file and then import it here
    
def graphic1():
	
    # initialize empty lists:
    time = []
    pck1 = []
    pck2 = []
    thr1 = []
    thr2 = []   
    lpck1 = []
    lpck2 = []
    tthr1 = []
    tthr2 = []
    
    file1 = open('client-packets.data', 'r')
    client1 = file1.readlines()
    file1.close()

    file2 = open('client-throughput.data', 'r')
    client2 = file2.readlines()
    file2.close()

    file3 = open('car0-packets.data', 'r')
    car01 = file3.readlines()
    file3.close()

    file4 = open('car0-throughput.data', 'r')
    car02 = file4.readlines()
    file4.close()
    
    # scan the rows of the file stored in lines, and put the values into some variables:
    i = 0
    for j in client1:    
        field = j.split()
        pck1.append(int(field[0]))
        if len(pck1) > 1:
            lpck1.append(pck1[i] - pck1[i - 1])
        i += 1
    
    i = 0
    for j in client2:    
        field = j.split()
        thr1.append(int(field[0]))
        if len(thr1) > 1:
            tthr1.append(thr1[i] - thr1[i - 1])
        i += 1
    
    i = 0
    for j in car01:    
        field = j.split()
        pck2.append(int(field[0]))
        if len(pck2) > 1:
            lpck2.append(pck2[i] - pck2[i - 1])
        i += 1
    
    i = 0
    for j in car02:    
        field = j.split()
        thr2.append(int(field[0]))
        if len(thr2) > 1:
            tthr2.append(thr2[i] - thr2[i - 1])
        i += 1
    
    i = 0
    for j in range(len(lpck1)):    
        time.append(i)
        i += 0.5
    
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    ax1.plot(time, lpck1, color='red', label='Client-Received Data', markevery=7, linewidth=1)
    ax1.plot(time, lpck2, color='black', label='Car0-Transmited Data', markevery=7, linewidth=1)
    ax2.plot(time, tthr1, color='red', label='Client-Throughput', ls="--", markevery=7, linewidth=1)
    ax2.plot(time, tthr2, color='black', label='Car0-Throughput', ls='--', markevery=7, linewidth=1)
    
    ax1.legend(loc=2, borderaxespad=0., fontsize=12)
    ax2.legend(loc=1, borderaxespad=0., fontsize=12) 

    ax2.set_yscale('log')

    ax1.set_ylabel("Total Packets", fontsize=16)
    ax1.set_xlabel("Time (sec)", fontsize=16)
    ax2.set_ylabel("Throughput (bytes/sec)", fontsize=16)

    plt.show()
    plt.savefig("GraphicFunction1.eps")
    
def graphic2():
	
	time = []
	
	loss1 = []
	loss2 = []
	lloss1 = []
	lloss2 = []

	file5 = open('client-loss.data', 'r')
	client3 = file5.readlines()
	file5.close()
    
	file6 = open('car0-loss.data', 'r')
	car03 = file6.readlines()
	file6.close()
    
	i = 0
	for j in client3:    
		field = j.split()
		loss1.append(int(field[0]))
		if len(loss1) > 1:
			lloss1.append(loss1[i] - loss1[i - 1])
		i += 1
    
	i = 0
	for j in car03:    
		field = j.split()
		loss2.append(int(field[0]))
		if len(loss2) > 1:
			lloss2.append(loss2[i] - loss2[i - 1])
		i += 1
    
	i = 0
	for j in range(len(lloss1)):    
		time.append(i)
		i += 0.5
    
	fig, ax1 = plt.subplots()
    
	ax1.plot(time, lloss1, color='red', label='Client-Packets Dropped', markevery=7, linewidth=1)
	ax1.plot(time, lloss2, color='black', label='Car0-Packets Dropped', markevery=7, linewidth=1)
   
	ax1.legend(loc=2, borderaxespad=0., fontsize=12)
    
	ax1.set_ylabel("Packets Dropped", fontsize=16)
	ax1.set_xlabel("Time (sec)", fontsize=16)

	plt.show()
	plt.savefig("GraphicFunction2.eps") 

def graphic3():
	
	time = []
	
	bw1 = []
	bw2 = []

	file7 = open('client-bandwidth.data', 'r')
	client4 = file7.readlines()
	file7.close()
    
	i = 0
	for j in client4:    
		field = j.split()
		bw1.append(int(field[0]))
		if len(bw1) > 1:
			bw2.append(bw1[i] - bw1[i - 1])
		i += 1
    
	i = 0
	for j in range(len(bw2)):    
		time.append(i)
		i += 0.5
    
	fig, ax1 = plt.subplots()
    
	ax1.plot(time, bw2, color='green', label='Client Bandwidth', ls='--', markevery=7, linewidth=1)
   
	ax1.legend(loc=2, borderaxespad=0., fontsize=12)
    
	ax1.set_ylabel("Bandwidth", fontsize=16)
	ax1.set_xlabel("Time (sec)", fontsize=16)

	plt.show()
	plt.savefig("GraphicFunction3.eps") 
	
def graphic4():
	
	time = []
	
	jit1 = []
	jit2 = []

	file8 = open('client-jitter.data', 'r')
	client5 = file8.readlines()
	file8.close()
    
	i = 0
	for j in client5:    
		field = j.split()
		jit1.append(int(field[0]))
		if len(jit1) > 1:
			jit2.append(jit1[i] - jit1[i - 1])
		i += 1
    
	i = 0
	for j in range(len(jit2)):    
		time.append(i)
		i += 0.5
    
	fig, ax1 = plt.subplots()
    
	ax1.plot(time, jit2, color='yellow', label='Client Jitter', ls='--', markevery=7, linewidth=1)
   
	ax1.legend(loc=2, borderaxespad=0., fontsize=12)
    
	ax1.set_ylabel("Jitter", fontsize=16)
	ax1.set_xlabel("Time (sec)", fontsize=16)

	plt.show()
	plt.savefig("GraphicFunction4.eps")
	
def graphic5():
	
	time = []
	
	lat1 = []
	lat2 = []

	file9 = open('client-latency.data', 'r')
	client6 = file9.readlines()
	file9.close()
    
	i = 0
	for j in client6:    
		field = j.split()
		lat1.append(float(field[0]))
		if len(lat1) > 1:
			lat2.append(lat1[i] - lat1[i - 1])
		i += 1
    
	i = 0
	for j in range(len(lat2)):    
		time.append(i)
		i += 0.5
    
	fig, ax1 = plt.subplots()
    
	ax1.plot(time, lat2, color='blue', label='Client Latency', markevery=7, linewidth=1)
   
	ax1.legend(loc=2, borderaxespad=0., fontsize=12)
    
	ax1.set_ylabel("Latency", fontsize=16)
	ax1.set_xlabel("Time (sec)", fontsize=16)

	plt.show()
	plt.savefig("GraphicFunction5.eps")
	
def apply_experiment(car,client,switch):

    time.sleep(2)

    print "Applying first phase"

    ################################################################################ 
    #	1) Add the flow rules below and the necessary routing commands
    #
    #	Hint 1: For the OpenFlow rules you can either delete and add rules
    #			or modify rules (using mod-flows command)       
    #	Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #	Hint 2: For the routing commands check the configuration 
    #			at the beginning of the experiment.
    #
    #	2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #		Hint: Remember that you can insert commands via the mininet
    #		Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
	#   			***************** Insert code below *********************  
    #################################################################################
	 
	#!!!Clear the flows every time the station switches to the next access point!!!

    os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    os.system('ovs-ofctl del-flows eNodeB1')
    os.system('ovs-ofctl del-flows eNodeB2')
    os.system('ovs-ofctl del-flows rsu1')

    car[0].cmd('ip route del 200.0.10.2 via 200.0.10.50')
    client.cmd('ip route del 200.0.10.100 via 200.0.10.150')

    TotalTime = time.time() + PhaseTime
    currentTime = time.time()
    i = 0
 
    while True:
        if time.time() > TotalTime:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % car0_packets)
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % client_packets)
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk  \'{print $4}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % car0_loss)
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk \'{print $4}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % client_loss)
            car[0].cmd('ifconfig bond0 | grep \"TX bytes\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % car0_throughput)
            client.cmd('ifconfig client-eth0 | grep \"RX bytes\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % client_throughput)
            #client.cmd('iperf -s -u -i 0.5 | grep \"0.0-\" | awk \'{print $8}\' >> %s' % client_bandwidth)
            #car[0].cmd('iperf -c 200.0.10.2 -u -i 0.5')
            #client.cmd('iperf -s -u -i 0.5 | grep \"0.0-\" | awk \'{print $10}\' >> %s' % client_jitter)
            #car[0].cmd('iperf -c 200.0.10.2 -u -i 0.5')
            car[0].cmd('ping -c 1 200.0.10.2 | grep \"64 bytes\" | awk \'{print $7}\' | awk \'{split($0,a,"="); print a[2]}\'>> %s' % client_latency)
            #every 0.5 seconds add new entry/line to file
            i += 0.5
	
	#CLI(gnet)
	
    print "Moving nodes"
    car[0].moveNodeTo('150,100,0')
    car[1].moveNodeTo('120,100,0')
    car[2].moveNodeTo('90,100,0')
    car[3].moveNodeTo('70,100,0')

    
    time.sleep(2)
    
    print "Applying second phase"
    ################################################################################ 
    #	1) Add the flow rules below and the necessary routing commands
    #
    #	Hint 1: For the OpenFlow rules you can either delete and add rules
    #			or modify rules (using mod-flows command)       
    #	Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #	Hint 2: For the routing commands check the configuration 
    #			you have added before.
    #			Remember that now the car connects to RSU1 and eNodeB2
    #
    #	2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #		Hint: Remember that you can insert commands via the mininet
    #		Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #			***************** Insert code below ********************* 
    #################################################################################
    
    
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2,3')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')
    os.system('ovs-ofctl del-flows eNodeB1')
    os.system('ovs-ofctl del-flows eNodeB2')
    os.system('ovs-ofctl del-flows rsu1')

    car[0].cmd('ip route del 200.0.10.2 via 200.0.10.50')
    client.cmd('ip route del 200.0.10.100 via 200.0.10.150')

    TotalTime = time.time() + PhaseTime
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > TotalTime:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % car0_packets)
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % client_packets)
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk  \'{print $4}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % car0_loss)
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk \'{print $4}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % client_loss)
            car[0].cmd('ifconfig bond0 | grep \"TX bytes\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % car0_throughput)
            client.cmd('ifconfig client-eth0 | grep \"RX bytes\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % client_throughput)
            #client.cmd('iperf -s -u -i 0.5 | grep \"0.0-\" | awk \'{print $8}\' >> %s' % client_bandwidth)
            #car[0].cmd('iperf -c 200.0.10.2 -u -i 0.5')
            #client.cmd('iperf -s -u -i 0.5 | grep \"0.0-\" | awk \'{print $10}\' >> %s' % client_jitter)
            #car[0].cmd('iperf -c 200.0.10.2 -u -i 0.5')
            car[0].cmd('ping -c 1 200.0.10.2 | grep \"64 bytes\" | awk \'{print $7}\' | awk \'{split($0,a,"="); print a[2]}\'>> %s' % client_latency)
            #every 0.5 seconds add new entry/line to file
            i += 0.5
    
    #CLI(gnet)
    
    print "Moving nodes"
    car[0].moveNodeTo('190,100,0')
    car[1].moveNodeTo('150,100,0')
    car[2].moveNodeTo('120,100,0')
    car[3].moveNodeTo('90,100,0')


    time.sleep(2)
    print "Applying third phase"
    
  	################################################################################ 
    #	1) Add the flow rules below and routing commands if needed
    #
    #	Hint 1: For the OpenFlow rules you can either delete and add rules
    #			or modify rules (using mod-flows command)       
    #	Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #
    #	2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #		Hint: Remember that you can insert commands via the mininet
    #		Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #			***************** Insert code below ********************* 
    #################################################################################
    
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')
    os.system('ovs-ofctl del-flows eNodeB1')
    os.system('ovs-ofctl del-flows eNodeB2')
    os.system('ovs-ofctl del-flows rsu1')
    
    car[0].cmd('ip route del 200.0.10.2 via 200.0.10.50')
    client.cmd('ip route del 200.0.10.100 via 200.0.10.150')

    TotalTime = time.time() + PhaseTime
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > TotalTime:
            break;
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % car0_packets)
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % client_packets)
            car[0].cmd('ifconfig bond0 | grep \"TX packets\" | awk  \'{print $4}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % car0_loss)
            client.cmd('ifconfig client-eth0 | grep \"RX packets\" | awk \'{print $4}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % client_loss)
            car[0].cmd('ifconfig bond0 | grep \"TX bytes\" | awk \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % car0_throughput)
            client.cmd('ifconfig client-eth0 | grep \"RX bytes\" | awk  \'{print $2}\' | awk \'{split($0,a,":"); print a[2]}\' >> %s' % client_throughput)
            #client.cmd('iperf -s -u -i 0.5 | grep \"0.0-\" | awk \'{print $8}\' >> %s' % client_bandwidth)
            #car[0].cmd('iperf -c 200.0.10.2 -u -i 0.5')
            #client.cmd('iperf -s -u -i 0.5 | grep \"0.0-\" | awk \'{print $10}\' >> %s' % client_jitter)
            #car[0].cmd('iperf -c 200.0.10.2 -u -i 0.5')
            car[0].cmd('ping -c 1 200.0.10.2 | grep \"64 bytes\" | awk \'{print $7}\' | awk \'{split($0,a,"="); print a[2]}\'>> %s' % client_latency)
            #every 0.5 seconds add new entry/line to file
            i += 0.5
    
    #CLI(gnet)

def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch, accessPoint=OVSKernelAP)
    global gnet
    gnet = net

    print "*** Creating nodes"
    car = []
    stas = []
    for x in range(0, 4):
        car.append(x)
        stas.append(x)
    for x in range(0, 4):
        car[x] = net.addCar('car%s' % (x), wlans=2, ip='10.0.0.%s/8' % (x + 1), \
        mac='00:00:00:00:00:0%s' % x, mode='b')

    
    eNodeB1 = net.addAccessPoint('eNodeB1', ssid='eNodeB1', dpid='1000000000000000', mode='ac', channel='1', position='80,75,0', range=60)
    eNodeB2 = net.addAccessPoint('eNodeB2', ssid='eNodeB2', dpid='2000000000000000', mode='ac', channel='6', position='180,75,0', range=70)
    rsu1 = net.addAccessPoint('rsu1', ssid='rsu1', dpid='3000000000000000', mode='g', channel='11', position='140,120,0', range=40)
    c1 = net.addController('c1', controller=Controller)
    client = net.addHost ('client')
    switch = net.addSwitch ('switch', dpid='4000000000000000')

    net.plotNode(client, position='125,230,0')
    net.plotNode(switch, position='125,200,0')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(eNodeB1, switch)
    net.addLink(eNodeB2, switch)
    net.addLink(rsu1, switch)
    net.addLink(switch, client)
    net.addLink(rsu1, car[0])
    net.addLink(eNodeB2, car[0])
    net.addLink(eNodeB1, car[3])

    print "*** Starting network"
    net.build()
    c1.start()
    eNodeB1.start([c1])
    eNodeB2.start([c1])
    rsu1.start([c1])
    switch.start([c1])

    for sw in net.vehicles:
        sw.start([c1])

    i = 1
    j = 2
    for c in car:
        c.cmd('ifconfig %s-wlan0 192.168.0.%s/24 up' % (c, i))
        c.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (c, i))
        c.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2

    i = 1
    j = 2
    for v in net.vehiclesSTA:
        v.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (v, j))
        v.cmd('ifconfig %s-mp0 10.0.0.%s/24 up' % (v, i))
        v.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        i += 1
        j += 2

    for v1 in net.vehiclesSTA:
        i = 1
        j = 1
        for v2 in net.vehiclesSTA:
            if v1 != v2:
                v1.cmd('route add -host 192.168.1.%s gw 10.0.0.%s' % (j, i))
            i += 1
            j += 2

    client.cmd('ifconfig client-eth0 200.0.10.2')
    net.vehiclesSTA[0].cmd('ifconfig car0STA-eth0 200.0.10.50')

    car[0].cmd('modprobe bonding mode=3')
    car[0].cmd('ip link add bond0 type bond')
    car[0].cmd('ip link set bond0 address 02:01:02:03:04:08')
    car[0].cmd('ip link set car0-eth0 down')
    car[0].cmd('ip link set car0-eth0 address 00:00:00:00:00:11')
    car[0].cmd('ip link set car0-eth0 master bond0')
    car[0].cmd('ip link set car0-wlan0 down')
    car[0].cmd('ip link set car0-wlan0 address 00:00:00:00:00:15')
    car[0].cmd('ip link set car0-wlan0 master bond0')
    car[0].cmd('ip link set car0-wlan1 down')
    car[0].cmd('ip link set car0-wlan1 address 00:00:00:00:00:13')
    car[0].cmd('ip link set car0-wlan1 master bond0')
    car[0].cmd('ip addr add 200.0.10.100/24 dev bond0')
    car[0].cmd('ip link set bond0 up')

	#connect through the other cars
    car[3].cmd('ifconfig car3-wlan0 200.0.10.150')

    client.cmd('ip route add 192.168.1.8 via 200.0.10.150')
    client.cmd('ip route add 10.0.0.1 via 200.0.10.150')

    net.vehiclesSTA[3].cmd('ip route add 200.0.10.2 via 192.168.1.7')
    net.vehiclesSTA[3].cmd('ip route add 200.0.10.100 via 10.0.0.1')
    net.vehiclesSTA[0].cmd('ip route add 200.0.10.2 via 10.0.0.4')

    car[0].cmd('ip route add 10.0.0.4 via 200.0.10.50')
    car[0].cmd('ip route add 192.168.1.7 via 200.0.10.50')
    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.50')
    car[3].cmd('ip route add 200.0.10.100 via 192.168.1.8')


    """plot graph"""
    net.plotGraph(max_x=250, max_y=250)

    net.startGraph()
	
    # Uncomment and modify the two commands below to stream video using VLC 
    # client(ip:200.0.10.2) is streaming and car0(ip:200.0.10.100) is the receiver
    car[0].cmdPrint("vlc -vvv bunnyMob.mp4 --sout '#duplicate{dst=rtp{dst=200.0.10.2,port=5004,mux=ts},dst=display}' :sout-keep &")
    client.cmdPrint("vlc rtp://@200.0.10.2:5004 &")

    car[0].moveNodeTo('95,100,0')
    car[1].moveNodeTo('80,100,0')
    car[2].moveNodeTo('65,100,0')
    car[3].moveNodeTo('50,100,0')
    
    time.sleep(2)
    
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    
    apply_experiment(car,client,switch)
   
    # Uncomment the line below to generate the graph that you implemented
	
    graphic1()	   #total packets transmited,throughtput (through ifconfig)
	
    graphic2()	   #packets dropped (through ifconfig)
    
    #graphic3()    #bandwidth (through iperf)
    
    #graphic4()    #jitter (through iperf)
    
    graphic5()    #latency (through ping)
	
    # kills all the xterms that have been opened
    os.system('pkill xterm')

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    try:
        topology()
    except:
        type = sys.exc_info()[0]
        error = sys.exc_info()[1]
        traceback = sys.exc_info()[2]
        print ("Type: %s" % type)
        print ("Error: %s" % error)
        print ("Traceback: %s" % traceback)
        if gnet != None:
            gnet.stop()
        else:
            print "No network was created..."
