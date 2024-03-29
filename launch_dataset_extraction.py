#! /usr/bin/env python

import sys,getopt,os
import argparse
import pandas as pd
import shutil
import subprocess
import params
import functions as f

def parse_args():
    parser=argparse.ArgumentParser(description="check dataset definition and generate the associated job")
    parser.add_argument('-dataset',type=str,help='dataset param')
    args=parser.parse_args()
    return args

def check(machine,configuration,simulations,regions,variables,frequency,date_init,date_end):
    #All the checks

    f.check(machine,params.machine_list,'The machine '+str(machine)+' does not exist yet')
    f.check(configuration,params.configuration_list[machine],'The configuration '+str(configuration)+' is not stored on the machine '+str(machine))
       
    for sim in simulations:
        f.check(sim,params.simulation_list[machine][configuration],'The simulation '+str(sim)+' for the configuration '+str(configuration)+' is not stored on the machine '+str(machine))

    for reg in regions:
        f.check(reg,params.regions_list[configuration],'The region '+str(reg)+' is not defined for the configuration '+str(configuration))

    for var in variables:
        f.check(var,params.variable_list,'The variable '+str(var)+' is not defined')

    for sim in simulations:
        for var in variables:
            f.check(frequency,params.frequencies[sim][var],'The variable '+str(var)+' for the simulation '+str(sim)+' does not have the frequency '+str(frequency))

    for sim in simulations:
        if pd.Timestamp(date_init) < pd.Timestamp(params.sim_date_init[sim]):
            sys.exit('The initial date '+str(date_init)+' is not included the period of output of the simulation '+str(sim))
        if pd.Timestamp(date_end) > pd.Timestamp(params.sim_date_end[sim]):
            sys.exit('The end date '+str(date_end)+' is not included the period of output of the simulation '+str(sim))

    print('All checks have passed, we are now going to generate and launch a job that will extract '+str(variables)+' from simulations '+str(simulations)+' from configuration '+str(configuration)+' from '+str(date_init)+' to '+str(date_end)+' at '+str(frequency)+' frequency on machine '+str(machine))


def job(machine,configuration,simulations,regions,variables,frequency,date_init,date_end):
    #Concatenate the name of all simulations, regions, variables
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allregions=f.concatenate_all_names_in_list(regions)
    allvariables=f.concatenate_all_names_in_list(variables)
    mpmdname='mpmd_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.conf'
    jobname='tmp_job_extract_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
    
    #Check if variables are 2D or 3D and parallelize accordingly (monthly or daily)
    freqex={}
    scr_list={}
    nb_procs=0
    pos=[]
    all_dates=pd.date_range(date_init,date_end,freq='D')
    for var in variables:
        if params.vars_dim[var]=='2D':
            freqex[var]='1m'
            print('We are going to extract variable '+str(var)+' in parallel by month')
            all_month=pd.date_range(date_init,date_end,freq='M')
            for ym in all_month:
                year=ym.year
                month=ym.month
                mm="{:02d}".format(month)
                tag=str(year)+'-'+str(mm)
                for simulation in simulations:
                    for region in regions:
                        scriptname=('tmp_script_extract_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')
                        shutil.copyfile('script_extract_'+str(machine)+'_2Dvar_1month_template.ksh',scriptname)
                        subprocess.call(["sed", "-i", "-e",  's/CONFIGURATION/'+str(configuration)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/SIMULATION/'+str(simulation)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/REGIONNAME/'+str(region)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/REGIONABR/'+str(params.ex[configuration][region])+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/VARIABLE/'+str(var)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/VNAME/'+str(params.vars_name[simulation][var])+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/FREQUENCY/'+str(frequency)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/YEAR/'+str(year)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/MONTH/'+str(mm)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/FILETYP/'+str(params.filetyp[simulation][var])+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's%SOURCEDIR%'+str(params.directory[machine][configuration][simulation])+'%g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/STYLENOM/'+str(params.stylenom[machine][configuration][simulation])+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/XTRACTINDICES/'+str(params.xy[configuration][region])+'/g', scriptname])
                        subprocess.call(["chmod", "+x", scriptname])
                        
                        with open(mpmdname, 'a') as file:
                            file.write("{}\n".format(str(nb_procs)+' ./'+str(scriptname)))
                        
                        nb_procs=nb_procs+1

        else:
            freqex[var]='1d'
            print('We are going to extract variable '+str(var)+' in parallel by day')

    if nb_procs < 127:
        print('We are going to launch one job')


        #Copy the template job for the given machine and name the job according to the specs
        jobname='tmp_job_extract_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
        shutil.copyfile('job_'+str(machine)+'_template.ksh',jobname)
        subprocess.call(["sed", "-i", "-e",  's/NPROCS/'+str(nb_procs)+'/g', jobname])
        subprocess.call(["sed", "-i", "-e",  's/MPMDCONF/'+str(mpmdname)+'/g', jobname])
        subprocess.call(["sbatch",jobname])

def make(machine,configuration,simulations,regions,variables,frequency,date_init,date_end):
    #Concatenate the name of all simulations, regions, variables
    allsimulations=f.concatenate_all_names_in_list(simulations)
    allregions=f.concatenate_all_names_in_list(regions)
    allvariables=f.concatenate_all_names_in_list(variables)
    mpmdname='tmp_make_extract_'+str(machine)+'_'+str(configuration)+'_'+str(allsimulations)+'_'+str(allregions)+'_'+str(allvariables)+'_'+str(frequency)+'_'+str(date_init)+'_'+str(date_end)+'.ksh'
    
    #Check if variables are 2D or 3D and parallelize accordingly (monthly or daily)
    scr_list={}
    nb_procs=0
    pos=[]
    all_dates=pd.date_range(date_init,date_end,freq='D')
    for var in variables:
        if params.vars_dim[var]=='2D':
            print('We are going to extract variable '+str(var)+' in parallel by month')
            all_month=pd.date_range(date_init,date_end,freq='M')
            for ym in all_month:
                year=ym.year
                month=ym.month
                mm="{:02d}".format(month)
                tag=str(year)+'-'+str(mm)
                for simulation in simulations:
                    for region in regions:
                        scriptname=('tmp_script_extract_'+str(machine)+'_'+str(configuration)+'_'+str(simulation)+'_'+str(region)+'_'+str(var)+'_'+str(frequency)+'_'+str(tag)+'.ksh')
                        shutil.copyfile('script_extract_2Dvar_1month_template.ksh',scriptname)
                        subprocess.call(["sed", "-i", "-e",  's/CONFIGURATION/'+str(configuration)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/SIMULATION/'+str(simulation)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/REGIONNAME/'+str(region)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/REGIONABR/'+str(params.ex[configuration][region])+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/VARIABLE/'+str(var)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/VNAME/'+str(params.vars_name[simulation][var])+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/FREQUENCY/'+str(frequency)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/YEAR/'+str(year)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/MONTH/'+str(mm)+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/FILETYP/'+str(params.filetyp[simulation][var])+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's%SOURCEDIR%'+str(params.directory[machine][configuration][simulation])+'%g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/STYLENOM/'+str(params.stylenom[machine][configuration][simulation])+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's/XTRACTINDICES/'+str(params.xy[configuration][region])+'/g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's%SCPATH%'+str(params.scratch_path[machine])+'%g', scriptname])
                        subprocess.call(["sed", "-i", "-e",  's%NCOPATH%'+str(params.nco_path[machine])+'%g', scriptname])
                        subprocess.call(["chmod", "+x", scriptname])
                        
                        with open(mpmdname, 'a') as file:
                            file.write("{}\n".format(' ./'+str(scriptname)))
                        
                        nb_procs=nb_procs+1

    print('We are going to run the extraction scripts on the frontal node')
    subprocess.call(["chmod", "+x", mpmdname])
    subprocess.run(params.script_path[machine]+'/'+mpmdname,shell=True)



def main():
    param_dataset = parse_args().dataset
    da = __import__(param_dataset)
    print('Extractions for '+str(param_dataset)+' are launched')
    check(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end)
#    job(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end)
    make(da.machine,da.configuration,da.simulations,da.regions,da.variables,da.frequency,da.date_init,da.date_end)

if __name__ == "__main__":
    main()

