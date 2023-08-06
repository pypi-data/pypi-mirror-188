from __future__ import annotations

from pybulldozer.general.node import Node



""" General structure for non-relational file data. 
    :arg summarize  bool    for summarizing the structure of the file
"""
class Structure:

    summarize:bool
    __nodelist:[Node]

    def __init__(self, summarize:bool=False):
        self.summarize = summarize
        self.__nodelist = []
    def __len__(self):
        return len(self.__nodelist)
    def __contains__(self, node:Node):
        return node in self.__nodelist

    def get_node(self, targetNode:Node) -> Node:
        """ Retrieves a node from the structure. Returns None if node is not found """

        for node in self.__nodelist:
            if (targetNode == node):
                return node

    def node_in_structure(self, node:Node) -> bool:
        """ Returns t/f depending on wheteher the node is already contained in this structure """
        return node.id in [n.id for n in self.__nodelist]

    def add_node(self, newNode:Node) -> None:
        """ Tries to combine nodes if node is already present, else adds a new one """

        if (self.summarize and self.node_in_structure(node=newNode)):
                foundNode:Node = self.get_node(newNode)
                foundNode + newNode
        else:
            self.__nodelist.append(newNode)

    def get_node_list(self, sorted:bool=False, tagname_filter:str=None):
        """ """
        nodelist:[Node] = self.__nodelist.copy()
        n: Node
        if (tagname_filter != None):
            nodelist = [n for n in nodelist if (n.tagname == tagname_filter)]
        if (sorted):
            nodelist.sort(key=lambda n: (n.id))
        return nodelist
    def get_formatted_structure(self, indentation:int=1, show_attribs:bool=False, add_id:bool=False) -> str:
        """ Sorts each node by id and styles the nodes before returning the structure as a string """
        sorted_list = self.get_node_list(sorted=True)
        max_node_name = max([len(n.tagname) for n in sorted_list])
        max_indent = max([n.depth for n in sorted_list]) * indentation
        padding = max_node_name + max_indent + 10
        n:Node
        return "\n".join([n.format_node(indentation=indentation, show_attribs=show_attribs, padding=padding, add_id=add_id) for n in sorted_list])

    def get_signature(self):
        """ Returns the signature of the structure; a hashed representation of all its summarized elements """
        n:Node
        sorted_list = sorted(self.__nodelist, key=lambda n: (n.id))
        joined_list = "".join([f"{n.id}_{n.count}" for n in sorted_list])
        return hash(joined_list)

    def get_node_by_id(self, node_id:str):
        """ """
        n:Node
        nodelist = [n for n in self.__nodelist if (n.id == node_id)]
        if (len(nodelist) == 0):
            return None
        return nodelist[0]