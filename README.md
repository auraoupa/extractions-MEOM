# All the tools to perform extractions

MEOM produces simulations on super-computers and would like to share some of the outputs to people outside.

Data can be sitting on several machines :
  - adastra at CINES
  - jean-zay at IDRIS
  - irene at TGCC

Here are the steps to easily extract a dataset on any machine :
 - You need to define the dataset you want to extract by copying and modifying the [template](dataset_definition_template.py) by selecting parameters already defined in [this file](params.py)
 - The advanced users can modify the [param](params.py) to specify a new simulation that has been run and stored on a machine for instance
 - If not already done, install the proper [conda environment](env.yml) and activate it 
 - Then you launch the script that will generate and launch the scripts or jobs that will perform the extractions
	- on adastra, the store is not accessible via login nodes so raw extractions are to be done on the frontal nodes and not in parallel, therefore a single script can launch the extractions, check the extractions after they are done and save the output to the store : ```./run_extraction_adastra.ksh CALEDO60-SSH-SSU-SSV-1h-2014```


Different type of files can be found here :
  - some python scripts gather parameters (params.py) and functions (functions.py) and are called in bigger python scripts (launch/check/save_dataset_extractions.py)
  - the big python scripts are generating some bash scripts from template (script*ksh) that can be launched inside a job or in a bigger script
