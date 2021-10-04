import os
from Directory import mats_path, models_dict

def getpath(nested_dict, value, prepath=()):
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if v == value: # found value
            return path
        elif hasattr(v, 'items'): # v is a dict
            p = getpath(v, value, path) # recursive call
            if p is not None:
                return p


def import_mats(mats_path, models_dict):
    # note that you must change all ES_ to <part_name>_ for the materials to work if using mimics
    for file_ext in os.listdir(mats_path):
        file_extless = file_ext.split('.')[0]  # remove file extension

        # Find the model and access the dict name for the material trab
        dict_path = getpath(models_dict, file_extless) # note this will fail when imported name does not match the name of the file, ensurte imported files follow naming convention
        print(models_dict)
        print(file_extless)
        print(dict_path)
        try:
            trab_mat_name = models_dict[dict_path[0]]['trab_cut_mat']
        except:
            trab_mat_name = models_dict[dict_path[0]]['trab_mat']

        # Part within imported model will share the name of the model minus the 'MAT' ending and will be all caps
        mdb.ModelFromInputFile(name= trab_mat_name, inputFileName= mats_path+file_ext)

        # Changes the part name to match the model name
        mdb.models[trab_mat_name].parts.changeKey(
            fromName = mdb.models[trab_mat_name].parts.keys()[0], toName = trab_mat_name)



def transfer_mats(models_dict):
    for model_need_mat in models_dict:
        import part
        import material
        import section
        try:
            # Bring the cut trab with material pptys into the implant model
            trab_cut_mat = models_dict[model_need_mat]['trab_cut_mat']
            mdb.models[model_need_mat].Part(trab_cut_mat, 
                mdb.models[trab_cut_mat].parts[trab_cut_mat])
            mdb.models[model_need_mat].copyMaterials(
                sourceModel=mdb.models[trab_cut_mat])
            mdb.models[model_need_mat].copySections(
                sourceModel=mdb.models[trab_cut_mat])

            del mdb.models[trab_cut_mat]

            # Remove the trab without pptys
            del mdb.models[model_need_mat].parts[models_dict[model_need_mat]['trab_cut']]
            
        # Same thing but for intact instead of implant models
        except:
            trab_mat = models_dict[model_need_mat]['trab_mat']
            mdb.models[model_need_mat].Part(trab_mat, 
                mdb.models[trab_mat].parts[trab_mat])
            mdb.models[model_need_mat].copyMaterials(
                sourceModel=mdb.models[trab_mat])
            mdb.models[model_need_mat].copySections(
                sourceModel=mdb.models[trab_mat])
                
            del mdb.models[trab_mat]
            del mdb.models[model_need_mat].parts[models_dict[model_need_mat]['trab']]

def cort_mats(models_dict):
    for cort_need_mat in models_dict:
        import part
        import material
        import section

        cort = models_dict[cort_need_mat]['cort']

        mdb.models[cort_need_mat].Material(name='Cort')
        mdb.models[cort_need_mat].materials['Cort'].Elastic(table=((20000.0, 0.3), ))
        p = mdb.models[cort_need_mat].parts[cort]
        mdb.models[cort_need_mat].HomogeneousSolidSection(name='Cort', material='Cort', 
            thickness=None)
        
        region = p.sets[cort]
        p.SectionAssignment(region=region, sectionName='Cort', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)

def implants_mats(models_dict):
    for implant_need_mat in models_dict:
        import part
        import material
        import section

        implant = models_dict[implant_need_mat]['implant']

        mdb.models[implant_need_mat].Material(name='Ti')
        mdb.models[implant_need_mat].materials['Ti'].Elastic(table=((20000.0, 0.3), ))
        p = mdb.models[implant_need_mat].parts[implant]
        mdb.models[implant_need_mat].HomogeneousSolidSection(name='Implant', material='Cort', 
            thickness=None)
        
        region = p.sets[implant]
        p.SectionAssignment(region=region, sectionName='Implant', offset=0.0, 
            offsetType=MIDDLE_SURFACE, offsetField='', 
            thicknessAssignment=FROM_SECTION)
            


import_mats(mats_path, models_dict)
transfer_mats(models_dict)
cort_mats(models_dict)
