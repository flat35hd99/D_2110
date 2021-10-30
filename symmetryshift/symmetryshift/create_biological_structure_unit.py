import sys
# If you want to use in jphacks/D_2110 repository, refer Quick install guide on README file
# https://github.com/jphacks/D_2110#quick-install-and-use-guide
# or disable comment-out below  

# sys.path.append(os.path.join(os.path.dirname(__file__), "../../biopython"))

from Bio.PDB import PDBParser, PDBList, PDBIO, parse_pdb_header

def creater(pdb_id: str, output="out.pdb"):
    # Fetch PDB file
    pdb = PDBList()
    pdb_file = pdb.retrieve_pdb_file(pdb_id, file_format="pdb")
    
    # Get header information
    dictionary = parse_pdb_header(pdb_file)

    # Get structure
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(pdb_id, pdb_file)
    models = list(structure.get_models())
    model = models[0]
    chains = list(structure.get_chains())

    # Work operator
    chain_ids_to_work_symmetry_operator = dictionary["chain_ids_to_work_symmetry_operator"]
    new_chain_ids_candicate = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        ]
    chain_ids = [chain.get_id() for chain in chains]
    new_chain_ids = list(x for x in new_chain_ids_candicate if x not in chain_ids)
    for chain in chains:
        if chain.get_id() in chain_ids_to_work_symmetry_operator:
            for operator in dictionary["symmetry_operator"]:
                new_chain = chain * operator["matrix"] + operator["shift"]
                new_chain._id = new_chain_ids.pop(0)
                model.add(new_chain)

    structure.detach_child(0)
    structure.add(model)

    # Save new structure as PDB file
    io = PDBIO()
    io.set_structure(structure)
    io.save(output)

def main():
    pdb_id = sys.argv[1]
    if len(sys.argv) >= 3:
        output_filename = sys.argv[2]
        creater(pdb_id=pdb_id, output=output_filename)
    else:
        creater(pdb_id=pdb_id)

if __name__ == "__main__":
    main()
