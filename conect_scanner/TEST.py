def ligand_scanner(file):
    
    ok_file_count, error_file_count, metal_count, files_with_metal_count = 0 
    extra_in_cutoff_count_by_atom, extra_in_CONECT_count_by_atom, both_extra_CONECT_higher_count_by_atom = 0
    both_extra_cutoff_higher_count_by_atom, both_extra_both_equal_by_atom, extra_in_cutoff_count_by_file = 0
    extra_in_CONECT_count_by_file, both_extra_count_by_file, both_equal_count_by_atom, both_equal_count_by_file = 0
    
    metal_ligand_dict_by_cutoff = {}
    metal_ligand_dict_by_CONECT = {}
    metal_ligand_dict_in_cutoff_not_CONECT = {}
    metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT = {}
    metal_ligand_dict_in_CONECT_not_cutoff = {}
    extra_in_cutoff_for_file_analyzed = False
    extra_in_CONECT_for_file_analyzed = False
    both_extra_for_file_analyzed = False
    both_equal_for_file_analyzed = False
    
    try:
        traj = md.load_pdb(file)
        with lock:
            ok_file_count += 1
    except:
        with lock:
            error_file_count += 1
        return None

    
    # Select atoms and pairs
    topo = traj.topology
    metal_select_name = 'name %s' % metal_name
    metal_atoms = topo.select(metal_select_name)
    metal_all_pairs = topo.select_pairs(metal_select_name, 'all')
    
    # No metal - skip, metal - add to count 
    if not metal_atoms.size:
        return None
    
    files_with_metal_count += 1
    
    # Prep dictionary with metal indices as keys
    for i in metal_atoms:
        metal_ligand_dict_by_cutoff[i] = []
        metal_ligand_dict_by_CONECT[i] = []
        metal_ligand_dict_in_cutoff_not_CONECT[i] = []
        metal_ligand_dict_in_CONECT_not_cutoff[i] = []
        metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT[i] = []
        
        with lock:
            metal_count += 1
        
    # Compute distances
    metal_all_distances = md.compute_distances(traj, metal_all_pairs)
    
    # Populate the metal_ligand_dict_by_cutoff with atoms closer than cutoff
    for i in range(len(metal_all_distances[0])):
        if metal_all_distances[0, i] < cutoff:
            if metal_all_pairs[i, 0] in metal_atoms:
                metal_ligand_dict_by_cutoff[metal_all_pairs[i, 0]].append(metal_all_pairs[i, 1])
            elif metal_all_pairs[i, 1] in metal_atoms:
                metal_ligand_dict_by_cutoff[metal_all_pairs[i, 1]].append(metal_all_pairs[i, 0])
                
    # Look at the CONECT record through topology.bonds
    for i in metal_ligand_dict_by_CONECT:
        for bond in topo.bonds:
            if bond[0].index == i:
                metal_ligand_dict_by_CONECT[i].append(bond[1].index)
            elif bond[1].index == i:
                metal_ligand_dict_by_CONECT[i].append(bond[0].index)
                
    # Compare the contents of metal_ligand_dict_by_cutoff and metal_ligand_dict_by_CONECT, correct for cutoff recognizing extra atoms for residues already in CONECT
    for i in metal_atoms:
        metal_ligand_dict_in_cutoff_not_CONECT[i] = [x for x in metal_ligand_dict_by_cutoff[i] if x not in metal_ligand_dict_by_CONECT[i]]
        metal_ligand_dict_in_CONECT_not_cutoff[i] = [x for x in metal_ligand_dict_by_CONECT[i] if x not in metal_ligand_dict_by_cutoff[i]]    
    
    for i in metal_atoms:
        for j in metal_ligand_dict_in_cutoff_not_CONECT[i]:
            if not any(topo.atom(j).residue == topo.atom(k).residue for k in metal_ligand_dict_by_CONECT[i]):
                metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT[i].append(j)
    
    
    # compare the cutoff and CONECT data and make conclusions
    for i in metal_atoms:
        
        if not metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT[i] and not metal_ligand_dict_in_CONECT_not_cutoff[i]:
            with lock:
                both_equal_count_by_atom += 1
            if not both_equal_for_file_analyzed:
                with lock:
                    both_equal_count_by_file += 1
                    both_equal_for_file_analyzed = True
        
        elif metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT[i] and not metal_ligand_dict_in_CONECT_not_cutoff[i]:
            with lock:
                 extra_in_cutoff_count_by_atom += 1
            if not extra_in_cutoff_for_file_analyzed:
                with lock:
                    extra_in_cutoff_count_by_file += 1
                    extra_in_cutoff_for_file_analyzed = True
        
        elif metal_ligand_dict_in_CONECT_not_cutoff[i] and not metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT[i]:
            with lock:
                 extra_in_CONECT_count_by_atom += 1
            if not extra_in_CONECT_for_file_analyzed:
                with lock:
                    extra_in_CONECT_count_by_file += 1
                    extra_in_CONECT_for_file_analyzed = True
                 
        elif metal_ligand_dict_in_CONECT_not_cutoff[i] and metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT[i]:
            
            if len(metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT[i]) > len(metal_ligand_dict_in_CONECT_not_cutoff[i]):
                with lock:
                     both_extra_cutoff_higher_count_by_atom += 1
                if not both_extra_for_file_analyzed:
                    with lock:
                        both_extra_count_by_file += 1
                        both_extra_for_file_analyzed = True
            
            elif len(metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT[i]) < len(metal_ligand_dict_in_CONECT_not_cutoff[i]):
                with lock:
                     both_extra_CONECT_higher_count_by_atom += 1
                     if not both_extra_for_file_analyzed:
                         with lock:
                             both_extra_count_by_file += 1
                             both_extra_for_file_analyzed = True
                     
            elif len(metal_ligand_dict_CORRECTED_in_cutoff_not_CONECT[i]) == len(metal_ligand_dict_in_CONECT_not_cutoff[i]):
                with lock:
                     both_extra_both_equal_by_atom += 1
                     if not both_extra_for_file_analyzed:
                         with lock:
                             both_extra_count_by_file += 1
                             both_extra_for_file_analyzed = True
                             
    # build results dictionary
    dictionary_of_process_counts = {}
    dictionary_of_process_counts['ok_file_count'] = ok_file_count
    dictionary_of_process_counts['error_file_count'] = error_file_count
    dictionary_of_process_counts['files_with_metal_count'] = files_with_metal_count
    dictionary_of_process_counts['metal_count'] = metal_count
    dictionary_of_process_counts['both_equal_count_by_atom'] = both_equal_count_by_atom
    dictionary_of_process_counts['extra_in_cutoff_count_by_atom'] = extra_in_cutoff_count_by_atom
    dictionary_of_process_counts['extra_in_CONECT_count_by_atom'] = extra_in_CONECT_count_by_atom
    dictionary_of_process_counts['both_extra_CONECT_higher_count_by_atom'] = both_extra_CONECT_higher_count_by_atom
    dictionary_of_process_counts['both_extra_cutoff_higher_count_by_atom'] = both_extra_cutoff_higher_count_by_atom
    dictionary_of_process_counts['both_extra_both_equal_by_atom'] = both_extra_both_equal_by_atom
    dictionary_of_process_counts['both_equal_count_by_file'] = both_equal_count_by_file
    dictionary_of_process_counts['extra_in_cutoff_count_by_file'] = extra_in_cutoff_count_by_file
    dictionary_of_process_counts['extra_in_CONECT_count_by_file'] = extra_in_CONECT_count_by_file
    dictionary_of_process_counts['both_extra_count_by_file'] = both_extra_count_by_file                          
                                                          
    return dictionary_of_process_counts                                                      
                     
