from Directory import model_import, models_dict

#Cuts the trab with each implant
def assembly_cut(model_import, models_dict):
    for model_to_cut in models_dict:
        try:
            trab_cut = models_dict[model_to_cut]['trab_cut']
            trab = models_dict[model_to_cut]['trab']
            implant = models_dict[model_to_cut]['implant']
            a = mdb.models[model_import].rootAssembly
            a.features[trab + '-1'].resume()
            a.InstanceFromBooleanCut(name = trab_cut, 
                instanceToBeCut=mdb.models[model_import].rootAssembly.instances[trab+'-1'], 
                cuttingInstances=(a.instances[implant + '-1'], ),
                originalInstances=SUPPRESS)
            mdb.models[model_import].parts[trab_cut].sets.changeKey(
                fromName = trab, toName = trab_cut)
            print(implant +' has cut '+ trab)
        except:
            continue


assembly_cut(model_import, models_dict)