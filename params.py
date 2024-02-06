
# Machines list

machine_list=['adastra','jean-zay','irene']

# Directories on each machine

script_path={}
script_path['adastra']='/lus/home/CT1/ige2071/aalbert/git/extractions-MEOM'

nco_path={}
nco_path['adastra']='/lus/home/CT1/ige2071/aalbert/.conda/envs/nco/bin'

scratch_path={}
scratch_path['adastra']='/lus/scratch/CT1/hmg2840/aalbert/TMPEXTRACT'

store_path={}
store_path['adastra']='/lus/store/CT1/hmg2840/aalbert/'

# All the configurations available on each machine

configuration_list={}
configuration_list['adastra']=['CALEDO60']

# All the simulations run with each configuration on each machine

simulation_list={}
simulation_list['adastra']={}
simulation_list['adastra']['CALEDO60']=['TRPC12NT0','TRPC12N00']

# Where to find the -S directory for a given simulation of a configuration on a machine and how it is organized

directory={}
directory['adastra']={}
directory['adastra']['CALEDO60']={}
directory['adastra']['CALEDO60']['TRPC12NT0']='/lus/store/CT1/ige2071/brodeau/TROPICO12/TROPICO12_NST-TRPC12NT0-S'

stylenom={}
stylenom['adastra']={}
stylenom['adastra']['CALEDO60']={}
stylenom['adastra']['CALEDO60']['TRPC12NT0']='brodeau_nst'

# All the regions we can extract in a configuration and the associated parameters

regions_list={}
regions_list['CALEDO60']=['CALEDO60']

xy={}
xy['CALEDO60']={}
xy['CALEDO60']['CALEDO60']=''

ex={}
ex['CALEDO60']={}
ex['CALEDO60']['CALEDO60']=''

# All the variables we can extract and the associated name and filetyp for each simulations

variable_list=['SSH','SSU','SSV','T','S','U','V','W','TAUM','TAUBOT','QTOCE','QSROCE','QSBOCE','QNSOCE','QLWOCE','QLAOCE','PRECIP','EVAPOCE','EMPMR','WINDSP','RHOAIR','MLD','SBU','TAUUO','SBV','TAUVO']

vars_name={}
vars_name['TRPC12NT0']={'SSH':'zos','SSU':'uos','SSV':'vos'}
vars_name['TRPC12N00']={'SSH':'zos','SSU':'uos','SSV':'vos'}

filetyp={}
filetyp['TRPC12NT0']={'SSH':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D'}
filetyp['TRPC12N00']={'SSH':'gridT-2D','SSU':'gridU-2D','SSV':'gridV-2D'}

vars_dim={'SSH':'2D','SSU':'2D','SSV':'2D','T':'3D','S':'3D','U':'3D','V':'3D','W':'3D','TAUM':'2D','TAUBOT':'2D','QTOCE':'2D','QSROCE':'2D','QSBOCE':'2D','QNSOCE':'2D','QLWOCE':'2D','QLAOCE':'2D','PRECIP':'2D','EVAPOCE':'2D','EMPMR':'2D','WINDSP':'2D','RHOAIR':'2D','MLD':'2D','SBU':'2D','TAUUO':'2D','SBV':'2D','TAUVO':'2D'}
# The time frequency available for a given variable and simulation

frequencies={}
frequencies['TRPC12NT0']={'SSH':'1h','SSU':'1h','SSV':'1h'}
frequencies['TRPC12N00']={'SSH':'1h','SSU':'1h','SSV':'1h'}

# The period of time covered by a simulation

sim_date_init={'TRPC12NT0':'2012-01-01'}
sim_date_end={'TRPC12NT0':'2018-12-31'}


