import os

from pybulldozer.helpers import logger
from pybulldozer.loddict import Lod_dict
from pybulldozer.parsing_strats import Parser


# if (os.environ.get("USECYTHON") == "y"):
#     logger.warning("USING CYTHON")
#     from pybulldozer.general_cy.structure import Structure
#     from pybulldozer.general_cy.node import Node
# else:
from pybulldozer.general.structure import Structure
from pybulldozer.general.node import Node
from colorama import Fore, Back, Style


class FileParser:

    parser:Parser

    def __init__(self, parser:Parser):
        """ Sets inputs and calls validate function """
        self.parser = parser

    def get_signature(self, filepath:str):
        """ Returns a hash that determines the exact """
        structure:Structure = self.parser.parse(filepath=filepath, summarize=True)
        return structure.get_signature()

    def display_structure_difference(self, filepath1:str, filepath2:str) -> None:
        """ Finds the differences in structure between two files
            Returns how file
        """

        # 1. Get the summarized nodelists of both files.
        structure1:Structure = self.parser.parse(filepath=filepath1, summarize=True)
        nodelist1 = structure1.get_node_list()
        structure2:Structure = self.parser.parse(filepath=filepath2, summarize=True)
        nodelist2 = structure2.get_node_list()

        # if (structure1.get_signature() == structure2.get_signature()):
        #     logger.debug(msg=f"{self.display_structure_difference.__name__} - files match")
        #     return None

        # 2. Prepare all lists: allnodes must be unique (by structure_id) nodes from both lists, create sets of structure_ids from both lists
        allnodes:[Node] = list({n.structure_id: n for n in nodelist1 + nodelist2}.values())
        allnodes.sort(key=lambda n: (n.id))
        idset1 = set([f"{n.structure_id}" for n in nodelist1])
        idset2 = set([f"{n.structure_id}" for n in nodelist2])

        # 3. Compare the nodelists; determine disjoint nodes
        left_only_struct_ids:[str] = [n.structure_id for n in nodelist1 if (n.structure_id in idset1.difference(idset2))]
        right_only_struct_ids:[str] = [n.structure_id for n in nodelist2 if (n.structure_id in idset2.difference(idset1))]

        # 4. Loop through all nodes and determine color
        for n in allnodes:
            color = Fore.BLUE
            if (n.structure_id in left_only_struct_ids): color = Fore.GREEN
            if (n.structure_id in right_only_struct_ids): color = Fore.RED
            destring = n.format_node(padding=30, show_attribs=False, add_structure_id=False)
            print(color, destring)
        else:
            print(Style.RESET_ALL, end='\r')


    def display_structure(self, filepath:str, include_attribs:bool=True, include_ids:bool=True) -> None:
        """ Prints out the structure of the provided file """
        structure:Structure = self.parser.parse(filepath=filepath, summarize=True)
        print(structure.get_formatted_structure(show_attribs=include_attribs, add_id=include_ids))

    def flatten_file(self, filepath:str, target_tagname:str):
        """ Flattens the file into a dictionary of {tablename: list_of_records} """

        logger.debug(msg=f"{self.flatten_file.__name__} | start flatten up until tag '{target_tagname}'")

        # 1. Parse the file
        structure:Structure = self.parser.parse(filepath=filepath, summarize=False)
        logger.debug(msg=f"{self.flatten_file.__name__} | parsed file with summarized = false")

        # 2. Get a list of all nodes with the target tagname
        target_node_list = structure.get_node_list(tagname_filter=target_tagname)
        logger.debug(msg=f"{self.flatten_file.__name__} | Got list that contains {len(target_node_list)} target nodes")

        # 3. Go through each target_node and flatten each child
        lod_dict = Lod_dict()
        for targetnode in target_node_list:
            lod_dict = targetnode.flatten_node(foreign_key_node=targetnode, lod_dict=lod_dict)
        logger.debug(msg=f"{self.flatten_file.__name__} | Flatteded target nodes")

        # 3. Check out result
        lod_dict.debug(sample=False)


    def get_table_create(self, filepath:str):
        # self.parser.set_summary(summarize=True)
        # self.parser.parse(filepath=filepath)

        raise NotImplementedError("To do")