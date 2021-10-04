#Importing necessary Python modules
'''
Bone files must be .SLDPRT files and implants must be .STEP files.
This is becaue importing bone as .STEP makes creating a set difficult as you
must select every single face on the part.
Oddly the same is not true for the implant files, and when tryin to import
implant files as .SLDPRT errors that the file is corrupted often appear.
I don't know why this is.
'''

from Directory import file_path_dict, var_list, model_import, models_dict

#Imports all Solidworks partmat and Step files in folder
def part_import(file_path_dict, var_list, model_import, models_dict):
    for var in var_list:
        try:
            sldprt = mdb.openSolidworks(fileName=file_path_dict.get(var), topology=SOLID)
            mdb.models[model_import].PartFromGeometryFile(name = var, 
                geometryFile=sldprt, combine=False, stitchTolerance=1.0, 
                dimensionality=THREE_D, type=DEFORMABLE_BODY, convertToAnalytical=1, 
                stitchEdges=1)
            print('Importing file from '+file_path_dict.get(var))
        except:
            step = mdb.openStep(file_path_dict.get(var), scaleFromFile=OFF)
            mdb.models[model_import].PartFromGeometryFile(name = models_dict[var]['implant'], 
                geometryFile=step, combine=False, dimensionality=THREE_D, type=DEFORMABLE_BODY)
            print('Importing file from '+file_path_dict.get(var))


mdb.Model(name=model_import, modelType=STANDARD_EXPLICIT)

part_import(file_path_dict, var_list, model_import, models_dict)
del mdb.models['Model-1']

