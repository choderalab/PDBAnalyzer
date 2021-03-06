from __future__ import print_function
import multiprocessing as mp
import glob
import mdtraj as md

pdbpath = '/Users/rafalpwiewiora/PDB/pdb/a*/*.ent.gz'
ppn = 6
#metal_name = 'ZN'

def loader(file):

    try:
        md.load_pdb(file)
    except:
        return None
            
    print(file)
    
    return None
    #try:
    #    traj = md.load_pdb(file)
    #except:    
#        print('ERROR: %s' % file)
    
def database_analyzer(pdbpath):
    
    pool.map(loader, glob.iglob(pdbpath))
    
if __name__ == '__main__':
    
    pool = mp.Pool(processes = ppn)        
    database_analyzer(pdbpath)
