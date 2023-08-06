from dataclasses import dataclass
from pybulldozer.loddict import Lod_dict
@dataclass
class NodeTypes:
    leaf:str = "leaf"
    array:str = "array"
    object:str = "object"
    empty:str = "empty"
class Node:
    id:str
    structure_id:str
    tagname:str
    depth:int
    index:int
    parent:Node
    children: [Node]
    content:str
    attributes:[str]
    count:int
    def __init__(self, tagname:str, depth:int, content:str, attribs:[str]=None, parent:Node=None, index:int=0):
        ...
    def __eq__(self, other:Node) -> bool:
        ...
    def __add__(self, other:Node) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __repr__(self) -> str:
        ...
    def __hash__(self):
        ...
    @property
    def id(self):
        ...
    @property
    def structure_id(self):
        ...
    @property
    def nodetype(self) -> str:
        ...
    @property
    def __hasContent(self) -> bool:
        ...
    @property
    def __hasChildren(self) -> bool:
        ...
    @property
    def __isLeaf(self) -> bool:
        ...
    @property
    def __record_id(self):
        ...
    def flatten_node(self, foreign_key_node:Node=None, lod_dict:Lod_dict=None) -> Lod_dict:
        ...
    def tagpath(self) -> str:
        ...
    def format_node(self, indentation:int=1, show_attribs:bool=False, padding:int=100, add_id:bool=False, add_structure_id:bool=False):
        ...
