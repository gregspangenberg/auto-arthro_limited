#Copyright 2020, Gregory Spangeberg, All rights reserved.
import sys
from Directory import root_path


#Initial Code generated upon startup
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

#Open Database
'''
When opening the database you need to declare what the mdb variable is 
if you just do openMdb(cae_path) then it wont be able to save the 
updated database
'''

cae_path = sys.argv[-3]
mdb = openMdb(cae_path)

#############################################################
#################     Execute Scripts      ##################
execfile(root_path + '\\src\\ImportMATS.py', __main__.__dict__)
execfile(root_path + '\\src\\combineMATS.py', __main__.__dict__)

# mdb.save()