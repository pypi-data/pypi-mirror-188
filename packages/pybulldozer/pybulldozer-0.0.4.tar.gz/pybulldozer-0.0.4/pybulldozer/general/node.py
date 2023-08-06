from __future__ import annotations

from dataclasses import dataclass

from pybulldozer.loddict import Lod_dict



@dataclass
class NodeTypes:
    leaf:str = "leaf"         # tag with a value                          -> {}
    # keyvalue:str = "keyvalue" # all children are leafs                    -> {}
    array:str = "array"       # all children are leafs with same tagname  -> []
    object:str = "object"     # has leafs and arrays as children
    empty:str = "empty"       #self-closing


class Node:
    # Identification
    id:str
    structure_id:str
    # Structural information
    tagname:str
    depth:int
    index:int
    # Node-specific
    parent:Node
    children: [Node]
    content:str
    attributes:[str]
    # Meta-data
    count:int

    def __init__(self, tagname:str, depth:int, content:str, attribs:[str]=None, parent:Node=None, index:int=0):
        self.tagname = tagname
        self.depth = depth
        self.index = index
        self.content = content.strip()[:30] if (content != None) else None
        self.count = 1
        self.attributes = [] if (attribs == None) else attribs
        self.parent = parent
        self.children = []
    def __eq__(self, other:Node) -> bool:
        """  """
        if (other == None):
            return False
        return self.id == other.id
    def __add__(self, other:Node) -> None:
        self.attributes = list(set(self.attributes + other.attributes))
        self.content = self.content or other.content
        self.count += 1
    def __str__(self) -> str:
        """ """
        return f"[NODE id={self.id}]"
        # return self.format_node(indentation=1, show_attribs=False)
    def __repr__(self) -> str:
        return self.__str__()
    def __hash__(self):
        return hash(self.id)

    @property
    def id(self):
        """ Determines when a node is unique, e.g: the combination of depth, index and tagname """
        parent_id = f"{self.parent.id}>" if (self.parent != None) else ""
        return parent_id + f"D{self.depth}_I{self.index}_T{self.tagname}"
    @property
    def structure_id(self):
        """ Determines when a node is unique, e.g: the combination of depth, count and tagname
            Because index is not taken into account the nodes can be summarized and counted
        """
        parent_id = f"{self.parent.id}>" if (self.parent != None) else ""
        return parent_id + f"D{self.depth}_C{self.count}_T{self.tagname}"
    @property
    def nodetype(self) -> str:
        hascontent = self.content != None and self.content != ''
        haschildren = len(self.children) > 0
        allChildrenSameTag = len(list(set([n.tagname for n in self.children]))) == 1 and len(self.children) > 1


        nodetype = None
        if (hascontent):
            nodetype = NodeTypes.leaf
        else:
            if (haschildren):       # no content, yes children
                if (allChildrenSameTag):
                    nodetype = NodeTypes.array
                else:
                    nodetype = NodeTypes.object
                    # if (allChildrenAreLeafs):
                    #     nodetype = NodeTypes.keyvalue
                    # else:
                    #     nodetype = NodeTypes.object
            else:
                nodetype = NodeTypes.empty

        return nodetype
    @property
    def __hasContent(self) -> bool:
        return (self.content != None and self.content != '')
    @property
    def __hasChildren(self) -> bool:
        return len(self.children) > 0
    @property
    def __isLeaf(self) -> bool:
        return (not self.__hasChildren and self.__hasContent)
    @property
    def __record_id(self):
        """ This is the ID that each database table record will get """
        return self.index


    def flatten_node(self, foreign_key_node:Node=None, lod_dict:Lod_dict=None) -> Lod_dict:
        """ Unpacks the node a dictionary, all children are unpacked to different dictionaries. Dictionaries are kept in lod_dict
        :param foreign_key_node: str       This node's first ancestor that is NOT an array
        :param lod_dict: Lod_dict   Structure in which we keep track of the lod_dict arrays by name of the node
        :return: lod_dict: Lod_dict Dictionary. Key=tablename, value=record_array
        """

        node_dict = {}

        c:Node
        if (self.nodetype == NodeTypes.empty):
            pass
        elif (self.nodetype in [NodeTypes.leaf]):
            # Creates a record for this leaf alone
            node_dict[self.tagname] = self.content
        elif (self.nodetype in [NodeTypes.array]):
            for c in self.children:
                c.flatten_node(foreign_key_node=foreign_key_node, lod_dict=lod_dict)
        elif (self.nodetype in [NodeTypes.object]):
            for c in self.children:
                if (c.nodetype == NodeTypes.empty):
                    pass
                elif (c.nodetype == NodeTypes.leaf):
                    node_dict[c.tagname] = c.content
                else:
                    c.flatten_node(foreign_key_node=self, lod_dict=lod_dict)
        else:
            raise ValueError(f"fileparser: Unknown node type: {self}")


        if (node_dict == {}):
            return lod_dict

        # HANDLE IDS AND FOREIGN KEYS
        node_dict['id'] = self.__record_id
        if (foreign_key_node):
            if (foreign_key_node.id != self.id):
                # foreign_key_colname = f'foreign_key'
                foreign_key_colname = f"{foreign_key_node.tagpath()}_id"
                node_dict[foreign_key_colname] = foreign_key_node.__record_id
        # / HANDLE IDS AND FOREIGN KEYS

        lod_dict.add(name=self.tagpath(), record=node_dict)

        return lod_dict
    def tagpath(self) -> str:
        """" Get the tree of tagnames from root till this node """
        parent_tag = f"{self.parent.tagpath()}_" if (self.parent != None) else ""
        return parent_tag + self.tagname.lower()

    def format_node(self, indentation:int=1, show_attribs:bool=False, padding:int=100, add_id:bool=False, add_structure_id:bool=False) -> str:
        """ Determines how the node will be displayed in the console """
        the_indent = f"" if (self.depth == 0) else f"|{'-' * indentation * self.depth}"
        the_tagname = self.tagname.ljust(padding - len(the_indent))
        tagname_count = f"#{str(self.count).rjust(6)}"

        attrib_info = ""
        if (len(self.attributes) > 0):
            attrib_info = f"attributes: {self.attributes}" if (show_attribs) else f"({len(self.attributes)} attribs)"

        example_content = f"{self.content.rjust(55 - len(attrib_info)) if (self.content != None) else ''}"
        nodeId = f"\t{self.id}" if (add_id) else ""
        structureId = f"\t{self.structure_id}" if (add_structure_id) else ""
        thestring = f"{the_indent}{the_tagname} {tagname_count} {attrib_info} {example_content}{nodeId}{structureId}"
        return thestring

