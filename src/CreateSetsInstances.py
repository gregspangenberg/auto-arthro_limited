import part
from Directory import model_import

def CreateSets(model_import):
    for key in mdb.models[model_import].parts.keys():
        p = mdb.models[model_import].parts[key]
        c = p.cells
        cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
        p.Set(cells=cells, name=key)
        print('Creating set for '+key)

def AssemblyCreateInstances(model_import):
    for key in mdb.models[model_import].parts.keys():
        a = mdb.models[model_import].rootAssembly
        a.DatumCsysByDefault(CARTESIAN)
        p = mdb.models[model_import].parts[key]
        a.Instance(name=key+'-1', part=p, dependent=ON)

AssemblyCreateInstances(model_import)
CreateSets(model_import)
