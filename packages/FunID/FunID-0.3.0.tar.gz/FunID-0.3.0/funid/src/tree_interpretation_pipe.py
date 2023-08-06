# Performing multiple tree interpretation
from ete3 import Tree
from funid.src import tree_interpretation
from funid.src.tool import initialize_path, get_genus_species, mkdir
from funid.src.hasher import encode, decode
from funid.src.reporter import Singlereport
import pandas as pd
import sys, os
import shutil
import logging
import multiprocessing as mp

### For single dataset
# Input : out, group, gene, V, path, opt
def pipe_module_tree_interpretation(
    out,
    group,
    gene,
    V,
    path,
    opt,
):

    # To reduce memory usage in multithreaded performance, copy necessary objects and then remove V
    funinfo_dict = V.dict_hash_FI
    funinfo_list = V.list_FI
    hash_dict = V.dict_hash_name
    query_list = V.dict_dataset[group][gene].list_qr_FI
    outgroup = V.dict_dataset[group][gene].list_og_FI
    # for unexpectively included sequence during clustering
    db_list = list(
        set([FI for FI in V.list_FI if FI.datatype == "db"])
        - set(outgroup)
        - set(query_list)
    )
    genus_list = V.tup_genus

    del V

    # For get_genus_species
    initialize_path(path)

    # Tree name selection for tree construction software
    tree_name = f"{path.out_tree}/hash/hash_{opt.runname}_{group}_{gene}.nwk"
    logging.debug(tree_name)

    if os.path.isfile(tree_name):
        Tree(tree_name, format=2)
    else:
        logging.warning(f"Cannot find {tree_name}")
        raise Exception

    # initialize before analysis
    Tree_style = tree_interpretation.Tree_style()

    # Read tree
    tree_info = tree_interpretation.Tree_information(
        tree_name, Tree_style, group, gene, opt
    )

    # Give necessary variables parsed from dataset
    tree_info.db_list = db_list
    tree_info.query_list = query_list
    tree_info.outgroup = outgroup
    tree_info.funinfo_dict = funinfo_dict

    # Main phase
    # calculate zero distance with alignment
    if gene != "concatenated":
        tree_info.calculate_zero(
            f"{path.out_alignment}/{opt.runname}_hash_trimmed_{group}_{gene}.fasta"
        )
    else:
        tree_info.calculate_zero(
            f"{path.out_alignment}/{opt.runname}_hash_trimmed_{group}_concatenated.fasta"
        )

    # Reroot outgroup and save original tree into image
    tree_info.reroot_outgroup(
        f"{path.out_tree}/hash_{opt.runname}_{group}_{gene}_original.svg"
    )
    # Decode hash of image
    # Should work more on non-safe characters
    tree_hash_dict = encode(funinfo_list, newick=True)

    decode(
        tree_hash_dict,
        f"{path.out_tree}/hash_{opt.runname}_{group}_{gene}_original.svg",
        f"{path.out_tree}/{opt.runname}_{group}_{gene}_original.svg",
        newick=True,
    )

    # In validation mode, use original sp. number
    if opt.mode == "validation":
        tree_info.reserve_sp()

    # Reconstruct flat branches if option given
    if opt.solveflat is True:
        tree_info.t = tree_info.reconstruct(tree_info.t.copy("newick"), gene)

    # reorder tree for pretty look
    tree_info.t.ladderize(direction=1)

    # Search tree and delimitate species
    tree_info.tree_search(tree_info.t, gene)

    return tree_info


### synchronize sp. numbers from multiple dataset
# to use continuous sp numbers over trees
# Seperated because this step cannot be done by multiprocessing
def synchronize(V, tree_info_list):

    # Get all available genus from tree_info
    def get_possible_genus(tree_info):
        return set([taxon[0] for taxon in tree_info.collapse_dict])

    tree_info_dict = {}

    # get available groups per genus
    tree_info_dict = {}

    for tree_info in tree_info_list:
        possible_genus = get_possible_genus(tree_info)
        for genus in possible_genus:
            if not (genus) in tree_info_dict:
                tree_info_dict[genus] = {tree_info.group: {tree_info.gene: tree_info}}
            elif not (tree_info.group in tree_info_dict[genus]):
                tree_info_dict[genus][tree_info.group] = {tree_info.gene: tree_info}
            elif not (tree_info.gene in tree_info_dict[genus][tree_info.group]):
                tree_info_dict[genus][tree_info.group][tree_info.gene] = tree_info
            else:
                logging.error("DEVELOPMENTAL ERROR, DUPLICATED TREE_INFO")
                raise exception

    for genus in tree_info_dict.keys():
        # cnt number that should be added
        cnt_sp_adder = 0
        for group in sorted(list(tree_info_dict[genus].keys())):
            if not ("concatenated" in tree_info_dict[genus][group]):
                logging.error("DEVELOPMENTAL ERROR, NO CONCATENATED ANALYSIS")
                raise exception
            else:
                # Start with concatenated
                tree_info = tree_info_dict[genus][group]["concatenated"]

                # Get all sp taxon list
                taxon_set = set()
                for taxon in tree_info.collapse_dict.keys():
                    if "sp." in taxon[1]:
                        taxon_set.add(taxon)

                hash_dict = {}
                # Make one hash - one sp dict pair
                for taxon in taxon_set:
                    for leaf in tree_info.collapse_dict[taxon][0].leaf_list:
                        hash_dict[leaf[0]] = (
                            taxon[0],
                            f"sp. {str(int(taxon[1].split(' ')[1]) + cnt_sp_adder)}",
                        )

                ## Change it with cnt_sp_adder
                for taxon in taxon_set:
                    tree_info.collapse_dict[
                        (
                            taxon[0],
                            f"tmp sp. {str(int(taxon[1].split(' ')[1]) + cnt_sp_adder)}",
                        )
                    ] = tree_info.collapse_dict.pop(taxon)

                # Performing in two steps in order to tkae collapse_dict safe
                for taxon in taxon_set:
                    tree_info.collapse_dict[
                        (
                            taxon[0],
                            f"sp. {str(int(taxon[1].split(' ')[1]) + cnt_sp_adder)}",
                        )
                    ] = tree_info.collapse_dict.pop(
                        (
                            taxon[0],
                            f"tmp sp. {str(int(taxon[1].split(' ')[1]) + cnt_sp_adder)}",
                        )
                    )

                # Now solve other genes
                for gene in tree_info_dict[genus][group]:
                    if gene != "concatenated":
                        bygene_taxon_dict = {}

                        tree_info = tree_info_dict[genus][group][gene]

                        # Synchronize bygene taxon name to concatenated
                        for taxon in tree_info.collapse_dict:

                            # Do not change non- sp.
                            if "sp." in taxon[1]:

                                hash_list = [
                                    leaf[0]
                                    for leaf in tree_info.collapse_dict[taxon][
                                        0
                                    ].leaf_list
                                ]

                                available_set = set()
                                for _hash in hash_list:
                                    if _hash in hash_dict:
                                        available_set.add(hash_dict[_hash][1])

                                species_text = "/".join(sorted(list(available_set)))

                                if not (".sp") in taxon[1]:
                                    species_text = f"{taxon[1]}/{species_text}"

                                bygene_taxon_dict[taxon] = species_text

                        # Change taxon name
                        tmp_taxon_list = [key for key in tree_info.collapse_dict]
                        for taxon in tmp_taxon_list:
                            if "sp." in taxon[1]:
                                tree_info.collapse_dict[
                                    (taxon[0], bygene_taxon_dict[taxon])
                                ] = tree_info.collapse_dict.pop(taxon)
                cnt_sp_adder += len(taxon_set)

    # Return sp number fixed tree_info_list
    return tree_info_list


### Visualization after synchronization
def pipe_module_tree_visualization(
    tree_info,
    group,
    gene,
    V,
    path,
    opt,
):

    genus_list = V.tup_genus

    # Collapse tree branches for visualization
    tree_info.collapse_tree()

    # Polish tree image
    tree_info.polish_image(
        f"{path.out_tree}/{opt.runname}_{group}_{gene}.svg", genus_list
    )

    # sort taxon order
    list_taxon_1 = [
        taxon
        for taxon in tree_info.collapse_dict.keys()
        if not (taxon[1].startswith("sp."))
    ]
    list_taxon_2 = [
        taxon for taxon in tree_info.collapse_dict.keys() if taxon[1].startswith("sp.")
    ]
    list_taxon_1.sort(key=lambda x: x[1])
    list_taxon_2.sort(key=lambda x: x[1])
    list_taxon = list_taxon_1 + list_taxon_2

    # Declare report collection
    report_list = []
    for taxon in list_taxon:
        # If only one taxon exists, enumerate does not work properly
        if len(tree_info.collapse_dict[taxon]) <= 1:
            collapse_info = tree_info.collapse_dict[taxon][0]
            # Get each of the leaf result to report
            for leaf in collapse_info.leaf_list:
                report = Singlereport()
                report.id = V.dict_hash_FI[leaf[0]].original_id
                report.hash = V.dict_hash_FI[leaf[0]].hash
                report.update_group(group)
                report.update_gene(gene)
                report.update_species_original(
                    get_genus_species(leaf[2], genus_list=genus_list)
                )
                report.update_species_assigned(taxon)
                report.ambiguous = collapse_info.clade_cnt
                report.flat = collapse_info.flat

                report_list.append(report)

        else:
            for n, collapse_info in enumerate(tree_info.collapse_dict[taxon]):
                for leaf in collapse_info.leaf_list:
                    report = Singlereport()
                    report.id = V.dict_hash_FI[leaf[0]].original_id
                    report.hash = V.dict_hash_FI[leaf[0]].hash
                    report.update_group(group)
                    report.update_gene(gene)
                    report.update_species_original(
                        get_genus_species(leaf[2], genus_list=genus_list)
                    )
                    report.update_species_assigned((" ".join(taxon), f"{n+1}"))
                    report.ambiguous = collapse_info.clade_cnt
                    report.flat = collapse_info.flat

                    report_list.append(report)

    return report_list


### For all datasets, multiprocessing part
def pipe_tree_interpretation(V, path, opt):
    tree_interpretation_opt = []

    for group in V.dict_dataset:
        for gene in V.dict_dataset[group]:
            # draw tree only when query sequence exists
            if (
                len(V.dict_dataset[group][gene].list_qr_FI) > 0
                or opt.queryonly is False
            ):

                # Generating tree_interpretation opts for multithreading support
                tree_interpretation_opt.append(
                    (
                        f"{opt.runname}_{group}_{gene}",
                        group,
                        gene,
                        V,
                        path,
                        opt,
                    )
                )

    # Tree interpretation - outgroup, reconstruction(solve_flat), collapsing
    if opt.verbose < 3:
        p = mp.Pool(opt.thread)
        tree_info_list = p.starmap(
            pipe_module_tree_interpretation, tree_interpretation_opt
        )
        p.close()
        p.join()

    else:
        # non-multithreading mode for debugging
        tree_info_list = [
            pipe_module_tree_interpretation(*option)
            for option in tree_interpretation_opt
        ]

    # Synchronize sp. numbers
    tree_info_list = synchronize(V, tree_info_list)

    tree_interpretation_result = []
    for tree_info in tree_info_list:
        tree_interpretation_result.append(
            pipe_module_tree_visualization(
                tree_info, tree_info.group, tree_info.gene, V, path, opt
            )
        )

    # Collect identifiation result to V
    for raw_result in tree_interpretation_result:
        if raw_result is not (None):
            for result in raw_result:
                FI = V.dict_hash_FI[result.hash]
                if result.gene == "concatenated" or opt.concatenate is False:
                    # logging.debug("Updating final species")
                    FI.final_species = result.species_assigned
                    FI.species_identifier = result.ambiguous
                    if result.flat is True:
                        FI.flat.append("concatenated")
                else:
                    # logging.debug("Not updating final species")
                    FI.bygene_species[result.gene] = result.species_assigned
                    if result.flat is True:
                        FI.flat.append(result.gene)

    return V, path, opt
