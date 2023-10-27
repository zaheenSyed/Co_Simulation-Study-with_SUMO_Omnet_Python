## this script will run the sumo and record the result in text file

# actionStepLength="0.7" for hv
# actionStepLength="0.1" for CAV 

import os
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import glob
import os,sys
import pandas as pd
from operator import itemgetter
import shutil
import warnings
from datetime import datetime
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

dicfile_name="newmap_finalbaseline_exp_result.csv"
change_str="all params"
# roufiles=['acc25idm75.rou.xml','acc25krauss75.rou.xml','cacc25idm75.rou.xml','cacc25krauss75.rou.xml','cacc100.rou.xml', 'acc100.rou.xml','krauss100.rou.xml','idm100.rou.xml']
# roufiles=['krauss100.rou.xml']
# roufiles=['acc25krauss75.rou.xml','acc50krauss50.rou.xml','acc75krauss25.rou.xml','acc100.rou.xml','cacc25krauss75.rou.xml','cacc50krauss50.rou.xml','cacc75krauss25.rou.xml','cacc100.rou.xml','krauss100.rou.xml']
roufiles=['krauss100.rou.xml','acc25krauss75.rou.xml','acc50krauss50.rou.xml','acc75krauss25.rou.xml','acc100.rou.xml','cacc25krauss75.rou.xml','cacc50krauss50.rou.xml','cacc75krauss25.rou.xml','cacc100.rou.xml']

for run in roufiles:
    for loopers in range(5):
        ssm=[] # list surrogate safety measure  
        total_TT=[] # empty list to find the total Travel time
        stp_lngth=0.1
        cmd="sumo.exe -c I75_FInal.sumocfg -r "+run+" --step-length "+str(stp_lngth)+" --no-warnings"
        print(cmd)
        os.system(cmd)

        today = datetime.now()
        dt_string = today.strftime("%d-%m-%Y %H-%M-%S")
        dt_string2=today.strftime("%d%m%Y%H%M%S")
        mname=run[:-8]
        dpath=dt_string2+"_"+mname+"\\"
        print(dpath)

        try:
            os.mkdir(os.path.join(os.getcwd(),dpath))
        except:
            pass

        dst = os.path.join(os.getcwd(),dpath)
        
        input_files1 = r"ssm_k.xml"
        input_files2 = r"ssm_a.xml"
        input_files3 = r"ssm_c.xml"


        input_files4 = r"traveltime.xml" 
        input_files5 =  r"loop.xml" 

        input_files6=r"fcd.xml"
        input_files7=r"stat.xml"


        for i in range(1,8):
                myfile=eval('input_files%d'% (i))

                if os.path.isfile(myfile): 
                    cmd1 = "python xml2csv.py " + myfile
                    os.system(cmd1)

        ssm_dict={'krauss':0,'acc':0,'cacc':0}
        drac_dict={'krauss':0,'acc':0,'cacc':0}
        out_files1 = r"ssm_k.csv"
        out_files2 = r"ssm_a.csv"
        out_files3 = r"ssm_c.csv"

        ## TTC and DRAC operation

        for i in range(1,4):
                    
            ssm_file=eval('out_files%d'% (i))
            

            if not os.path.isfile(ssm_file):
                continue

            print(ssm_file)
            df1=pd.read_csv(ssm_file, sep=';',)
            df1=df1[(df1['conflict_begin']>=1800.0) & (df1['conflict_begin']<5400.0 )]
            
            df1=df1.fillna(-1)
            df_ttc=df1[df1['minTTC_value']>=0]
            df_ttc=df_ttc[df_ttc["minTTC_type"]==2]
            df_ttc_crash=df1[(df1['minTTC_value']>=0) & (df1['minTTC_value']<=1.5)]
            df_ttc_crash=df_ttc_crash[df_ttc_crash["minTTC_type"]==2]

            ## ploting
            fig, ax4=plt.subplots(figsize=(6,4))
            n, bins, patches = ax4.hist(df_ttc['minTTC_value'],40,density=False, facecolor='y', alpha=0.75)
            #ax4.hist(df_ttc['minTTC_value'])
            ax4.set_xlabel('Time to Collision',size='14')
            ax4.set_ylabel('Frequency',size='14')
            ax4.set_title('Distribution for TTC Value'+ssm_file,size='14')
            ax4.axvline(x=1.5)
            #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
            #ax4.axis([0.62,3.1,0,250])
            ax4.grid(True)
            plt.tight_layout()
            # plt.show()
            figname=ssm_file+'_ttc.png'
            fig.savefig(figname,dpi=500)
            shutil.move(figname,dst)
            plt.close()
            ## plotting the drac
            
            df_drac=df1[(df1['maxDRAC_value']>=0)]
            df_drac=df_drac[df_drac['maxDRAC_type']==2]
            df_drac_crash=df1[(df1['maxDRAC_value']>=3.30)]
            df_drac_crash=df_drac_crash[df_drac_crash['maxDRAC_type']==2]
            
            fig5, ax5=plt.subplots(figsize=(6,4))
            #ax5.hist(df_drac['maxDRAC_value'])

            n, bins, patches = ax5.hist(df_drac['maxDRAC_value'],40,density=False, facecolor='y', alpha=0.75)

            ax5.set_xlabel('Maximum DRAC Value',size='14')
            ax5.set_ylabel('Frequency',size='14')
            ax5.set_title('Distribution for Maximum DRAC '+ssm_file,size='14')
            ax5.axvline(x=3.5)
            #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
            #ax5.axis([0.5,3.0,0,90])
            ax5.grid(True)
            plt.tight_layout()
            # plt.show()
            figname=ssm_file+'_drac.png'
            fig5.savefig(figname,dpi=500)
            plt.close()

            shutil.move(figname,dst)
            df_drac_crash=df1[(df1['maxDRAC_value']>=3.30)]
            
            if i==1 and os.path.isfile(ssm_file):
                ssm_dict['krauss']=len(df_ttc_crash)
                drac_dict['krauss']=len(df_drac_crash)
                
            if i==2 and os.path.isfile(ssm_file):
                df_ttc_crash=df1[(df1['minTTC_value']>=0) & (df1['minTTC_value']<=0.75)]
                df_ttc_crash=df_ttc_crash[df_ttc_crash["minTTC_type"]==2]

                ssm_dict['acc']=len(df_ttc_crash)
                drac_dict['acc']=len(df_drac_crash)
            if i==3 and os.path.isfile(ssm_file):
                df_ttc_crash=df1[(df1['minTTC_value']>=0) & (df1['minTTC_value']<=0.5)]
                df_ttc_crash=df_ttc_crash[df_ttc_crash["minTTC_type"]==2]
                
                ssm_dict['cacc']=len(df_ttc_crash)
                drac_dict['cacc']=len(df_drac_crash)
            if os.path.isfile(ssm_file):
                # ssmp=r'./'+ssm_file
                os.remove(ssm_file)
        
        infile_tt=r'traveltime.csv'

        df_tt=pd.read_csv(infile_tt, sep=';')
        df_tt['traveltime']=df_tt['edge_traveltime']/60
        df_tt['begin']=df_tt['interval_begin']/60

        time_interval=df_tt['begin'].unique()

        # edge_list=['L23_L2','L2_L1','L3_L23','L4_L3','L4_LS4','L5_L4','L6_L5','LS3_L3','LS4_LS41s','R1_R2','R2_R3','R3_R4','R4_R5','R4_RS4','R5_R6','R6_R7','R7_R8','RS5_R5']
        edge_list=["1to2","2to3","3to4","4to5","5to6","6to7","7to8","8to9","9to10","10to11","11to12","12to13"]


        travel_time=pd.DataFrame(np.transpose([time_interval]),columns=['time_interval'])
        travel_time['total']=0.0

        for j in edge_list:
            tt=df_tt[(df_tt['edge_id']==j)]
            tt=tt.reset_index()
            # print(tt['edge_traveltime'])
            travel_time[str(j)]=tt['traveltime']
            travel_time['total']= travel_time['total']+travel_time[str(j)]
            total_TT.append(travel_time['total'].values)


        tt_str=str(np.mean(total_TT))
        std_tt_str=str(np.std(total_TT))
        
        ## Finding the flow:

        df_tt['traveltime']=df_tt['edge_traveltime']/60
        df_tt['begin']=df_tt['interval_begin']/60
        df_tt['end']=df_tt['interval_end']/60
        df_tt['period']=df_tt['interval_end']-df_tt['interval_begin']
        df_tt['avg_veh']=df_tt['edge_sampledSeconds']/df_tt['period']
        # Average traffic volume (#/h) = speed * 3.6 * density
        df_tt['tf_vol']=(df_tt['edge_speed']*3.6)*df_tt['edge_density']

        total_tf_vol=[]

        time_interval=df_tt['begin'].unique()

        # edge_list=['L23_L2','L2_L1','L3_L23','L4_L3','L4_LS4','L5_L4','L6_L5','LS3_L3','LS4_LS41s','R1_R2','R2_R3','R3_R4','R4_R5','R4_RS4','R5_R6','R6_R7','R7_R8','RS5_R5']
        edge_list=["1to2","2to3","3to4","4to5","5to6","6to7","7to8","8to9","9to10","10to11","11to12","12to13"]


        df_flow=pd.DataFrame(np.transpose([time_interval]),columns=['time_interval'])
        df_flow['total']=0.0

        for j in edge_list:
            tt=df_tt[(df_tt['edge_id']==j)]
            tt=tt.reset_index()
            # print(tt['edge_traveltime'])
            df_flow[str(j)]=tt['tf_vol']
            df_flow['total']= df_flow['total']+df_flow[str(j)]
            total_tf_vol.append(df_flow['total'].values)

        df_flow['total']= df_flow['total']/12

        traffic_flow_mean=np.mean(total_tf_vol)

        traffic_flow_std=(np.std(total_tf_vol))



        #Reading Loop  Data

        infile_loop=r"loop.csv"

        df_loop=pd.read_csv(infile_loop, sep=";",usecols=['interval_id','interval_begin','interval_flow','interval_speed'])

        df_loop=df_loop.sort_values(['interval_id'])

        loop_id=pd.unique(df_loop['interval_id'])

        loop_det=[]

        df_sort=pd.DataFrame()

        for i in range (len(df_loop)):
            interval_id=df_loop['interval_id'][i].split('_')
            loop_no=interval_id[0]
            lane_no=interval_id[1]
            #print(loop_no)
            loop_det.append([loop_no,lane_no])
            #lane_no.append(int(lane_no))

        det=pd.DataFrame(loop_det,columns=['loop_det','lane_no'])   
        df_loop['loop_det']=det['loop_det']
        df_loop['lane_no']=det['lane_no']
        df_loop=df_loop.sort_values(['loop_det','interval_begin'])

        flow=df_loop.filter(['interval_begin','loop_det','interval_flow'])

        grp_flow=flow.groupby(['interval_begin','loop_det']).sum()
        #df_loop=df_loop.sort_values(['interval_begin'])
        grp_flow=grp_flow.reset_index()
        grp_flow=grp_flow.sort_values(['loop_det'])

        speed=df_loop.filter(['interval_begin','loop_det','interval_speed'])

        grp_speed=speed.groupby(['interval_begin','loop_det']).mean()
        #df_loop=df_loop.sort_values(['interval_begin'])
        grp_speed=grp_speed.reset_index()

        grp_speed=grp_speed.sort_values(['loop_det','interval_begin'])

        df_sim=pd.merge(grp_flow, grp_speed, on=['loop_det','interval_begin'])
        df_sim=df_sim.sort_values(['loop_det','interval_begin'])


        #df_field=df_field.set_index(['interval_begin'],drop=True)
        df_sim=df_sim[(df_sim['interval_begin']>=1800) & (df_sim['interval_begin']<5400)]

        df_sim=df_sim.reset_index(drop=True)
        df_sim_1=df_sim.groupby('loop_det').mean()


        ## Recording
        

        dict1={}
        dict1['modelname']=run
        dict1['date_exp']=dt_string
        dict1['stp_lngth']=stp_lngth
        dict1['drac_cnt_LV']=drac_dict['krauss']
        dict1['drac_cnt_ACC']=drac_dict['acc']
        dict1['drac_cnt_CACC']=drac_dict['cacc']

        dict1['ttc_cnt_LV']=ssm_dict['krauss']
        dict1['ttc_cnt_ACC']=ssm_dict['acc']
        dict1['ttc_cnt_CACC']=ssm_dict['cacc']

        dict1['total_ttc']=ssm_dict['krauss']+ssm_dict['acc']+ssm_dict['cacc']

        dict1['tt_str']=tt_str
        dict1['std_tt_str']=std_tt_str
        dict1['traffic_flow_mean']=traffic_flow_mean
        dict1['traffic_flow_std']=traffic_flow_std

        dict1['reaction']=0.1
        dict1['tau']='1.3 1.2'

        dict1['loop DF']=df_sim_1
        dict1['exp']=change_str

        from csv import DictWriter

        dicfile=dicfile_name
        if os.path.isfile(dicfile):
            pass
        else:
            df_a = pd.DataFrame([dict1], columns=dict1.keys())
            df_a=df_a.set_index('modelname')
            df_a.to_csv(dicfile)


        field_names=list(dict1.keys())

        with open(dicfile, 'a') as f_object:

            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(dict1)
            f_object.close()

        try:

            df1.to_csv('ssmdata.csv')
            shutil.copy('ssmdata.csv',dst)
            os.remove('ssmdata.csv')

            travel_time.to_csv('tt.csv')
            shutil.copy('tt.csv',dst)
            os.remove('tt.csv')


            df_flow.to_csv('flow.csv')
            shutil.copy('flow.csv',dst)
            os.remove('flow.csv')

            df_sim_1.to_csv('loop_group.csv')
            shutil.move('loop_group.csv',dst)
            os.remove('loop_group.csv')

        except:
            pass

        try:
            os.remove(infile_loop)
        except:
            pass
        try:    
            os.remove(infile_tt)
        except:
            pass

        for i in range(1,8):
            myfile=eval('input_files%d'% (i))
            print(myfile)

            if os.path.isfile(myfile): 
                shutil.copy(myfile,dst)
                os.remove(myfile)
                print('removed')
            else:
                print('nononono')

        plt.close()
        

