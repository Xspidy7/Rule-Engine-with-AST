import mysql.connector
import json
import os  # Import os for environment variables
from node import Node

# Author: YourName
# GitHub: https://github.com/Xspidy7

# Establish a database connection using environment variables
try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=os.getenv("DB_PASSWORD", "Chetan333!!##"),  # Use environment variables for sensitive info
        database="sys"
    )
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)  # Exit if the connection fails

# Create a cursor object to execute queries
cursor = db.cursor()

def create_rule(rule_expression):
    """
    Inserts a new rule into the Rules table.
    
    Parameters:
    rule_expression (str): JSON string representing the rule expression.

    Returns:
    int: The ID of the created rule.
    
    Raises:
    ValueError: If the rule expression is invalid.
    """
    try:
        rule_expression_dict = json.loads(rule_expression)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format for rule expression.")

    if rule_expression_dict["type"] == "operand" and isinstance(rule_expression_dict["value"], int):
        rule_expression_dict["value"] = {
            "attribute": "value", 
            "operator": "=", 
            "value": rule_expression_dict["value"]
        }
    
    query = "INSERT INTO Rules (rule_expression) VALUES (%s)"
    cursor.execute(query, (json.dumps(rule_expression_dict),))
    db.commit()
    return cursor.lastrowid

def combine_rules(rule_ids):
    """
    Combines multiple rules identified by their IDs into a single rule.
    
    Parameters:
    rule_ids (list): List of rule IDs to combine.

    Returns:
    int: The ID of the combined rule.
    """
    query = "SELECT rule_expression FROM Rules WHERE id IN (%s)"
    cursor.execute(query, (",".join(map(str, rule_ids)),))
    rule_expressions = [row[0] for row in cursor.fetchall()]
    
    combined_expression_str = json.dumps({
        "type": "operator",
        "value": "AND",
        "left": json.loads(rule_expressions[0]),
        "right": json.loads(rule_expressions[1]) if len(rule_expressions) > 1 else None
    })
    query = "INSERT INTO Rules (rule_expression) VALUES (%s)"
    cursor.execute(query, (combined_expression_str,))
    db.commit()
    return cursor.lastrowid

def evaluate_rule(rule_id, user_data):
    """
    Evaluates a rule against provided user data.

    Parameters:
    rule_id (int): ID of the rule to evaluate.
    user_data (dict): Dictionary containing user attributes.

    Returns:
    bool: Result of the evaluation (True if user satisfies the rule, False otherwise).
    """
    query = "SELECT rule_expression FROM Rules WHERE id = %s"
    cursor.execute(query, (rule_id,))
    rule_expression = cursor.fetchone()[0]

    rule_expression = parse_ast_expression(rule_expression)
    
    result = evaluate_ast_expression(rule_expression, user_data)
    return result

def parse_ast_expression(expression):
    """
    Parses a JSON string into an AST Node.

    Parameters:
    expression (str | dict): The expression in JSON format.

    Returns:
    Node: The corresponding AST Node.
    """
    if isinstance(expression, str):
        expr_dict = json.loads(expression)
    else:
        expr_dict = expression

    left = parse_ast_expression(expr_dict["left"]) if "left" in expr_dict and isinstance(expr_dict["left"], dict) else expr_dict.get("left")
    right = parse_ast_expression(expr_dict["right"]) if "right" in expr_dict and isinstance(expr_dict["right"], dict) else expr_dict.get("right")
    return Node(expr_dict["type"], left=left, right=right, value=expr_dict.get("value"))

def combine_ast_expressions(expressions):
    """
    Combines multiple AST expressions into a single AST node.

    Parameters:
    expressions (list): List of AST expressions.

    Returns:
    Node: The combined AST node.
    """
    if not expressions:
        return None

    combined_node = parse_ast_expression(expressions[0])
    current_node = combined_node

    for expression in expressions[1:]:
        new_node = Node("operator", left=current_node, right=parse_ast_expression(expression), value="AND")
        current_node = new_node

    return current_node

def evaluate_ast_expression(expression, user_data):
    """
    Evaluates the AST expression recursively.

    Parameters:
    expression (Node): The root of the AST to evaluate.
    user_data (dict): The user data for evaluation.

    Returns:
    bool: Result of the evaluation.
    """
    if expression.type == "operand":
        return evaluate_operand(expression, user_data)
    elif expression.type == "operator":
        return evaluate_operator(expression, user_data)

def evaluate_operand(node, user_data):
    """
    Evaluates the operand value against the user data.

    Parameters:
    node (Node): The operand node to evaluate.
    user_data (dict): The user data for evaluation.

    Returns:
    bool: Result of the evaluation.
    """
    attribute = node.value["attribute"]
    operator = node.value["operator"]
    value = node.value["value"]
    
    if operator == "=":
        return user_data.get(attribute) == value
    elif operator == ">":
        return user_data.get(attribute) > value
    
    return False

def evaluate_operator(node, user_data):
    """
    Evaluates the left and right child nodes of an operator.

    Parameters:
    node (Node): The operator node to evaluate.
    user_data (dict): The user data for evaluation.

    Returns:
    bool: Result of the evaluation.
    """
    left_result = evaluate_ast_expression(node.left, user_data)
    right_result = evaluate_ast_expression(node.right, user_data)
    
    if node.value == "AND":
        return left_result and right_result
    elif node.value == "OR":
        return left_result or right_result
    
    return False
