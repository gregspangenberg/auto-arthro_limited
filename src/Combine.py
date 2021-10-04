## the intact model is being named INTACT011L instead of INTACT_011L

from Directory import  models_dict, model_comb, model_import, intact


def Combine(models_dict, model_comb, model_import, intact):
    mdb.Model(name = model_comb, modelType=STANDARD_EXPLICIT)

    for combined_part_name in models_dict:    

        if combined_part_name.startswith(intact):
            #Combine the Intact Trab and cort
            a = mdb.models[model_import].rootAssembly
            cort = models_dict[combined_part_name]['cort']
            trab = models_dict[combined_part_name]['trab']

            a.features[cort + '-1'].resume()
            a.features[trab + '-1'].resume()

            a.InstanceFromBooleanMerge(name = combined_part_name, instances=(
                a.instances[cort + '-1'], a.instances[trab + '-1'], ), 
                keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY)

            mdb.models[model_comb].Part(combined_part_name, mdb.models[model_import].parts[combined_part_name])
            print(cort +' and '+ trab +' have been merged and placed in combined')

        else:
            # Combine the implant, trab_cut, and cort 
            a = mdb.models[model_import].rootAssembly
            cort = models_dict[combined_part_name]['cort']
            trab = models_dict[combined_part_name]['trab_cut']
            implant = models_dict[combined_part_name]['implant']

            a.features[trab + '-1'].resume()
            a.features[cort + '-1'].resume()
            a.features[implant + '-1'].resume()

            a.InstanceFromBooleanMerge(name = combined_part_name, instances=(
                a.instances[cort+'-1'], a.instances[trab +'-1'], a.instances[implant +'-1'] ), 
                keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY)

            mdb.models[model_comb].Part(combined_part_name, mdb.models[model_import].parts[combined_part_name])
            print(cort +', '+ trab +' ,and '+ implant +' have been merged and placed in combined')
        

Combine(models_dict, model_comb, model_import, intact)




