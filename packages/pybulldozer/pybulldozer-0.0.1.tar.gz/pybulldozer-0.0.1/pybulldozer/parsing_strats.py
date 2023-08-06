import xml.etree.ElementTree
import xml.etree.ElementTree as ET
from abc import abstractmethod, ABC

from pybulldozer.general.structure import Structure
from pybulldozer.general.node import Node


class Parser(ABC):
    """ Parsers convert a file-specific structure into a general pybulldozer structure """

    @abstractmethod
    def parse(self, filepath:str, summarize:bool=False) -> Structure:
        ...


class XmlParser(Parser):

    def parse(self, filepath:str, summarize:bool=False) -> Structure:
        """ Sets structure """

        structure = Structure(summarize=summarize)
        tree = ET.parse(source=filepath)
        root = tree.getroot()
        self.__recurse(elem=root, level=0, index=0, structure=structure)
        return structure

    def __recurse(self, elem: ET.Element, level: int, index:int, structure:Structure, parentNode: Node = None):
        """ Walks through the xml elements """

        # 1. If the structure should displays a summary we don't want to differentiate between nodes by index
        if (structure.summarize):
            index = 0

        # 2. Add the new node to the structure
        attrib_titles = None if (elem.attrib == {}) else list(elem.attrib)
        tagname = elem.tag.split("}")[1] if ("}" in elem.tag) else elem.tag
        node: Node = Node(tagname=tagname, depth=level, content=elem.text, attribs=attrib_titles, parent=parentNode, index=index)
        if (parentNode != None):
            parentNode.children.append(node)
        structure.add_node(newNode=node)

        # if (parentNode != None):
        #     input(f"parent={parentNode.id} ({len(parentNode.children)}) \t\t {node.id=}")

        # 3. Handle all children
        for c_index, child in enumerate(elem):
            self.__recurse(elem=child, level=level + 1, parentNode=node, index=c_index, structure=structure)


