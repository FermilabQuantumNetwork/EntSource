#!/usr/bin/python2.7

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import pymysql
import os
import time

#figname = "plot_FQNETGUINov27png"

START_TIME = '2019-12-18 17:30:00'
END_TIME = '2019-12-19 05:00:00'

#START_TIME = '2019-12-11 12:14:00'
#END_TIME = '2019-12-11 14:47:54'

mpl.rcParams["savefig.directory"] = os.chdir(os.path.dirname("/home/inqnet1/Desktop/CQNET/EntSource"))


#Thermistor params
R0=10000
T0 = 25+273.15
beta = 3435
rInf = R0*math.exp(-beta/T0)
V0 = 2.5


#connect to database


T1 = []
time_T1 = []
P = []
time_P = []
Vap = []
time_Vap = []
Vin=[]
time_Vin = []
and1=[]
and2 = []
and3 = []
Ra2=[]
Rb2=[]
time_tab2=[]
time_histo=[]

T_Vap = []
T_Vin = []
try:
	db_tcom = pymysql.connect(host="192.168.0.125",  # this PC
						 user="inqnet1",
						 passwd="Teleport1536!",  # your password
						 db="teleportcommission",
						 charset='utf8mb4',
						 cursorclass=pymysql.cursors.DictCursor)
	with db_tcom.cursor() as cur:

		TABLE_NAME = "VapVin"
		queryVapVin = "SELECT Vap, Vin,datetimeVap,datetimeVin FROM "+TABLE_NAME+" WHERE datetimeVap BETWEEN {ts %s} AND {ts %s}"
		TABLE_NAME = "Temp"
		queryT1 = "SELECT T1, datetimeT1 FROM "+TABLE_NAME+" WHERE datetimeT1 BETWEEN {ts %s} AND {ts %s}"
		TABLE_NAME = "IM"
		queryP = "SELECT P, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"


		cur.execute(queryT1, (START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			T1.append(row["T1"])
			time_T1.append(row["datetimeT1"])
			row = cur.fetchone()

		cur.execute(queryP, (START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			P.append(10**(-3)*row["P"])
			time_P.append(row["datetime"])
			row = cur.fetchone()

		cur.execute(queryVapVin, (START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			Vap.append(row["Vap"])
			time_Vap.append(row["datetimeVap"])
			Vin.append(row["Vin"])
			time_Vin.append(row["datetimeVin"])
			row = cur.fetchone()
	db_tcom.close()




	db_gui = pymysql.connect(host="192.168.0.125",
						 user="inqnet1",
						 passwd="Teleport1536!",  # your password
						 db="INQNET_GUI",
						 charset='utf8mb4',
						 cursorclass=pymysql.cursors.DictCursor)
	with db_gui.cursor() as cur:
		TABLE_NAME = "inqnet_gui_tab2gates_V2"
		queryGUI = "SELECT and1, and2, and3, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"

		cur.execute(queryGUI, (START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			and1.append(row["and1"])
			and2.append(row["and2"])
			and3.append(row["and3"])
			time_tab2.append(row["datetime"])
			row = cur.fetchone()

		TABLE_NAME = "inqnet_gui_historates"
		queryGUI = "SELECT Ra2, Rb2, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			Ra2.append(row["Ra2"])
			Rb2.append(row["Rb2"])
			time_histo.append(row["datetime"])
			row = cur.fetchone()
	db_gui.close()


	time_T1_first = str(time_T1[0])
	print("time_T1_first=",time_T1_first )
	time_T1_last = str(time_T1[-1])
	first_time_T1 = datetime.datetime.strptime(time_T1_first,'%Y-%m-%d %H:%M:%S')
	time_T1_dt=[]
	time_T1_el_mins=[]

	time_P_first = str(time_P[0])
	print("time_P_first=",time_P_first )
	time_P_last = str(time_P[-1])
	first_time_P = datetime.datetime.strptime(time_P_first,'%Y-%m-%d %H:%M:%S')
	time_P_dt=[]
	time_P_el_mins=[]


	time_Vap_first = str(time_Vap[0])
	print("time_Vap_first=",time_Vap_first )
	time_Vap_last = str(time_Vap[-1])
	first_time_Vap = datetime.datetime.strptime(time_Vap_first,'%Y-%m-%d %H:%M:%S')
	time_Vap_dt = []
	time_Vap_el_mins = []

	time_Vin_first = str(time_Vin[0])
	print("time_Vin_first=",time_Vin_first )
	time_Vin_last = str(time_Vin[-1])

	first_time_Vin = datetime.datetime.strptime(time_Vin_first,'%Y-%m-%d %H:%M:%S')
	time_Vin_dt = []
	time_Vin_el_mins = []

	time_tab2_first = str(time_tab2[0])
	print("time_tab2_first=",time_tab2_first )
	time_tab2_last = str(time_tab2[-1])

	first_time_tab2 = datetime.datetime.strptime(time_tab2_first,'%Y-%m-%d %H:%M:%S')
	time_tab2_dt = []
	time_tab2_el_mins = []

	time_histo_first = str(time_histo[0])
	print("time_histo_first=",time_histo_first )
	time_histo_last = str(time_histo[-1])

	first_time_histo = datetime.datetime.strptime(time_histo_first,'%Y-%m-%d %H:%M:%S')
	time_histo_dt = []
	time_histo_el_mins = []


	for t in time_Vap:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime- first_time_Vap
		time_Vap_dt.append(datime)#.time)
		time_Vap_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
	for t in time_Vin:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime- first_time_Vin
		time_Vin_dt.append(datime)#.time)
		time_Vin_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
	for t in time_T1:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_T1
		time_T1_dt.append(datime)#.time)
		time_T1_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
	for t in time_P:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_P
		time_P_dt.append(datime)#.time)
		time_P_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
	for t in time_tab2:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_tab2
		time_tab2_dt.append(datime)#.time)
		time_tab2_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
	for t in time_histo:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_histo
		time_histo_dt.append(datime)#.time)
		time_histo_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes





	for i in range(len(Vap)):
		Rt_Vap = Vap[i]*R0/(V0-Vap[i])
		t = beta/(math.log(Rt_Vap/rInf))
		T_Vap.append(t-273.15)
		Rt_Vin = Vin[i]*R0/(V0-Vin[i])
		t = beta/(math.log(Rt_Vin/rInf))
		T_Vin.append(t-273.15)

	time_histo_el_mins=np.array(time_histo_el_mins)
	time_tab2_el_mins=np.array(time_tab2_el_mins)
	time_P_el_mins=np.array(time_P_el_mins)
	time_T1_el_mins=np.array(time_T1_el_mins)






	#Visib = (maxVis - minVis)/(maxVis + minVis)
	#sig = np.sqrt(maxVisStd**2 + minVisStd**2)
	#VisibStd = Visib*sig*np.sqrt((1/(maxVis-minVis))**2+(1/(maxVis+minVis))**2)
	#print("Visib ", Visib)
	#print("VisibStd ", VisibStd)






	#Stacked plot of all data

	fig, axs = plt.subplots(8,1, num=238, sharex = True)
	xmin=time_Vap_el_mins[0] #40
	xmax=time_Vap_el_mins[-1] #60
	tab2_indices = np.where(time_tab2_el_mins > time_Vap_el_mins[0])
	tab2_indices = tab2_indices[0]

	T_indices = np.where((time_T1_el_mins > time_Vap_el_mins[0]) &(time_T1_el_mins < time_Vap_el_mins[-1]))
	T_indices = T_indices[0]

	P_indices = np.where((time_P_el_mins > time_Vap_el_mins[0]) &(time_P_el_mins < time_Vap_el_mins[-1]))
	P_indices = P_indices[0]

	histo_indices = np.where(time_histo_el_mins > time_Vap_el_mins[0])
	histo_indices = histo_indices[0]


	#Vap
	axs[0].plot(time_Vap_el_mins, T_Vap,  linestyle = 'none', marker = '.', markersize = 2)
	axs[0].set_ylabel(r"$T_{set}$ ($\degree$C)")
	axs[0].grid()

	print(time_T1_el_mins[T_indices[0]:T_indices[-1]])
	#Temp
	axs[1].plot(time_T1_el_mins[T_indices[0]:T_indices[-1]], T1[T_indices[0]:T_indices[-1]],  linestyle = 'none', marker = '.', markersize = 2)
	axs[1].set_ylabel(r"T ($\degree C$)")
	axs[1].grid()


	print(time_P_el_mins[P_indices[0]:P_indices[-1]])
	#Power
	axs[2].plot(time_P_el_mins[P_indices[0]:P_indices[-1]], P[P_indices[0]:P_indices[-1]],  linestyle = 'none', marker = '.', markersize = 2)
	axs[2].set_ylim([5.3,5.6])
	axs[2].set_ylabel(r"IM Output P ($\mu$W)")
	axs[2].grid()


	print(time_tab2_el_mins[tab2_indices[0]:tab2_indices[-1]])

	#and1
	axs[3].plot(time_tab2_el_mins[tab2_indices[0]:tab2_indices[-1]], and1[tab2_indices[0]:tab2_indices[-1]],  linestyle = 'none', marker = '.', markersize = 8)
	axs[3].set_ylabel("and1")
	#axs[3].set_ylim(0,25)
	axs[3].grid()


	#and2
	axs[4].plot(time_tab2_el_mins[tab2_indices[0]:tab2_indices[-1]], and2[tab2_indices[0]:tab2_indices[-1]],  linestyle = 'none', marker = '.', markersize = 8)#, label = "Min Counts = {}".format(min(and2[tab2_indices[0]:tab2_indices[-1]]))+" , Max Counts = {}".format(max(and2[tab2_indices[0]:tab2_indices[-1]])))
	axs[4].set_ylabel("and2")
	#axs[4].legend()
	#axs[4].set_ylim(0,60)
	axs[4].grid()

	#and3
	axs[5].plot(time_tab2_el_mins[tab2_indices[0]:tab2_indices[-1]], and3[tab2_indices[0]:tab2_indices[-1]],  linestyle = 'none', marker = '.', markersize = 8)
	axs[5].set_ylabel("and3")
	#axs[5].set_ylim(0,25)
	axs[5].grid()


	print(time_histo_el_mins[histo_indices[0]:histo_indices[-1]])
	#Ra2
	axs[6].plot(time_histo_el_mins[histo_indices[0]:histo_indices[-1]], Ra2[histo_indices[0]:histo_indices[-1]],  linestyle = 'none', marker = '.', markersize = 8)
	axs[6].set_ylabel("Ra1")
	#axs[3].set_ylim(0,25)
	axs[6].grid()

	#Rb2
	axs[7].plot(time_histo_el_mins[histo_indices[0]:histo_indices[-1]], Rb2[histo_indices[0]:histo_indices[-1]],  linestyle = 'none', marker = '.', markersize = 8)#, label = "Min Counts = {}".format(min(and2[tab2_indices[0]:tab2_indices[-1]]))+" , Max Counts = {}".format(max(and2[tab2_indices[0]:tab2_indices[-1]])))
	axs[7].set_ylabel("Rb2")
	#axs[4].legend()
	#axs[4].set_ylim(0,60)
	axs[7].grid()

	axs[7].set_xlim(xmin, xmax)
	fig.suptitle("Coincidences from \n"+str(time_Vap[0]+datetime.timedelta(minutes=xmin))+" to "+str(time_Vap[0]+datetime.timedelta(minutes=xmax)))#+"\nVisibility = {:.3}".format(Visib)+", VisibErr = {:.3}".format(VisibStd))
	plt.xlabel('Elapsed time (min)', fontsize =16)
	#plt.savefig(figname)





	plt.show()

	print("")
	print("time_T1_last=",time_T1_last )
	print("time_P_last=",time_P_last )
	print("time_Vap_last=",time_Vap_last )
	print("time_Vin_last=",time_Vin_last )
	print("time_tab2_last=",time_tab2_last )
	print("time_histo_last=",time_histo_last )



except KeyboardInterrupt:
	print("Quit")
