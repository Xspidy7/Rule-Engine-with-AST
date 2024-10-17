class Node:
    """
    Represents a node in the Abstract Syntax Tree (AST) used for rule evaluation.
    
    Attributes:
    - type (str): The type of the node, either "operator" or "operand".
    - left (Node or None): Reference to the left child node.
    - right (Node or None): Reference to the right child node.
    - value (any): Optional value for operand nodes.
    """
    
    def __init__(self, node_type, left=None, right=None, value=None):
        """
        Initializes a new AST node.

        Parameters:
        node_type (str): The type of the node ("operator" or "operand").
        left (Node, optional): The left child node. Defaults to None.
        right (Node, optional): The right child node. Defaults to None.
        value (any, optional): The value of the node. Defaults to None.
        """
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

# Author: Ujjawal Pathak
# GitHub: https://github.com/Xspidy7
