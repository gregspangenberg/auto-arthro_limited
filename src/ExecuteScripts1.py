from Directory import sample,root_path,working_directory_path

#Initial Code generated upon startup
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
Mdb()


#############################################################
#################     Execute Scripts      ##################
execfile(root_path +'\\src\\ImportParts.py', __main__.__dict__)
execfile(root_path +'\\src\\CreateSetsInstances.py', __main__.__dict__)
execfile(root_path +'\\src\\AssemblyCut.py', __main__.__dict__)
execfile(root_path +'\\src\\Combine.py', __main__.__dict__)
execfile(root_path +'\\src\\Mesh.py', __main__.__dict__)
execfile(root_path +'\\src\\MeshWash.py', __main__.__dict__)

mdb.saveAs(pathName=working_directory_path + sample)
