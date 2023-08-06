# CAT-V is short for Command-based Automated Tree - Visualizer
from ete3 import (
    Tree,
    TreeStyle,
    NodeStyle,
    TextFace,
    CircleFace,
    RectFace,
    faces,
)
from Bio import SeqIO
from copy import deepcopy
from time import sleep
import lxml.etree as ET
import pandas as pd
from functools import lru_cache
from funid.src.tool import get_genus_species
import dendropy
import collections
import os
import re
import sys
import json

# Get maximum tree distance in given tree
def get_max_distance(tree):

    max_distance = 0
    tree = deepcopy(tree)
    (farthest_node, max_distance) = tree.detach().get_farthest_node()
    return max_distance


def divide_by_max_len(string, max_len, sep=" "):

    # divide string by new line character to prevent long string from being cut
    # by the maximum length of the string
    final_string = ""
    tmp_string = ""

    for char in string:
        if char == sep:
            if len(tmp_string) < max_len:
                tmp_string += char
            else:
                tmp_string += char
                final_string += tmp_string + "\n"
                tmp_string = ""
        else:
            tmp_string += char
    final_string += tmp_string
    return final_string


# per clade information
class Collapse_information:
    def __init__(self):
        self.query_list = []
        self.db_list = []
        self.outgroup = []
        self.clade = ""
        self.leaf_list = []
        self.clade_cnt = 0  # if clade with same name exists, use this as counter
        self.collapse_type = (
            ""  # line - for single clade / triangle - for multiple clade
        )
        self.color = ""  # color after collapsed
        self.height = ""
        self.width = ""
        self.taxon = ""  # taxon name to be shown
        self.n_db = 0
        self.n_query = 0
        self.n_others = 0
        self.flat = False

    def __str__(self):
        return f"clade {self.taxon} with {len(self.leaf_list)} leaves"


"""
class Visual_information:
    def __init__(self):
        self.bootstrap_cutoff = 70
        self.designated_genus = "Tmpgenus"
        self.const_width = 1000
        self.const_height = 6
        self.const_max_len = 48
        self.black = "#000000"
        self.highlight = "#bb0000"
        self.bgcolor1 = "#f4f4f4"
        self.bgcolor2 = "#c6c6c6"
        self.outgroup_color = "#999999"
        self.fsize = 10
        self.ftype = "Arial"
        self.fsize_bootstrap = 10
        self.shorten_genus = True
        self.solve_flat = True
        self.zero = 0.00000100000050002909
        # numbers equal or same to option.zero were considered option.zero length


zero = 0.00000100000050002909  # for better binding
"""


def concat_clade(
    clade1,
    clade2,
    dist1,
    dist2,
    root_dist,
    support1=1,
    support2=1,
):

    tmp = Tree()
    tmp.dist = root_dist
    tmp.support = 1
    # tmp = Tree.add_child(name="tmp1", dist=option.zero)
    tmp.add_child(clade1, dist=dist1, support=support1)
    tmp.add_child(clade2, dist=dist2, support=support2)
    return tmp


# concat all branches for concatenation
def concat_all(clade_tuple, root_dist, zero):

    if len(clade_tuple) == 0:
        print("No clade input found, abort")
        raise Exception

    elif len(clade_tuple) == 1:
        return clade_tuple[0].copy("newick")
    elif len(clade_tuple) == 2:
        return_clade = clade_tuple[0].copy("newick")
        return_clade = concat_clade(
            clade1=return_clade,
            clade2=clade_tuple[1].copy("newick"),
            dist1=return_clade.dist,
            dist2=clade_tuple[1].dist,
            root_dist=root_dist,
        )
    elif len(clade_tuple) >= 3:
        # First clade
        return_clade = clade_tuple[0].copy("newick")
        # Second to last-1 clade
        for c in clade_tuple[1:-1]:
            return_clade = concat_clade(
                clade1=return_clade,
                clade2=c.copy("newick"),
                dist1=return_clade.dist,
                dist2=c.dist,
                root_dist=zero,
            )
        # Last clade
        return_clade = concat_clade(
            clade1=return_clade,
            clade2=clade_tuple[-1].copy("newick"),
            dist1=return_clade.dist,
            dist2=clade_tuple[-1].dist,
            root_dist=root_dist,
        )
    else:
        raise Exception

    return return_clade


class Tree_style:
    def __init__(self):
        self.ts = TreeStyle()
        self.ts.scale = 1000
        # self.ts.show_branch_length = True
        # self.ts.show_branch_support = True
        self.ts.branch_vertical_margin = 10
        self.ts.allow_face_overlap = True
        self.ts.children_faces_on_top = True
        self.ts.complete_branch_lines_when_necessary = False
        self.ts.extra_branch_line_color = "black"
        self.ts.margin_left = 200
        self.ts.margin_right = 200
        self.ts.margin_top = 200
        self.ts.margin_bottom = 200
        self.ts.show_leaf_name = False


class Tree_information:
    def __init__(self, tree, Tree_style, group, gene, opt):

        self.tree_name = tree  # for debugging
        self.t = Tree(tree)
        self.group = group
        self.gene = gene
        self.dendro_t = dendropy.Tree.get(
            path=self.tree_name, schema="newick"
        )  # dendropy format for distance calculation

        # if support ranges from 0 to 1, change it from 0 to 100
        # b for branch
        support_set = set()
        for b in self.t.traverse():
            support_set.add(b.support)

        if max(support_set) <= 1:
            for b in self.t.traverse():
                b.support = int(100 * b.support)

        self.query_list = []
        self.db_list = []
        self.outgroup = []
        self.outgroup_leaf_name_list = []
        self.funinfo_dict = {}  # leaf.name : Funinfo

        self.sp_cnt = 1
        self.reserved_sp = set()

        self.Tree_style = Tree_style
        self.opt = opt

        self.collapse_dict = {}  # { taxon name : collapse_info }

        self.outgroup_clade = None
        self.bgstate = 0
        self.additional_clustering = True
        self.zero = 0.00000100000050002909

    # to find out already existing new species number to avoid overlapping
    # e.g. avoid sp 5 if P. sp 5 already exsits in database
    def reserve_sp(self):

        for leaf in self.t.iter_leaves():
            sys.stdout.flush()
            taxon = (
                self.funinfo_dict[leaf.name].genus,
                self.funinfo_dict[leaf.name].ori_species,
            )
            sys.stdout.flush()
            if taxon[1].split(" ")[0] in ("sp", "sp."):
                self.reserved_sp.add(" ".join(taxon[1].split(" ")[1:]))

    # this function decides whether the string is db or query
    @lru_cache(maxsize=10000)
    def decide_type(self, string, by="hash", priority="query"):
        query = False
        db = False

        query_list = [FI.hash for FI in self.query_list]
        db_list = [FI.hash for FI in self.db_list]
        outgroup_list = [FI.hash for FI in self.outgroup]

        if by == "hash":
            if string in query_list:
                return "query"
            elif string in db_list:
                return "db"
            elif string in outgroup_list:
                return "outgroup"
            else:
                return "none"

        elif by == "accession":
            db_list = [
                self.funinfo_dict[x].accession
                for x in self.funinfo_dict
                if self.funinfo_dict[x].datatype == "db"
            ]
            query_list = [
                self.funinfo_dict[x].accession
                for x in self.funinfo_dict
                if self.funinfo_dict[x].datatype == "query"
            ]

            if string in query_list:
                return "query"
            elif string in db_list:
                return "db"
            else:
                return "none"

        elif by == "original_id":
            db_list = [
                self.funinfo_dict[x].original_id
                for x in self.funinfo_dict
                if self.funinfo_dict[x].datatype == "db"
            ]
            query_list = [
                self.funinfo_dict[x].original_id
                for x in self.funinfo_dict
                if self.funinfo_dict[x].datatype == "query"
            ]

            if string in query_list:
                return "query"
            elif string in db_list:
                return "db"
            else:
                return "none"

        # elif by == "regex": # legacy code, mabye used for standalone CAT_V
        else:
            for regex in self.query_list:
                if re.search(regex, string):
                    query = True

            for regex in self.db_list:
                if re.search(regex, string):
                    db = True

            if priority == "query":
                if query == True:
                    return "query"
                elif db == True:
                    return "db"
                else:
                    return "none"

            elif priority == "db":
                if db == True:
                    return "db"
                elif query == True:
                    return "query"
                else:
                    return "none"

    # Calculate zero length branch length cutoff with given tree and alignment
    def calculate_zero(self, alignment_file):

        # Parse alignment
        seq_list = list(SeqIO.parse(alignment_file, "fasta"))

        # Check if tree leaves and alignments are consensus
        hash_list_tree = [leaf.name for leaf in self.t]
        hash_list_alignment = [seq.id for seq in seq_list]

        if collections.Counter(hash_list_tree) != collections.Counter(
            hash_list_alignment
        ):
            print(
                f"[ERROR] content of tree and alignment is not identical for {self.tree_name}"
            )
            raise Exception

        # Find identical or including pairs in alignment
        identical_pairs = []
        unidentical_pairs = []
        for seq1 in seq_list:
            for seq2 in seq_list:
                if not (
                    str(seq1.id).strip() == str(seq2.id).strip()
                    or (seq1.id, seq2.id) in identical_pairs
                    or (seq2.id, seq1.id) in identical_pairs
                    or (seq1.id, seq2.id) in unidentical_pairs
                    or (seq2.id, seq1.id) in unidentical_pairs
                ):
                    seq1_clean = str(seq1.seq).replace("-", "")
                    seq2_clean = str(seq2.seq).replace("-", "")
                    if seq1_clean in seq2_clean or seq2_clean in seq1_clean:
                        identical_pairs.append(
                            tuple(sorted([str(seq1.id).strip(), str(seq2.id).strip()]))
                        )
                    else:
                        unidentical_pairs.append(
                            tuple(sorted([str(seq1.id).strip(), str(seq2.id).strip()]))
                        )

        # make phylogenetic distance matrix
        pdc = self.dendro_t.phylogenetic_distance_matrix().as_data_table()._data

        # For each alignment pairs, find tree length

        set_identical = set()
        set_unidentical = set()

        # If very short sequence exsists, zero length might be too big
        for pair in identical_pairs:
            set_identical.add(pdc[pair[0]][pair[1]])

        for pair in unidentical_pairs:
            set_unidentical.add(pdc[pair[0]][pair[1]])

        if len(set_identical) > 0 and len(set_unidentical) > 0:
            if max(set_identical) < min(set_unidentical):
                self.zero = max(set_identical)
            else:
                self.zero = min(set_unidentical) - 0.0000000000001

        elif len(set_identical) > 0:
            self.zero = max(set_identical)

        # returm maximum
        return self.zero

    def reroot_outgroup(self, out):

        # rerooting
        # Reroot should be done first because unrooted tree has 3 children

        outgroup_leaves = []
        self.t.resolve_polytomy()

        for leaf in self.t:
            if leaf.name.startswith("_R_"):
                leaf.name = leaf.name[3:]

        for outgroup in self.outgroup:
            print(f"finding outgroup {outgroup} ({outgroup.hash}) in {self.tree_name}")
            for leaf in self.t:
                # print(f"leaf: {leaf.name} outgroup: {outgroup.hash}")
                if outgroup.hash in leaf.name:
                    outgroup_leaves.append(leaf)

        self.outgroup_leaf_name_list = [leaf.name for leaf in outgroup_leaves]

        # find smallest monophyletic clade that contains all leaves in outgroup_leaves
        # reroot with outgroup_clade
        # print(outgroup_leaves)

        try:
            if len(outgroup_leaves) >= 2:
                self.outgroup_clade = self.t.get_common_ancestor(outgroup_leaves)
                self.t.set_outgroup(self.outgroup_clade)
                self.t.ladderize(direction=1)
                self.outgroup_clade = self.t.get_common_ancestor(outgroup_leaves)
            elif len(outgroup_leaves) == 1:
                self.outgroup_clade = outgroup_leaves[0]
                self.t.set_outgroup(self.outgroup_clade)
                self.t.ladderize(direction=1)
                self.outgroup_clade = outgroup_leaves[0]
            else:
                print(f"[Warning] no outgroup selected in {self.tree_name}")
                raise Exception

            if len(outgroup_leaves) != len(self.outgroup_clade):
                print(
                    f"[Warning] outgroup does not seems to be monophyletic in {self.tree_name}"
                )

        except:
            print(f"[Warning] no outgroup selected in {self.tree_name}")

            outgroup_flag = False
            # if outgroup_clade is on the root side, reroot with other leaf temporarily and reroot again
            for leaf in self.t:
                if not (leaf in outgroup_leaves):
                    self.t.set_outgroup(leaf)
                    # Rerooting again while outgrouping gets possible
                    try:
                        self.outgroup_clade = self.t.get_common_ancestor(
                            outgroup_leaves
                        )
                        print(f"Ancestor: {self.outgroup_clade}")
                        self.t.set_outgroup(self.outgroup_clade)
                        outgroup_flag = True
                        break
                    except:
                        pass

            if outgroup_flag is False:
                # never erase this for debugging
                print(f"Outgroup not selected in {self.tree_name}")
                print(f"Outgroup leaves: {outgroup_leaves}")
                print(f"Outgroup : {self.outgroup}")
                print(f"Outgroup clade : {self.outgroup_clade}")
                raise Exception

        self.Tree_style.ts.show_leaf_name = True
        for node in self.t.traverse():
            node.img_style["size"] = 0  # removing circles whien size is 0

        self.t.render(f"{out}", tree_style=self.Tree_style.ts)
        self.Tree_style.ts.show_leaf_name = False

    # String manipulation operations

    # count number of taxons in the clade
    @lru_cache(maxsize=10000)
    def taxon_count(self, clade, gene, count_query=False):

        taxon_dict = {}

        for leaf in clade:
            taxon = ("", "")
            if count_query == True:
                taxon = (
                    self.funinfo_dict[leaf.name].genus,
                    self.funinfo_dict[leaf.name].bygene_species[gene],
                )
            elif (
                self.decide_type(leaf.name) == "db"
                or self.decide_type(leaf.name) == "outgroup"
            ):
                taxon = (
                    self.funinfo_dict[leaf.name].genus,
                    self.funinfo_dict[leaf.name].bygene_species[gene],
                )

            if not (taxon is None):
                if not (taxon in taxon_dict):
                    taxon_dict[taxon] = 1
                else:
                    taxon_dict[taxon] += 1

        # Remove empty taxon after counting taxon
        taxon_dict.pop(("", ""), None)

        return taxon_dict

    @lru_cache(maxsize=10000)
    def genus_count(self, gene, clade):

        taxon_dict = {}

        for leaf in clade.iter_leaves():
            if (
                self.decide_type(leaf.name) == "db"
                or self.decide_type(leaf.name) == "outgroup"
            ):
                if not (
                    (
                        self.funinfo_dict[leaf.name].genus,
                        self.funinfo_dict[leaf.name].bygene_species[gene],
                    )
                    in taxon_dict
                ):
                    taxon_dict[
                        (
                            self.funinfo_dict[leaf.name].genus,
                            self.funinfo_dict[leaf.name].bygene_species[gene],
                        )[0]
                    ] = 1
                else:
                    taxon_dict[
                        (
                            self.funinfo_dict[leaf.name].genus,
                            self.funinfo_dict[leaf.name].bygene_species[gene],
                        )[0]
                    ] += 1

        return taxon_dict

    @lru_cache(maxsize=10000)
    def designate_genus(self, gene, clade):

        genus_dict = self.genus_count(gene, clade)

        if len(genus_dict) >= 2:  # if genus is not clear
            return "Ambiguousgenus"
        elif len(genus_dict) == 1:
            return list(genus_dict.keys())[0]
        else:
            return self.designate_genus(gene, clade.up)
            """
            try:
                return self.designate_genus(clade.up)
            except:
                return "Unknowngenus"
            """

    # this function finds major species of the clade
    # returns (genus, species)
    @lru_cache(maxsize=10000)
    def find_majortaxon(self, clade, gene, opt=None):

        taxon_dict = self.taxon_count(clade, gene)
        max_value = 0
        major_taxon = ("", "")

        for taxon in taxon_dict:
            if taxon_dict[taxon] > max_value:
                max_value = taxon_dict[taxon]
                major_taxon = taxon

        if major_taxon == ("", ""):
            if opt is None:
                # if major species not selected, try to match genus at least
                major_taxon = (
                    self.designate_genus(gene, clade),
                    f"sp. {self.sp_cnt}",
                )

            elif opt.mode == "validation":  # in validation mode, try to follow query sp
                taxon_dict = self.taxon_count(clade, gene, count_query=True)
                max_value = 0
                for taxon in taxon_dict:
                    if taxon_dict[taxon] > max_value:
                        max_value = taxon_dict[taxon]
                        major_taxon = taxon

                if not (major_taxon[1].startswith("sp")):
                    major_taxon = (
                        self.designate_genus(gene, clade),
                        f"sp. {self.sp_cnt}",
                    )

            else:
                major_taxon = (
                    self.designate_genus(gene, clade),
                    f"sp. {self.sp_cnt}",
                )

        return major_taxon

    def collapse(self, collapse_info, clade, taxon):

        collapse_info.clade = clade
        collapse_info.taxon = taxon

        if len(clade) == 1:
            collapse_info.collapse_type = "line"
        elif len(clade) >= 2:
            collapse_info.collapse_type = "triangle"
        else:
            raise Exception

        if (
            any(self.decide_type(leaf.name) == "query" for leaf in clade.iter_leaves())
            == True
        ):
            collapse_info.color = self.opt.visualize.highlight
        else:
            collapse_info.color = "#000000"

        # all these things were ignored when type is line
        collapse_info.width = get_max_distance(clade) * 1000
        # scale problem when visualizing
        collapse_info.height = len(clade) * self.opt.visualize.heightmultiplier

        # count query, db, others
        for leaf in clade.iter_leaves():
            if (
                self.decide_type(leaf.name) == "db"
                or self.decide_type(leaf.name) == "outgroup"
            ):
                collapse_info.leaf_list.append((leaf.name, "#000000", leaf.name))
                collapse_info.n_db += 1
            elif self.decide_type(leaf.name) == "query":
                collapse_info.leaf_list.append(
                    (leaf.name, self.opt.visualize.highlight, leaf.name)
                )
                collapse_info.n_query += 1
            else:
                # if some errornous count occurs, that maybe because of this part
                # however, the last part of tuple is essential for CAT_V pipe to collect data
                # it is not sure why "other" exists - that might be outgroup
                collapse_info.leaf_list.append((leaf.name, "#000000", leaf.name))
                collapse_info.n_others += 1

    def tree_search(self, clade, gene):
        def check_monophyletic(self, clade, gene):
            # if given clade is clade with db or only query
            def decide_clade(clade, gene):
                taxon_dict = self.taxon_count(clade, gene)
                if len(taxon_dict.keys()) == 0:
                    return "query"
                else:
                    return "db"

            # decides if the clade is monophyletic
            def is_monophyletic(self, clade, gene, taxon):

                taxon_dict = self.taxon_count(clade, gene)

                if (
                    len(taxon_dict.keys()) == 0
                ):  # if taxon dict.keys() have 0 species: all query
                    for children in clade.children:
                        if (
                            children.dist > self.opt.collapsedistcutoff
                        ):  # if any of the branch length was too long for single clade
                            return False
                    return True
                elif len(taxon_dict.keys()) == 1:

                    # if taxon dict.keys() have only 1 species: section assigned
                    for children in clade.children:
                        # check query branch
                        if self.find_majortaxon(children, gene)[1].startswith("sp."):
                            if children.dist > self.opt.collapsedistcutoff:
                                return False
                    return True
                else:  # more than 2 species : not monophyletic
                    return False

            datatype = decide_clade(
                clade, gene
            )  # if clade only has query species or not

            # if only one clade, it is firmly monophyletic
            if len(clade.children) == 1:
                return datatype, True

            # if additional_clustering option is on, check if basal group includes query seqs
            taxon = self.find_majortaxon(clade, gene)

            if self.additional_clustering == False:
                self.opt.collapsebscutoff = 0

            if is_monophyletic(self, clade, gene, taxon):
                return datatype, True
            else:
                return datatype, False

        def generate_collapse_information(self, clade, opt=None, flat=False):

            collapse_info = Collapse_information()
            collapse_info.query_list = self.query_list
            collapse_info.db_list = self.db_list
            collapse_info.outgroup = self.outgroup
            collapse_info.flat = flat
            taxon = self.find_majortaxon(clade, gene, opt)
            self.collapse(collapse_info, clade, taxon)

            # counting new species
            if taxon[1].startswith("sp."):
                while 1:
                    self.sp_cnt += 1
                    if str(self.sp_cnt) in self.reserved_sp:
                        print(f"skipping {self.sp_cnt} to avoid overlap in database")
                        continue
                    else:
                        break
            print(f"Generating collapse information for taxon {taxon}")
            if not (taxon in self.collapse_dict):
                self.collapse_dict[taxon] = [collapse_info]
            else:
                self.collapse_dict[taxon].append(collapse_info)

        # start of tree_search
        # at the last leaf
        if len(clade.children) == 1:
            generate_collapse_information(clade, opt=self.opt)
            return

        # ordinary search
        elif len(clade.children) == 2:
            for child_clade in clade.children:

                # Calculate root distance between two childs to check flat
                flat = True if child_clade.dist <= self.zero else False

                datatype, monophyletic = check_monophyletic(self, child_clade, gene)
                if monophyletic is True:
                    generate_collapse_information(
                        self, child_clade, opt=self.opt, flat=flat
                    )
                else:
                    self.tree_search(child_clade, gene)
            return

        # if error
        else:
            print(clade.children)
            raise Exception

        # end of tree_search

    def reconstruct(self, clade, gene):

        sys.stdout.flush()

        @lru_cache(maxsize=10000)
        def solve_flat(clade):
            def consist(c):

                db = 0
                query = 0

                for leaf in c:
                    if (
                        self.decide_type(leaf.name) == "db"
                        or self.decide_type(leaf.name) == "outgroup"
                    ):
                        db += 1
                    else:
                        query += 1

                if db == 0 and query == 0:
                    print(c)
                    print(db)
                    print(query)
                    raise Exception
                elif db == 0 and query != 0:
                    return "query"
                elif db != 0 and query == 0:
                    return "db"
                else:
                    return "both"

            def get_taxon(c, gene, mode="db"):

                taxon_dict = {}

                # edited
                def t(leaf):

                    return (
                        self.funinfo_dict[leaf.name].genus,
                        self.funinfo_dict[leaf.name].bygene_species[gene],
                    )

                # if error occurs, change t to this again

                if mode == "db":
                    for leaf in c:
                        if not (t(leaf) in taxon_dict):
                            taxon_dict[t(leaf)] = 1
                        else:
                            taxon_dict[t(leaf)] += 1

                    if len(taxon_dict) == 0:
                        print(taxon_dict)
                        print(c)
                        raise Exception

                    elif len(taxon_dict) == 1:
                        return list(taxon_dict.keys())[0]
                    else:
                        return False

                elif mode == "query":

                    for leaf in c:
                        if not (t in taxon_dict):
                            taxon_dict[t(leaf)] = 1
                        else:
                            taxon_dict[t(leaf)] += 1

                    if len(taxon_dict) == 0:
                        print(taxon_dict)
                        print(c)
                        raise Exception

                    elif len(taxon_dict) == 1:
                        return list(taxon_dict.keys())[0]

                    else:
                        max_taxon = ""
                        maximum = 0
                        for taxon in taxon_dict:
                            if taxon_dict[taxon] > maximum:
                                maximum = taxon_dict[taxon]
                                max_taxon = taxon
                        return max_taxon

                elif mode == "both":

                    for leaf in c:
                        if (
                            self.decide_type(leaf.name, priority="query") == "db"
                            or self.decide_type(leaf.name, priority="query")
                            == "outgroup"
                        ):
                            if not (t in taxon_dict):
                                taxon_dict[t(leaf)] = 1
                            else:
                                taxon_dict[t(leaf)] += 1

                    if len(taxon_dict) == 0:
                        print(taxon_dict)
                        print(clade)
                        raise Exception

                    elif len(taxon_dict) == 1:
                        return list(taxon_dict.keys())[0]

                    else:
                        return False

            def seperate_clade(clade, gene, clade_list):

                for c in clade.children:
                    c_tmp = c.copy()
                    if c_tmp.dist <= self.zero:
                        if len(c_tmp) == 1:
                            clade_list.append(
                                (
                                    get_taxon(c_tmp, gene, mode=consist(c_tmp)),
                                    c_tmp,
                                    c_tmp.dist,
                                    c_tmp.support,
                                )
                            )
                        else:
                            clade_list = seperate_clade(c_tmp, gene, clade_list)
                    else:
                        c2 = self.reconstruct(c_tmp, gene)
                        clade_list.append(
                            (
                                get_taxon(c2, gene, mode=consist(c2)),
                                c2,
                                c2.dist,
                                c2.support,
                            )
                        )

                return clade_list

            # Start of function
            root_dist = clade.dist
            clade_list = seperate_clade(clade, gene, [])
            cnt = 0

            # count option.zero clades
            # result is from seperate_clade function
            # each of the result has list of (taxon, clade, dist, support)
            for result in clade_list:
                if result[2] <= self.zero:
                    cnt += 1

            # when entered to final leaf
            if len(clade_list) == 0:
                return clade

            else:
                # seperating db taxon and query taxon needed
                clade_dict = {}
                final_clade = []

                for result in clade_list:
                    # if clade does not have taxonomical information
                    if result[0] is False:
                        final_clade.append(result[1])

                    else:
                        # if new taxa
                        if not (result[0] in clade_dict):
                            clade_dict[result[0]] = [result]
                        # if already checked taxa
                        else:
                            clade_dict[result[0]].append(result)

                for taxon in clade_dict:
                    l = clade_dict[taxon]
                    r_list = [r[1] for r in l]
                    r_list.sort(key=lambda r: r.dist, reverse=True)
                    r_tuple = tuple(r_list)

                    # concatenate within taxon clades
                    concatenated_clade = concat_all(
                        clade_tuple=r_tuple, root_dist=self.zero, zero=self.zero
                    )
                    final_clade.append(concatenated_clade)

                final = concat_all(
                    clade_tuple=tuple(final_clade), root_dist=root_dist, zero=self.zero
                )

                return final.copy("newick")
            # end of solve flat

        if len(clade.children) in (0, 1):
            return clade.copy("newick")

        elif len(clade.children) == 2:

            solitum_flag = 0
            discolor_flag = 0

            clade1 = clade.children[0]
            clade2 = clade.children[1]

            if clade.dist <= self.zero:
                return solve_flat(clade).copy("newick")
            elif clade1.dist <= self.zero or clade2.dist <= self.zero:
                return solve_flat(clade).copy("newick")
            else:
                r_clade1 = self.reconstruct(clade1, gene)
                r_clade2 = self.reconstruct(clade2, gene)

            concatanated_clade = concat_clade(
                clade1=r_clade1,
                clade2=r_clade2,
                dist1=clade1.dist,
                dist2=clade2.dist,
                support1=clade1.support,
                support2=clade2.support,
                root_dist=clade.dist,
            ).copy("newick")
            return concatanated_clade

        else:
            print(clade)
            print(clade.children)
            print(len(clade.children))
            raise Exception

    def get_bgcolor(self):
        return self.opt.visualize.backgroundcolor[
            self.bgstate % len(self.opt.visualize.backgroundcolor)
        ]

    def collapse_tree(self):

        for taxon in self.collapse_dict:
            for collapse_info in self.collapse_dict[taxon]:

                clade = collapse_info.clade
                # if only one clade with same name exists
                if len(self.collapse_dict[taxon]) == 1:
                    # taxon_string = " ".join(collapse_info.taxon)
                    taxon_string = " ".join(taxon)
                else:
                    collapse_info.clade_cnt = (
                        self.collapse_dict[taxon].index(collapse_info) + 1
                    )
                    """
                    taxon_string = (
                        f'{" ".join(collapse_info.taxon)} {collapse_info.clade_cnt}'
                    )
                    """
                    taxon_string = f'{" ".join(taxon)} {collapse_info.clade_cnt}'

                taxon_text = TextFace(
                    taxon_string,
                    fsize=self.opt.visualize.fsize,
                    ftype=self.opt.visualize.ftype,
                    fgcolor=collapse_info.color,
                )

                space_text = TextFace(
                    "  ",
                    fsize=self.opt.visualize.fsize,
                    ftype=self.opt.visualize.ftype,
                    fgcolor=collapse_info.color,
                )

                accession_string = divide_by_max_len(
                    ",tmpseperator, ".join(
                        sorted(
                            self.funinfo_dict[x[0]].original_id
                            for x in collapse_info.leaf_list
                        )
                    ),
                    self.opt.visualize.maxwordlength,
                )
                accession_text = TextFace(
                    accession_string,
                    fsize=self.opt.visualize.fsize,
                    ftype=self.opt.visualize.ftype,
                )

                if collapse_info.collapse_type == "triangle":
                    rectangle = RectFace(
                        width=collapse_info.width,
                        height=collapse_info.height,
                        fgcolor=collapse_info.color,
                        bgcolor=collapse_info.color,
                    )
                    clade.add_face(rectangle, 1, position="branch-right")

                clade.add_face(space_text, 2, position="branch-right")
                clade.add_face(taxon_text, 3, position="branch-right")
                clade.add_face(space_text, 4, position="branch-right")
                clade.add_face(accession_text, 5, position="branch-right")

                # get all tip names of the current working clade
                collapse_leaf_name_list = [x[0] for x in collapse_info.leaf_list]

                # check if current working clade includes only outgroup sequences
                if all(
                    x in self.outgroup_leaf_name_list or x in collapse_info.query_list
                    for x in collapse_leaf_name_list
                ) and any(
                    x in self.outgroup_leaf_name_list for x in collapse_leaf_name_list
                ):

                    clade.img_style["bgcolor"] = self.opt.visualize.outgroupcolor
                    clade.img_style["draw_descendants"] = False

                else:
                    clade.img_style["bgcolor"] = self.get_bgcolor()
                    # change background color for next clade
                    self.bgstate += 1

                    clade.img_style["draw_descendants"] = False

        # self.outgroup_clade.img_style["bgcolor"] = self.option.outgroupcolor
        # self.outgroup_clade.img_style["draw_descendants"] = False

        # show branch support above 70%
        for node in self.t.traverse():

            # change this part when debugging flat trees
            node.img_style["size"] = 0  # removing circles whien size is 0
            """
            if node.dist <= 0.00000100000050002909:
                node.img_style["fgcolor"] = "red"
            """

            if node.support > self.opt.visualize.bscutoff:
                # node.add_face without generating extra line
                # add_face_to_node
                node.add_face(
                    TextFace(
                        f"{int(node.support)}",
                        fsize=self.opt.visualize.fsize_bootstrap,
                        fstyle="Arial",
                    ),
                    column=0,
                    position="float",
                )

    # end of collapse tree

    # Decide if string of the tree is bootstrap, scale, taxon or accession
    def decide_string(self, string):

        taxon_list = [" ".join(x) for x in self.collapse_dict.keys()]

        try:
            int(string)
            return "bootstrap"
        except:
            if string == "0.05":
                return "scale"
            elif any(taxon.strip() == string.strip() for taxon in taxon_list):
                return "taxon"
            else:
                return "accession"

    # edit svg image from initial output from ete3
    def polish_image(self, out, genus_list):

        # make it to tmp svg file and parse
        self.t.render(f"{out}", tree_style=self.Tree_style.ts)
        tree_xml = ET.parse(f"{out}")

        # in tree_xml, find all group
        _group = list(tree_xml.iter("{http://www.w3.org/2000/svg}g"))
        group_list = list(_group[0].findall("{http://www.w3.org/2000/svg}g"))

        # in tree_xml change all rectangles to polygon (trigangle)
        for group in group_list:
            if len(list(group.findall("{http://www.w3.org/2000/svg}rect"))) == 1:
                if group.get("fill") in (
                    "#000000",
                    self.opt.visualize.highlight,
                ):
                    rect = list(group.findall("{http://www.w3.org/2000/svg}rect"))[0]
                    rect.tag = "{http://www.w3.org/2000/svg}polygon"
                    rect.set(
                        "points",
                        f'{rect.get("width")},0 0,{int(rect.get("height"))/2} {rect.get("width")},{rect.get("height")}',
                    )

        # for taxons, gather all texts
        text_list = list(tree_xml.iter("{http://www.w3.org/2000/svg}text"))

        for text in text_list:

            # decide text type (taxon, scaling bar or bootstrap)
            text_type = self.decide_string(text.text)

            # relocate text position little bit for better visualization
            text.set("y", f'{int(text.get("y"))-2}')

            if text_type == "taxon":
                genus = get_genus_species(text.text, genus_list=genus_list)[0]
                species = get_genus_species(text.text, genus_list=genus_list)[1]
                rest = (
                    text.text.replace(genus, "").replace(species, "").replace(" ", "")
                )

                # shorten genus to one
                if self.opt.visualize.fullgenus is False:
                    genus = (
                        get_genus_species(text.text, genus_list=genus_list)[0][:1] + "."
                    )
                else:
                    genus = get_genus_species(text.text, genus_list=genus_list)[0]

                # split genus, species, rest of parent into tspan
                # parent.remove(text)
                text.text = ""
                tspan_list = []
                if genus != "":
                    tspan = ET.SubElement(text, "{http://www.w3.org/2000/svg}tspan")
                    tspan.text = genus + " "
                    tspan.set("font-style", "italic")

                if species != "":
                    tspan = ET.SubElement(text, "{http://www.w3.org/2000/svg}tspan")
                    tspan.text = species + " "
                    try:
                        int(species)
                    except:
                        if "sp." in species:
                            pass
                        else:
                            tspan.set("font-style", "italic")

                if rest != "":
                    tspan = ET.SubElement(text, "{http://www.w3.org/2000/svg}tspan")
                    tspan.text = rest + " "

            elif text_type == "bootstrap":
                int(text.text)
                # move text upper
                text.set("y", f'{int(text.get("y"))-8}')
                text.set("x", f'{int(text.get("x"))+1}')

            elif text_type == "accession":
                words = text.text.split(",tmpseperator, ")
                text.text = ""
                for word in words:
                    tspan = ET.SubElement(text, "{http://www.w3.org/2000/svg}tspan")
                    tspan.text = word + "  "
                    if self.decide_type(word, by="original_id") == "query":
                        tspan.set("fill", self.opt.visualize.highlight)

        # fit size of tree_xml to svg
        # find svg from tree_xml
        svg = list(tree_xml.iter("{http://www.w3.org/2000/svg}svg"))[0]
        # svg.set("width", "100%")
        # svg.set("height", "100%")

        # write to file
        tree_xml.write(
            out,
            encoding="utf-8",
            xml_declaration=True,
        )
