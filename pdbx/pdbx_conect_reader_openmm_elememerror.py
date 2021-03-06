from __future__ import print_function
import gzip
import glob
import multiprocessing as mp
from simtk.openmm import *
from simtk.openmm.app import *
from simtk.unit import *
from ctypes import c_int

database_path = '/cbio/jclab/share/pdbx/*/*.cif.gz'
ppn = 32
metals = ['Ba',
 'Yb',
 'Eu',
 'Fe',
 'Dy',
 'V',
 'Ga',
 'Hg',
 'Pr',
 'Ni',
 'Pt',
 'Na',
 'Li',
 'Pb',
 'Re',
 'Tl',
 'Lu',
 'Ru',
 'Rb',
 'Te',
 'Tb',
 'K',
 'Zn',
 'Co',
 'Pd',
 'Ag',
 'Ca',
 'Ir',
 'Al',
 'Cd',
 'Gd',
 'Au',
 'Ce',
 'W',
 'In',
 'Cs',
 'Cr',
 'Cu',
 'Mg',
 'Sr',
 'Mo',
 'Mn',
 'Sm',
 'Os',
 'Ho',
 'Am',
 'La',
 'Sb',
 'Th',
 'As',
 'Be',
 'Rh']
pdblist_file = open('pdblist_element_error.txt')
pdblist = [line[:-1] for line in pdblist_file]

def file_reader(file):
    global progress_counter
    with lock:
        progress_counter.value += 1
    print(progress_counter.value)
    
    file_open = gzip.open(file)
    file_reader_results = []
    try:
        pdb = PDBxFile(file_open)
    except:
        return file_reader_results
    top = pdb.topology
    
    for atom in top.atoms():
        if atom.element == None:
            file_reader_results.append(atom.residue.name)
    
    return file_reader_results    
    
    
def database_analyzer(database_path):
    
    database_analyzer_results = []
    
    for file_reader_results in pool.map(file_reader, pdblist):
        database_analyzer_results.append(file_reader_results)
        
    return database_analyzer_results
        
if __name__ == "__main__":
    lock = mp.Lock()
    progress_counter = mp.Value(c_int)
    pool = mp.Pool(processes = ppn)
    database_analyzer_results = database_analyzer(database_path) 
    
    # write results
    with open('pdbx_conect_reader_openmm_results_elementerror2.txt', 'w') as f:
        f.write(str(database_analyzer_results))
                
    
